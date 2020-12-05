import numpy as np
import random
from matplotlib import pyplot as plt
import mnist_loader

def run_network(sizes, eta, epochs):
    print('Start {0} {1} {2}'.format(sizes, eta, epochs))
    training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
    net = Network(sizes)
    ret = []
    for i in range(epochs):
        net.SGD(training_data, 1, 10, eta)
        ret.append((net.evaluate(test_data), net.evaluate_c(test_data)))
    print('Finish {0} {1} {2}'.format(sizes, eta, epochs))
    return ret


def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))
def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))

def show_image(x, y):
    plt.title(str(y))
    plt.imshow(x.reshape((28, 28)), cmap='gray')
    plt.show()

class Network(object):

    def __init__(self, sizes):
        self.num_layers, self.sizes = len(sizes), sizes
        self.bias = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weight = [np.random.randn(y, x)
                  for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        for w, b in zip(self.weight, self.bias):
            a = sigmoid(np.dot(w, a) + b)
        return a
    
    def SGD(self, traning_data, epochs, mini_batch_size, eta, test_data=None):
        if test_data: n_test = len(test_data)
        n = len(traning_data)
        for j in range(epochs):
            random.shuffle(traning_data)
            mini_batches = [
                traning_data[k:k+mini_batch_size]
                for k in range(0, n, mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print('Epoch {0}: {1} / {2}'.format(
                    j, self.evaluate(test_data), n_test
                ))
    
    def update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.bias]
        nabla_w = [np.zeros(w.shape) for w in self.weight]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weight = [w - (eta/len(mini_batch))*nw
                       for w, nw in zip(self.weight, nabla_w)]
        self.bias = [b - (eta/len(mini_batch))*nb
                       for b, nb in zip(self.bias, nabla_b)]
    
    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.bias]
        nabla_w = [np.zeros(w.shape) for w in self.weight]
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.bias, self.weight):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        delta = self.cost_derivative(activations[-1], y) * \
                sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weight[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        results = [(np.argmax(self.feedforward(x)), y)
                   for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in results)
    
    def evaluate_return_wrong(self, test_data):
        ret = []
        for x, y in test_data:
            res = self.feedforward(x)
            if np.argmax(res) != y:
                ret.append((x, y, np.argmax(res), res))
        return ret

    def evaluate_c(self, test_data):
        ret = np.float64()
        for x, y in test_data:
            a = self.feedforward(x)
            ary = np.zeros((10, 1))
            ary[y] = 1
            ret = ret + np.sum((a-ary)**2)
        return ret/len(test_data)

    def cost_derivative(self, output_activations, y):
        return (output_activations-y)
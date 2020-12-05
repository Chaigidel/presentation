import mnist_loader
import network
training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
net = network.Network([784, 30, 10])
net.SGD(training_data, 1, 10, 3.0, test_data=test_data)
# x, y = training_data[0]
# net.backprop(x, y)
print(net.evaluate_c(test_data))
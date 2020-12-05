import mnist_loader
import network
import json
import time
ETA = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0]
LAYERS = [1, 2, 3, 4]
NUM = [5, 10, 20, 30, 50, 70, 90, 100]

# ETA = [0.5]
# LAYERS = [1]
# NUM = [5]

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

def run_network(layers, eta):
    net = network.Network([784]+layers+[10])
    ret = []
    for i in range(40):
        print(i)
        s = time.time()
        net.SGD(training_data, 1, 10, eta)
        t = time.time()
        ret.append((net.evaluate(test_data), net.evaluate_c(test_data), t-s))
    return ret

output = []

for eta in ETA:
    for layers in LAYERS:
        for num in NUM:
            print(eta, layers, num)
            output.append(['{0} {1} {2}'.format(eta, layers, num),
                           run_network([num]*layers, eta)])
            print(eta, layers, num)

json.dump(output, open('result.json', 'w'))

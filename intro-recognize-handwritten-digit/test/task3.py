import json
import mnist_loader
import network
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

def load_json(n):
    return json.load(open(n, 'r'))

def run_network(eta):
    net = network.Network([784, 30, 10])
    ret = []
    for i in range(40):
        s = time.time()
        net.SGD(training_data, 1, 10, eta)
        t = time.time()
        ret.append((net.evaluate(test_data), net.evaluate_c(test_data), t-s))
    return ret

def main():
    tests = load_json('task3.json')
    result = []
    for eta in tests:
        result.append(run_network(eta))
        print('F')
    json.dump(result, open('task3_result.json', 'w'))

def draw():
    tests = load_json('task3.json')
    datas = load_json('task3_result.json')
    ETAS = tests
    NUM_EPOCHS = 40

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for eta, result in zip(ETAS, datas):
        # print(result)
        num = [i[0] for i in result]
        ax.plot(np.arange(NUM_EPOCHS), num, "o-",
                label="$\eta$ = "+str(eta))
    zhfont1 = matplotlib.font_manager.FontProperties(fname="/usr/share/fonts/adobe-source-han-sans/SourceHanSansCN-Regular.otf") 
    ax.set_title('学习率 $\eta$ 对识别率的影响', fontproperties=zhfont1)
    ax.set_xlim([0, NUM_EPOCHS])
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Correct')
    plt.legend(loc='upper right')
    plt.show()

def check():
    tests = load_json('task3.json')
    datas = load_json('task3_result.json')
    ans = 0
    for layer, result in zip(tests, datas):
        ans = max([i[0] for i in result])
        print(layer, ans)


if __name__ == "__main__":
    # main()
    # draw()
    check()
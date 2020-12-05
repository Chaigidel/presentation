import json
import mnist_loader
import network
import time
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool
import matplotlib

def load_json(n):
    return json.load(open(n, 'r'))

def main():
    tests = load_json('task1.json')
    procs = []
    p = Pool()
    for test in tests:
        # result.append(network.run_network([784, test, 10], 3.0, 40))
        procs.append(
            p.apply_async(network.run_network,
                          args=([784, test, 10], 3.0, 40, )
            )
        )
    p.close()
    p.join()
    result = [proc.get() for proc in procs]
        # print('F')
    json.dump(result, open('task1_result.json', 'w'))

def draw():
    tests = load_json('task1.json')
    datas = load_json('task1_result.json')
    LAYERS = tests
    # COLORS = ['#2A6EA6', '#FFCD33', '#FF7033']
    NUM_EPOCHS = 40

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for layer, result in zip(LAYERS, datas):
        # print(result)
        num = [i[0] for i in result]
        ax.plot(np.arange(NUM_EPOCHS), num, "o-",
                label="node = "+str(layer))
    zhfont1 = matplotlib.font_manager.FontProperties(fname="/usr/share/fonts/adobe-source-han-sans/SourceHanSansCN-Regular.otf") 
    ax.set_title('节点数量（单层）对识别率的影响', fontproperties=zhfont1)
    ax.set_xlim([0, NUM_EPOCHS])
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Correct')
    plt.legend(loc='upper right')
    plt.show()

def check():
    tests = load_json('task1.json')
    datas = load_json('task1_result.json')
    ans = 0
    for layer, result in zip(tests, datas):
        ans = max([i[0] for i in result])
        print(layer, ans)

if __name__ == "__main__":
    # main()
    # draw()
    check()
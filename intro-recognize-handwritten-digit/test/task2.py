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
    tests = load_json('task2.json')
    procs = []
    p = Pool()
    for test in tests:
        procs.append(
            p.apply_async(network.run_network,
                          args=([784]+[30]*test+[10], 3.0, 40, )
            )
        )
    p.close()
    p.join()
    result = [proc.get() for proc in procs]
        # print('F')
    json.dump(result, open('task2_result.json', 'w'))

def draw():
    tests = load_json('task2.json')
    datas = load_json('task2_result.json')
    LAYERS = tests
    # COLORS = ['#2A6EA6', '#FFCD33', '#FF7033']
    NUM_EPOCHS = 40

    zhfont1 = matplotlib.font_manager.FontProperties(fname="/usr/share/fonts/adobe-source-han-sans/SourceHanSansCN-Regular.otf") 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for layer, result in zip(LAYERS, datas):
        # print(result)
        num = [i[0] for i in result]
        ax.plot(np.arange(NUM_EPOCHS), num, "o-",
                label="layer = "+str(layer))
    ax.set_title('不同层数（每层节点 30 个）对识别率的影响', fontproperties=zhfont1)
    ax.set_xlim([0, NUM_EPOCHS])
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Correct')
    plt.legend(loc='upper right')
    plt.show()

def check():
    tests = load_json('task2.json')
    datas = load_json('task2_result.json')
    ans = 0
    for layer, result in zip(tests, datas):
        ans = max([i[0] for i in result])
        print(layer, ans)


if __name__ == "__main__":
    # main()
    # draw()
    check()
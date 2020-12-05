from matplotlib import pyplot as plt
import pickle
d = pickle.loads(open('qaq', 'br').read())
# def show_image(x, y):
#     plt.title(str(y))
#     plt.imshow(x.reshape((28, 28)), cmap='gray')
#     plt.show()
# show_image(d[0][0], d[0][1])
import random
# random.shuffle(d)
plt.figure()
for i in range(5*13):
    n = 65*4+i
    x, y = d[n][0], d[n][1]
    plt.subplot(5, 13, i+1)
    plt.imshow(x.reshape((28, 28)), cmap='gray')
    plt.xticks([])
    plt.yticks([])
    plt.title(y)
plt.show()
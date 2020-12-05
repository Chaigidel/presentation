import numpy
import matplotlib.pyplot as plt

z = numpy.arange(-5, 5, .01)
sigma_fn = numpy.vectorize(lambda z: 4*z*z*z*z+1.5*z*z*z-3*z*z)
sigma = sigma_fn(z)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(z, sigma)
ax.set_ylim([-1.5, 4])
ax.set_xlim([-2,2])
ax.grid(True)
ax.set_xlabel('w')
ax.set_ylabel('Cx')


plt.show()

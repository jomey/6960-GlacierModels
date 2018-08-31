import matplotlib.pyplot as plt
import numpy as np


class Glacier(object):
    ICE_DENSITY = 920       # kg/m^3
    MANTEL_DENSITY = 1
    GRAVITY = 10
    SHEER_STRESS = 0.5e5

    ICE_CONSTANT = (2 * SHEER_STRESS)/(ICE_DENSITY * GRAVITY)
    ISOSTASY = 0.4

    def __init__(self, length, isostatic=False):
        self._length = length
        self._midpoint = self._length / 2
        self._isostatic = isostatic

    @property
    def length(self):
        return self._length

    @property
    def midpoint(self):
        return self._midpoint

    @property
    def isostatic(self):
        return self._isostatic

    @isostatic.setter
    def isostatic(self, value):
        self._isostatic = value

    def height(self, x):
        if x <= self.midpoint:
            x = Glacier.lower_bound(x)
        else:
            x = self.upper_bound(x)

        if self.isostatic:
            x = x * Glacier.ISOSTASY

        return x ** (1/2)

    @staticmethod
    def lower_bound(x):
        return Glacier.ICE_CONSTANT * x

    def upper_bound(self, x):
        return Glacier.ICE_CONSTANT * (self.length - x)


if __name__ == '__main__':
    resolution = 100
    glacier_length = 100000
    x = np.arange(start=0, stop=glacier_length, step=resolution)

    glacier = Glacier(length=glacier_length)
    y = [glacier.height(value) for value in x]

    glacier.isostatic = True
    y_isostatic = [glacier.height(value) for value in x]

    plt.plot(x, y, linestyle='solid')
    plt.plot(x, y_isostatic, linestyle='dashed', label='isostatic')
    plt.legend()
    plt.xlabel('Length of Glacier')
    plt.ylabel('Thickness of the Glacier')
    plt.show()
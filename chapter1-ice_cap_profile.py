import matplotlib.pyplot as plt
import numpy as np

from glacier import Glacier

if __name__ == '__main__':
    resolution = 100
    glacier_length = 100000

    x = np.arange(start=0, stop=glacier_length + 1, step=resolution)

    glacier = Glacier(length=glacier_length)
    y = [glacier.surface_height(value) for value in x]

    glacier.isostatic = True
    y_isostatic = [glacier.surface_height(value) for value in x]
    y_isostatic_b = [glacier.bed_depth(value) for value in y_isostatic]

    plt.plot(x, y, linestyle='solid')
    plt.plot(x, y_isostatic, linestyle='dashed', label='isostatic', color='orange')
    plt.plot(x, y_isostatic_b, linestyle='dashed', color='orange')
    plt.legend()
    plt.xlabel('Length of Glacier')
    plt.ylabel('Thickness of the Glacier')
    plt.show()

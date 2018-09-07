import matplotlib.pyplot as plt
import numpy as np
import math

from glacier import Glacier

if __name__ == '__main__':
    resolution = 100
    glacier_length = 100000
    x = np.arange(start=0, stop=glacier_length + 1, step=resolution)

    glacier = Glacier(length=glacier_length, isostatic=True)

    densities = dict([
        (3410, dict(linestyle='solid', color='black')),
        (3350, dict(linestyle='dotted', color='red')),
        (3270, dict(linestyle='dashed', color='blue')),
    ])

    plt.figure(figsize=(15, 8))

    for density, line_style in densities.items():
        glacier.mantel_density = density

        surface_height = [glacier.surface_height(value) for value in x]
        bed_depth = [glacier.bed_depth(value) for value in surface_height]

        plt.plot(
            x, surface_height, label='Density ' + str(density), **line_style
        )
        plt.plot(x, bed_depth, **line_style)

        max_height = max(surface_height)
        max_depth = min(bed_depth)
        print('\nStats for density ' + str(density) + ':\n')
        print('  Maximum surface height: ' + str(max_height))
        print('  Minimum bed depth: ' + str(max_depth))
        print(
            '  Maximum glacier thickness: ' +
            str(max_height + math.fabs(max_depth))
        )

    plt.legend(fontsize=24)
    plt.xlabel('Length of Glacier', size=32)
    plt.xticks(fontsize=24)
    plt.ylabel('Thickness of the Glacier', size=32)
    plt.yticks(fontsize=24)
    plt.title('Glacier height with varying mantle densities', size=42)
    plt.show()

import matplotlib.pyplot as plt
import numpy as np

from glacier import Glacier

if __name__ == '__main__':
    elevations = np.arange(4000, 5100, 100)
    slopes = np.arange(0.05, 0.30, 0.05)

    glacier = Glacier(height=5500)

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col', figsize=(14,10))

    for slope in slopes:
        lengths = [
            glacier.linear_equilibrium_length(elevation, slope)
            for elevation in elevations
        ]

        ax1.plot(lengths, elevations, label=slope.round(2))

    for elevation in elevations:
        lengths = [
            glacier.linear_equilibrium_length(elevation, slope)
            for slope in slopes
        ]

        ax2.plot(lengths, slopes, label=elevation, linewidth=.75)

    ax1.set_title("Basic Glacier Model on Linear Slope")
    ax1.set_ylabel("Equilibrium Line Altitude (ELA) (m)")
    ax1.tick_params(labelbottom=True)
    ax1.legend(title='Slope Angles')
    ax2.set_ylabel("Bed Slope")
    ax2.set_xlabel("Glacier Length (m)")
    ax2.legend(title='Glacier Elevations')
    plt.show()


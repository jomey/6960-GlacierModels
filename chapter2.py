import matplotlib.pyplot as plt
import numpy as np

from glacier import Glacier

if __name__ == '__main__':
    ela_elevations = np.arange(4000, 5100, 100)
    ela_changes = np.arange(100, 510, 100)
    slopes = np.arange(0.05, 0.30, 0.05)

    glacier = Glacier(max_bed_height=5500)

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(
        nrows=3, ncols=2, figsize=(14, 10)
    )

    # Length change with varying ELA
    for slope in slopes:
        glacier.slope = slope
        length_change = [
            glacier.linear_equilibrium_length(elevation)
            for elevation in ela_elevations
        ]
        ax1.plot(ela_elevations, length_change, label=slope.round(2))
    ax1.set_title('Length change with varying ELA')
    ax1.legend(title='Slope')

    # Change of length over change of ELA
    for slope in slopes:
        lengths = [
            glacier.length_change(ela_change, slope)
            for ela_change in ela_changes
        ]
        ax3.plot(ela_changes, lengths, label=slope.round(2))
    ax3.set_title('Length change with varying ELA change')
    ax3.legend(title='Slope')

    # Fraction of change of length over change of ELA
    for slope in slopes:
        lengths = [
            glacier.fractional_length_change(4500, ela_change, slope)
            for ela_change in ela_changes
        ]
        ax5.plot(ela_changes, lengths, label=slope.round(2))
    ax5.set_title('Fractional length change with varying ELA change, ELA = 4500 m')
    ax5.legend(title='Slope')

    # Change of length over varying slope
    for ela_elevation in ela_elevations:
        lengths = []
        for slope in slopes:
            glacier.slope = slope
            lengths.append(glacier.linear_equilibrium_length(ela_elevation))
        ax2.plot(slopes, lengths, label=ela_elevation)
    ax2.set_title('Length change with varying slope')
    ax2.legend(title='ELA elevation')

    # Length change with varying slope
    for ela_change in ela_changes:
        lengths = [
            glacier.length_change(ela_change, slope)
            for slope in slopes
        ]
        ax4.plot(slopes, lengths, label=ela_change)
    ax4.set_title('Length change with varying slope')
    ax4.legend(title='ELA change')

    # Fraction of change in length with varying slope
    # Change in ELA 250m
    for ela_elevation in ela_elevations:
        lengths = [
            glacier.fractional_length_change(ela_elevation, 250, slope)
            for slope in slopes
        ]
        ax6.plot(slopes, lengths, label=ela_elevation)
    ax6.set_title('Fractional length change with varying slope, ELA change 250')
    ax6.legend(title='ELA elevation')

    plt.show()

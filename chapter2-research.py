import matplotlib.pyplot as plt

from glacier import Glacier

# Greenland ice sheet
# Assumption uniform width for entire section
# Total length
# Critical ELA
#   Use ela_from_length to verify
# Ice thickness
#
# 	                    North	    East 	    South 	    West
# Max Bedrock	        1392    	2527    	2906    	1127
# Max surface	        2914	    3233	    3173    	3041
# min surface	        736 	    955     	214     	615
# mean_ice_thickness	1417	    1557    	1974    	2101
# length_of_segment	    820000	    380000	    1150000	    380000

BASINS = {
    'North': {
        'bed_height': 1392,
        'mean_ice_thickness': 1417,
        'max_surface': 2914,
        'min_surface': 736,
        'length_of_segment': 820000,
    },
    'East': {
        'bed_height': 2527,
        'mean_ice_thickness': 1557,
        'max_surface': 3233,
        'min_surface': 955,
        'length_of_segment': 380000,
    },
    'South': {
        'bed_height': 2906,
        'mean_ice_thickness': 1974,
        'max_surface': 3173,
        'min_surface': 214,
        'length_of_segment': 1150000,
    },
    'West': {
        'bed_height': 1127,
        'mean_ice_thickness': 2101,
        'max_surface': 3041,
        'min_surface': 0,
        'length_of_segment': 380000,
    },
}


def calc_slope(min_surface, max_surface, length):
    return (max_surface - min_surface) / length


if __name__ == '__main__':
    glacier = Glacier()

    measured_length = []
    linear_equilibrium_length = []

    max_surfaces = []
    ela = []
    critical_ela = []

    measured_thickness = []
    mean_thickness = []
    static_thickness = []

    for basin, data in BASINS.items():
        glacier.max_bed_height = data['bed_height']
        glacier.length = data['length_of_segment']
        glacier.slope = calc_slope(
            data['min_surface'], data['max_surface'], data['length_of_segment']
        )

        max_surfaces.append(data['max_surface'])
        ela.append(glacier.ela_from_length())
        critical_ela.append(glacier.critical_ela())

        measured_length.append(data['length_of_segment'] / 1000)
        linear_equilibrium_length.append(
            glacier.linear_equilibrium_length(
                ela[-1], thickness=data['mean_ice_thickness']
            ) / 1000
        )

        measured_thickness.append(data['mean_ice_thickness'])
        mean_thickness.append(glacier.mean_thickness())
        static_thickness.append(glacier.static_mean_thickness())

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(14, 6))
    x_axis = [1, 2, 3, 4]

    labels = dict(
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.4', fc='wheat', alpha=0.8)
    )

    ax1.scatter(x_axis, critical_ela, label='critical ELA', s=100)
    ax1.scatter(x_axis, ela, label='ELA from Length', marker='*', s=100)
    ax1.scatter(
        x_axis, max_surfaces, label='Max Surface Elevation', marker='+', s=100
    )
    ax1.set_title('Glacier ELA')
    ax1.set_ylabel('Elevation (Meters)')
    ax1.set_xticks([])
    ax1.legend()
    for label, x, y in zip(BASINS.keys(), x_axis, max_surfaces):
        ax1.annotate(label, xy=(x, y), xytext=(15, -30), **labels)

    ax2.scatter(
        x_axis, linear_equilibrium_length, label='Length Equilibrium', s=100
    )
    ax2.scatter(
        x_axis,
        measured_length,
        marker='+',
        label='Measured Length',
        color='g',
        s=100
    )
    ax2.set_title('Glacier Length')
    ax2.set_ylabel('Length (KM)')
    ax2.set_xticks([])
    ax2.legend()
    for label, x, y in zip(BASINS.keys(), x_axis, measured_length):
        ax2.annotate(label, xy=(x, y), xytext=(15, 20), **labels)

    ax3.scatter(
        x_axis, mean_thickness, label='Mean Thickness', s=100
    )
    ax3.scatter(
        x_axis,
        static_thickness,
        label='Static Thickness',
        marker='*',
        s=100
    )
    ax3.scatter(
        x_axis,
        measured_thickness,
        label='Measured Mean Thickness',
        marker='+',
        s=100
    )
    ax3.set_title('Glacier Thickness')
    ax3.set_ylabel('Thickness (Meters)')
    ax3.set_xticks([])
    ax3.legend()
    for label, x, y in zip(BASINS.keys(), x_axis, measured_thickness):
        ax3.annotate(label, xy=(x, y), xytext=(15, -30), **labels)

    fig.tight_layout()
    plt.show()

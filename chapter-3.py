# b_0 = 3900 m
# L_0 = 22000 m
# slope = 0.1
# dt = 1 year

# t_0: 0 to 90, change ELA every 10 years
# ELA = 2900, 3100, 2800, 2700, 3000, 2800, 3400, 3300, 3200, 3500
# Get to steady state length for ELA at 3500
# - How long is the glacier (length)
# - How long does it take to get there (time)

import math
import numpy as np
import matplotlib.pyplot as plt

from glacier import Glacier

if __name__ == '__main__':
    initial_length = 22000
    glacier = Glacier(max_bed_height=3900, length=initial_length, slope=0.1)
    elas = [2900, 3100, 2800, 2700, 3000, 2800, 3400, 3300, 3200, 3500]
    time = np.arange(0, 501, step=1)
    lengths = []
    ela_index = 0
    time_delta = 1

    e_folding = 1 / math.e
    e_year = None
    e_length = None

    for year in time:
        lengths.append(glacier.length_over_time(time_delta, elas[ela_index]))
        glacier.length = lengths[-1]

        if 1 < year < 99 and (year % 10 == 9):
            ela_index += 1
        elif e_folding and (1 - (lengths[-1] / initial_length)) > e_folding:
            e_year = year
            e_length = lengths[-1]
            e_folding = None

    plt.figure(figsize=(12, 8))
    plt.plot(time, lengths)
    plt.scatter(
        e_year, e_length, marker='+', s=300, color='orange', linewidth=5
    )
    plt.xlabel('Year')
    plt.ylabel('Length (m)')
    plt.annotate(
        'Steady State - Year: {0} - Length: {1:.2f}'.format(e_year, e_length),
        xy=(e_year, e_length),
        xytext=(240, -5), textcoords='offset points', ha='right', va='bottom'
    )
    plt.xlim(time.min(), time.max())
    plt.show()

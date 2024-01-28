import os

import matplotlib.pyplot as plt

from src.util import config
from src.util.data_util import parse_time


def hourly_plot(data, label, file):
    plt.clf()
    plt.close()
    plt.cla()
    time = [parse_time(e1) for e1, e2 in data]
    values = [e2 for e1, e2 in data]

    ticks = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
    labels = [str(round(i * 24)) + ':00' for i in ticks]

    fig, ax = plt.subplots()
    ax.set_xticklabels(labels)
    plt.plot(time, values)
    plt.xlabel('Time')
    plt.ylabel(label)
    plt.savefig(os.path.join(config.get_result_location(), file), dpi=300)

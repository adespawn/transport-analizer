import os
import datetime

from dateutil import parser
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.dates

import src.parser.analize_chunks.job as job
import src.util.config as config
from src.util.plots import hourly_plot


def time_plot_2(data):
    plt.clf()
    plt.close()
    plt.cla()
    time = [parser.parse(e1) for e1, e2 in data]
    values = [e2 for e1, e2 in data]
    plt.gcf().autofmt_xdate()
    fig, ax = plt.subplots()
    # ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=6))
    plt.plot(time, values)
    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.savefig(os.path.join(config.get_result_location(), 'daily_activity.png'), dpi=300)


class DailyActivity(job.Job):
    def __init__(self):
        super().__init__()
        self.hourly = {}
        self.daily = {}
        self.last_added_h = ()
        self.last_added_d = ()

    def do_job(self, chunk):
        super().do_job(chunk)
        if len(chunk['Time']) != 19:
            return
        current_hour = chunk['Time'].split(' ')[1][:-3]
        if self.last_added_h != (current_hour, chunk['VehicleNumber']):
            if current_hour not in self.hourly:
                self.hourly[current_hour] = 0
            self.hourly[current_hour] += 1
            self.last_added_h = (current_hour, chunk['VehicleNumber'])

        current_day_hour = chunk['Time'][:-3]

        if (self.last_added_d != (current_day_hour, chunk['VehicleNumber']) and
                '2023' not in current_day_hour):
            if current_day_hour not in self.daily:
                self.daily[current_day_hour] = 0
            self.daily[current_day_hour] += 1
            self.last_added_d = (current_day_hour, chunk['VehicleNumber'])

    def finish_job(self):
        super().finish_job()
        hourly_file = open(os.path.join(config.get_result_location(), 'hourly.txt'), 'w')
        daily_file = open(os.path.join(config.get_result_location(), 'daily.txt'), 'w')
        sorted_hourly = sorted(self.hourly.items())
        sorted_daily = sorted(self.daily.items())
        for hour in sorted_hourly:
            hourly_file.write(hour[0] + ', ' + str(hour[1]) + '\n')
        for day in sorted_daily:
            daily_file.write(day[0] + ', ' + str(day[1]) + '\n')
        hourly_file.close()
        daily_file.close()
        hourly_plot(sorted_hourly, 'Count', 'hourly_activity.png')
        time_plot_2(sorted_daily)


def get_job():
    my_job = DailyActivity()
    return my_job

import math

import pandas as pd
import plotly.express as px
import os

import src.parser.analize_chunks.job as job
import src.util.config as config


def draw_map(filename, label, radius):
    df = pd.read_csv(filename)

    fig = px.density_mapbox(df, lat='Lat', lon='Lon', z=label, radius=radius,
                            center=dict(lat=52.23, lon=21), zoom=10,
                            mapbox_style="open-street-map")
    fig.show()
    fig.write_html(os.path.join(config.get_result_location(), filename.split('.')[0] + '.html'))


def scale(value):
    return math.log(value, 10)


class MapJob(job.Job):
    def __init__(self, details, label, radius):
        super().__init__()
        self.file_name = os.path.join(config.get_result_location(), 'basic_map.txt')
        self.radius = radius
        self.details = details
        self.label = label
        self.scale_fun = scale
        self.map = {}

    def do_job(self, line):
        lon = line['Lon']
        lat = line['Lat']
        lon = round(lon, self.details)
        lat = round(lat, self.details)
        if self.map.get((lon, lat)) is None:
            self.map[(lon, lat)] = 0
        self.map[(lon, lat)] += 1

        pass

    def finish_job(self):
        file = open(self.file_name, 'w')
        file.write('Lon,Lat,' + self.label + '\n')
        for key, value in self.map.items():
            file.write(str(key[0]) + ',' + str(key[1]) + ',' + str(self.scale_fun(value)) + '\n')
        file.close()
        draw_map(self.file_name, self.label, self.radius)
        pass


def get_job():
    return MapJob(4, 'Count', 2)

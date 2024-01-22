import math
import os.path

import src.parser.map_jobs.basic_map_job as basic_map_job
from src.util.config import get_result_location


def scale(value):
    return math.log(value, 2)


class SpeedJob(basic_map_job.MapJob):
    def __init__(self, details, label, radius, speed):
        super().__init__(details, label, radius)
        self.speed = speed
        self.file_name = os.path.join(get_result_location(), 'speed_map.txt')
        self.scale_fun = scale

    def do_job(self, line):
        if 'speed' not in line or line['speed'] <= self.speed:
            return
        super().do_job(line)


def get_job():
    return SpeedJob(5, 'Count', 5, 65)

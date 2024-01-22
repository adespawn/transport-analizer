import os

from src.parser.analize_chunks import job
from src.parser.analize_chunks.job import Job
from src.util import config
from src.util.data_util import average_data
from src.util.plots import hourly_plot


class AverageSpeed(Job):
    def __init__(self, min_speed=0):
        super().__init__()
        self.speed_sum = {}
        self.speed_cnt = {}
        self.min_speed = min_speed
        pass

    def do_job(self, chunk):
        if 'speed' not in chunk or chunk['speed'] < self.min_speed:
            return
        super().do_job(chunk)
        if len(chunk['Time']) != 19:
            return
        current_hour = chunk['Time'].split(' ')[1][:-3]
        if self.speed_sum.get(current_hour) is None:
            self.speed_sum[current_hour] = 0
            self.speed_cnt[current_hour] = 0
        self.speed_sum[current_hour] += chunk['speed']
        self.speed_cnt[current_hour] += 1
        pass

    def finish_job(self):
        super().finish_job()
        result = []
        sorted_keys = sorted(self.speed_sum.keys())
        file = open(os.path.join(config.get_result_location(), f'avg_speed_{str(self.min_speed)}.txt'), 'w')
        for key in sorted_keys:
            avg_speed = self.speed_sum[key] / self.speed_cnt[key]
            result.append((key, avg_speed))
            file.write(str(key) + ', ' + str(avg_speed) + '\n')
        file.close()
        hourly_plot(average_data(result, 30), 'speed',
                    os.path.join(config.get_result_location(), f'avg_speed_{str(self.min_speed)}.jpg'))
        pass


def add_jobs(job_scheduler: job.JobScheduler) -> job.JobScheduler:
    job_scheduler.register_job(AverageSpeed())
    job_scheduler.register_job(AverageSpeed(min_speed=5))
    return job_scheduler

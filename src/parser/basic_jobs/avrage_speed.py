import os

from src.parser.analize_chunks import job
from src.parser.analize_chunks.job import Job
from src.parser.basic_jobs.average_job import AverageJob
from src.util import config
from src.util.data_util import average_data
from src.util.plots import hourly_plot


class AverageSpeed(AverageJob):
    def __init__(self, min_speed: int = 0):
        super().__init__(f'avg_speed_{str(min_speed)}')
        self.min_speed = min_speed
        pass

    def do_job(self, chunk):
        if 'speed' not in chunk or chunk['speed'] < self.min_speed:
            return
        super().do_job(chunk)
        if len(chunk['Time']) != 19:
            return
        current_hour = chunk['Time'].split(' ')[1][:-3]
        self.add_value(current_hour, chunk['speed'])
        pass

    def finish_job(self):
        result = super().finish_job()
        hourly_plot(average_data(result, 30), 'speed',
                    os.path.join(config.get_result_location(), f'avg_speed_{str(self.min_speed)}.jpg'))
        pass


def add_jobs(job_scheduler: job.JobScheduler) -> job.JobScheduler:
    job_scheduler.register_job(AverageSpeed())
    job_scheduler.register_job(AverageSpeed(min_speed=5))
    return job_scheduler

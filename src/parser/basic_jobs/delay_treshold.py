import os

from src.parser.analize_chunks import job
from src.parser.basic_jobs.average_job import AverageJob
from src.util import config
from src.util.data_util import average_data, valid_hour
from src.util.plots import hourly_plot


class DelayThreshold(AverageJob):
    def __init__(self, minutes: int):
        super().__init__(f'delay_over_{minutes}')
        self.minutes = minutes
        pass

    def do_job(self, chunk):
        pass

    def schedule_job(self, chunk):
        # if 'delay' not in chunk:
        #     return
        current_time = valid_hour(chunk)
        val = 0
        if 'delay' in chunk and self.minutes * 60 < chunk['delay'] < 60 * 60:
            val = 1
        self.add_value(current_time, val)

    def finish_job(self):
        result = super().finish_job()
        hourly_plot(average_data(result, 30), f'Delay (over {self.minutes} minutes)',
                    os.path.join(config.get_result_location(), f'delay_over_{self.minutes}.jpg'))
        pass


def add_jobs(job_scheduler: job.JobScheduler) -> job.JobScheduler:
    job_scheduler.register_job(DelayThreshold(5))
    return job_scheduler

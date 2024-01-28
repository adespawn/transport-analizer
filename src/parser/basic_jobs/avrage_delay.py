import os

from src.parser.analize_chunks import job
from src.parser.basic_jobs.average_job import AverageJob
from src.util import config
from src.util.data_util import average_data, valid_hour
from src.util.plots import hourly_plot


class AverageDelay(AverageJob):
    def __init__(self):
        super().__init__('avg_delay')
        pass

    def do_job(self, chunk):
        pass

    def schedule_job(self, chunk):
        if 'delay' not in chunk:
            return
        if chunk['delay'] > 60 * 60:
            return
        current_time = valid_hour(chunk)
        self.add_value(current_time, chunk['delay'] / 60)

    def finish_job(self):
        result = super().finish_job()
        hourly_plot(average_data(result, 30), 'Delay (min)',
                    os.path.join(config.get_result_location(), f'avg_delay.jpg'))
        pass


def add_jobs(job_scheduler: job.JobScheduler) -> job.JobScheduler:
    job_scheduler.register_job(AverageDelay())
    return job_scheduler

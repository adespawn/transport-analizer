import src.parser.analize_chunks.job as job
import src.parser.basic_jobs.daily_activity as daily_activity
from src.parser.basic_jobs import avrage_speed, avrage_delay, delay_treshold


def add_jobs(job_scheduler: job.JobScheduler) -> job.JobScheduler:
    job_scheduler.register_job(daily_activity.get_job())
    job_scheduler = avrage_speed.add_jobs(job_scheduler)
    job_scheduler = avrage_delay.add_jobs(job_scheduler)
    job_scheduler = delay_treshold.add_jobs(job_scheduler)
    return job_scheduler

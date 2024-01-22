import src.parser.analize_chunks.job as job
import src.parser.map_jobs.basic_map_job as basic_map_job
import src.parser.map_jobs.speed_job as speed_job


def add_jobs(job_scheduler: job.JobScheduler) -> job.JobScheduler:
    job_scheduler.register_job(basic_map_job.get_job())
    job_scheduler.register_job(speed_job.get_job())
    return job_scheduler

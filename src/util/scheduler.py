import src.parser.main as parser
import src.parser.analize_chunks.job as job
import src.parser.basic_jobs.main as basic_jobs
import src.parser.analize_chunks.filter as filters
import src.parser.analize_chunks.main as job_worker
import src.parser.map_jobs.main as map_jobs


def scheduler(args):
    if args.full or args.prepare:
        parser.parse()

    jobs = job.JobScheduler()
    chunk_filter = filters.full_fileter()

    if args.full or args.initial:
        jobs = basic_jobs.add_jobs(jobs)

    if args.full or args.map:
        jobs = map_jobs.add_jobs(jobs)

    job_worker.do_jobs(jobs, chunk_filter)
    pass

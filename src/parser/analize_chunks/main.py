import src.parser.analize_chunks.job as job
import src.parser.analize_chunks.chunks as chunks


def do_jobs(jobs: job.JobScheduler, chunk_filter):
    chunk_mng = chunks.ChunksParser(chunk_filter)
    while True:
        chunk: chunks.Chunk | None = chunk_mng.next_chunk()
        if chunk is None:
            break
        chunk.do_jobs(jobs)

    jobs.next_cycle()
    while True:
        next_job = jobs.get_next_job()
        if next_job is None:
            break
        next_job.finish_job()



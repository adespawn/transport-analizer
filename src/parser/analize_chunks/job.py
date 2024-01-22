class Job:
    def __init__(self):
        pass

    def do_job(self, chunk):
        pass

    def finish_job(self):
        pass


class JobScheduler:

    def __init__(self):
        self.registered_job = []
        self.current_id = 0

    def register_job(self, job):
        self.registered_job.append(job)

    def get_next_job(self) -> Job | None:
        if len(self.registered_job) == self.current_id:
            return None
        ret = self.registered_job[self.current_id]
        self.current_id += 1
        return ret

    def next_cycle(self):
        self.current_id = 0

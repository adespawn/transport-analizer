import json
import os

import src.parser.analize_chunks.filter as filters
import src.parser.analize_chunks.job as jobs
import src.util.config as config


class Chunk:
    def __init__(self, name):
        self.lines = []
        self.file = open(os.path.join(config.get_data_location(), 'locations_chunks', name), 'r')

    def next_line(self):
        return self.file.readline()

    def do_jobs(self, tasks: jobs.JobScheduler):
        while True:
            tasks.next_cycle()
            line = self.next_line()
            if not line:
                break
            self.lines.append(line)

        while True:
            job: jobs.Job = tasks.get_next_job()
            if job is None:
                break
            for line in self.lines:
                job.do_job(json.loads(line))
        self.lines = []


class ChunksParser:
    def __init__(self, my_filter: filters.Filter):
        self.filter = my_filter
        self.chunks = open(os.path.join(config.get_data_location(), 'locations_chunks/list'), 'r')

    def next_chunk(self):
        line = self.chunks.readline()
        if not line:
            return None
        line = line.replace('\n', '')
        vehicle = {'VehicleNumber': line.split('_')[0], 'Lines': line.split('_')[1]}
        if not self.filter.filter(vehicle):
            return self.next_chunk()
        chunk = Chunk(line)
        return chunk

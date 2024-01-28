import json
import os

import src.parser.analize_chunks.filter as filters
import src.parser.analize_chunks.job as jobs
import src.util.config as config


class Chunk:
    def __init__(self, name):
        self.name = name
        self.lines = []
        self.schedule = []
        self.file = open(os.path.join(config.get_data_location(), 'locations_chunks', name), 'r')
        self.file_sch = open(os.path.join(config.get_data_location(), 'vehicle_expected', name), 'r')

    def do_jobs(self, tasks: jobs.JobScheduler):
        tasks.next_cycle()
        while True:
            line = self.file.readline()
            if not line:
                break
            self.lines.append(json.loads(line))

        while True:
            line = self.file_sch.readline()
            if not line:
                break
            self.schedule.append(json.loads(line))

        while True:
            job: jobs.Job = tasks.get_next_job()
            if job is None:
                break
            for line in self.lines:
                try:
                    job.do_job(line)
                except Exception as e:
                    pass
            for line in self.schedule:
                try:
                    job.schedule_job(line)
                except Exception as e:
                    pass
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

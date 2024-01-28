import os

from src.parser.analize_chunks.job import Job
from src.util import config


class AverageJob(Job):

    def __init__(self, name):
        super().__init__()
        self.res_name = name
        self.val_sum = {}
        self.val_cnt = {}

    def add_value(self, key, value):
        if self.val_sum.get(key) is None:
            self.val_sum[key] = 0
            self.val_cnt[key] = 0
        self.val_sum[key] += value
        self.val_cnt[key] += 1

    def finish_job(self):
        super().finish_job()
        result = []
        sorted_keys = sorted(self.val_sum.keys())
        file = open(os.path.join(config.get_result_location(), f'{self.res_name}.txt'), 'w')
        for key in sorted_keys:
            avg_value = self.val_sum[key] / self.val_cnt[key]
            result.append((key, avg_value))
            file.write(str(key) + ', ' + str(avg_value) + '\n')
        file.close()
        return result

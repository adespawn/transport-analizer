import json
import os

import src.util.config as config


class Reader:
    def __init__(self, file):
        self.file = open(os.path.join(config.get_data_location(), file), 'r')

    def get_next_line(self):
        line = self.file.readline()
        if not line:
            return line
        data = json.loads(line)
        return data

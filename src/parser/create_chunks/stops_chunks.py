from dateutil import parser
import json
import os
from datetime import datetime

from src.util import config


def chunk_desc(line):
    return line['line'] + '_' + line['stopID'] + '_' + line['stopCount']


def get_date(line):
    date = datetime.fromtimestamp(line['checkID'])
    date_str = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    return date_str


class SingleChunk:
    def __init__(self, name):
        self.name = name
        self.file_name = os.path.join(config.get_data_location(), 'expected_chunks', name)
        self.file = open(self.file_name, 'w+')
        self.all_entry = {}

    def add_line(self, line):
        self.file.write(json.dumps(line) + '\n')


class Chunks:
    def __init__(self):
        self.chunks = {}
        loc_file = open(os.path.join(config.get_data_location(), 'locations.json'), 'r')
        data = json.loads(loc_file.readline())
        self.stops_locations = {}
        for element in data['result']:
            valid_element = {}
            for chunk in element['values']:
                valid_element[chunk['key']] = chunk['value']
            desc = valid_element['zespol'] + '_' + valid_element['slupek']
            self.stops_locations[desc] = valid_element

    def add_line(self, line):
        date = get_date(line)
        stop_id = line['stopID']
        stop_count = line['stopCount']
        line_nr = line['line']
        for entry in line['result']:
            entry['stopID'] = stop_id
            entry['stopCount'] = stop_count
            entry['line'] = line_nr
            entry['Time'] = date + ' ' + entry['czas']
            entry.pop('czas')
            loc = self.stops_locations[stop_id + '_' + stop_count]
            entry['Lat'] = float(loc['szer_geo'])
            entry['Lon'] = float(loc['dlug_geo'])
            entry['stop_name'] = loc['nazwa_zespolu']
            desc = line_nr + '_' + entry['brygada']
            if not self.chunks.__contains__(desc):
                self.chunks[desc] = SingleChunk(desc)
            self.chunks[desc].add_line(entry)

    def cleanup(self):
        file = open(os.path.join(config.get_data_location(), 'expected_chunks', 'list'), 'w+')
        for chunk in self.chunks.keys():
            file.write(chunk + '\n')

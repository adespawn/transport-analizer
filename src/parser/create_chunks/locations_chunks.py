from dateutil import parser
import haversine
import json
import os

import src.util.config as config
from src.util.data_util import parse_time

base_distance: int = 600


def get_time_diff(line, previous):
    current_time, skip_day_c = valid_time(line['Time'])
    previous_time, skip_day_p = valid_time(previous['Time'])
    current_time = parse_time(current_time)
    previous_time = parse_time(previous_time)
    val = (current_time - previous_time).total_seconds() + (skip_day_c - skip_day_p) * 60
    return val


def get_location_diff(line, previous):
    loc1 = (line['Lon'], line['Lat'])
    loc2 = (previous['Lon'], previous['Lat'])
    distance = haversine.haversine(loc1, loc2, unit='m')
    return distance


def get_speed(line, previous):
    time = get_time_diff(line, previous)
    distance = get_location_diff(line, previous)
    speed = distance / time  # in m / s
    speed = speed * 3.6

    if speed > 160:
        raise AttributeError("Speed too high")
    return speed


def valid_time(time):
    hour = time.split(' ')[1].split(':')[0]
    add_day = 0
    if int(hour) >= 24:
        hour = int(hour) - 24
        add_day = 60 * 24

    new_time = time.split(' ')[0] + ' ' + str(hour) + ':' + time.split(':', 1)[1]
    return new_time, add_day


def minute_stamp(time):
    new_time, add_day = valid_time(time)
    return round(parse_time(new_time).timestamp() / 60) + add_day


class SingleChunk:
    def __init__(self, name):
        self.name = name
        self.file_name = os.path.join(config.get_data_location(), 'locations_chunks', name)
        # self.mid_file = open(os.path.join(config.get_data_location(), 'to_check', name), 'w')
        # self.on_time_res = open(os.path.join(config.get_data_location(), 'vehicle_expected', name), 'w')
        self.file = open(self.file_name, 'w+')
        self.all_entry = {}
        self.check_lines = set()
        self.my_timestamps = {}
        self.schedule = []
        self.current_schedule = []
        self.schedule_index = 0

    def add_line(self, line):
        self.file.write(json.dumps(line) + '\n')
        self.check_lines.add(line["Lines"] + '_' + line['Brigade'])

    # def finish_request(self):
    #     request_file = open(os.path.join(config.get_data_location(), 'to_check', self.name), 'w')
    #     for request in self.check_lines:
    #         request_file.write(request + '\n')

    def load_data(self):
        self.file.close()
        self.file = open(self.file_name, 'r')
        while True:
            try:
                line = self.file.readline()
                if not line or line == '\n':
                    break
                line = json.loads(line)
                line['_id'] = line['_id']['$oid']
                self.all_entry[line['Time']] = line
                desc = line['Lines'] + '_' + line['Brigade']
                if not self.my_timestamps.__contains__(desc):
                    self.my_timestamps[desc] = set()
                self.my_timestamps[desc].add(minute_stamp(line['Time']))
            except Exception:
                pass
        self.file.close()

    def cleanup(self):
        with open(os.path.join(config.get_data_location(), 'vehicle_expected', self.name), 'w') as self.on_time_res:
            self.load_data()
            self.file = open(self.file_name, 'w')
            step = sorted(self.all_entry.keys())
            last_entry = None
            for entry in self.check_lines:
                self.try_single_line(entry)
            for entry in step:
                line = self.enhance(entry, last_entry)
                self.add_line(line)
                last_entry = entry

            for entry in self.current_schedule:
                self.on_time_res.write(json.dumps(entry) + '\n')
            self.all_entry = None
            self.schedule = None
            self.current_schedule = None

    def enhance(self, line, previous):
        try:
            line = self.all_entry[line]
            self.add_expected_stops(minute_stamp(line['Time']))
            self.update_expected_stops(line)
            valid = False
            if previous:
                valid = True
                previous = self.all_entry[previous]
            if valid is True and get_time_diff(line, previous) <= 60:
                line['last'] = previous['_id']
                line['speed'] = get_speed(line, previous)
        except Exception as e:
            line['last'] = None
            line['speed'] = 0
            if not isinstance(e, AttributeError):
                print(e.with_traceback)
        return line

    def add_expected_stops(self, my_time):
        while self.schedule_index < len(self.schedule):
            element = self.schedule[self.schedule_index]
            if element[0] - 5 > my_time:
                break
            self.schedule_index += 1
            element[1]['reached'] = False
            element[1]['min_distance'] = base_distance
            self.current_schedule.append(element[1])

    def update_expected_stops(self, line):
        for i in range(len(self.current_schedule)):
            try:
                element = self.current_schedule[i]
                distance = get_location_diff(element, line)
                time_diff = get_time_diff(line, element)
                if (element['reached'] is True and distance > base_distance) or time_diff > 60 * 60:
                    self.on_time_res.write(json.dumps(element) + '\n')
                    self.current_schedule.pop(i)
                    i -= 1
                    continue
                if distance < element['min_distance']:
                    element['reached'] = True
                    element['min_distance'] = distance
                    element['time_reached'] = line['Time']
                    element['delay'] = time_diff

                self.current_schedule[i] = element
            except IndexError:
                pass
        pass

    def try_single_line(self, line_schedule):
        file_name = os.path.join(config.get_data_location(), 'expected_chunks', line_schedule)
        try:
            open(file_name, 'x').close()
        except Exception:
            pass
        with open(file_name, 'r') as schedule_file:
            added = set()
            while True:
                line_t = schedule_file.readline()
                if not line_t or line_t == '\n':
                    break
                line = json.loads(line_t)
                time = minute_stamp(line['Time'])
                is_valid = False
                if line['line'] == '1' and line['brygada'] == '1':
                    pass
                for i in range(-2, 3):
                    if time + i in self.my_timestamps[line_schedule]:
                        is_valid = True
                if is_valid and line_t not in added:
                    added.add(line_t)
                    self.schedule.append((time, line))
            self.schedule.sort(key=lambda x: x[0])


def chunk_desc(line):
    return line['VehicleNumber'] + '_' + line['Lines']


class Chunks:
    def __init__(self):
        self.chunks = {}

    def add_line(self, line):
        if not self.chunks.__contains__(chunk_desc(line)):
            self.chunks[chunk_desc(line)] = SingleChunk(chunk_desc(line))
        self.chunks[chunk_desc(line)].add_line(line)

    def cleanup(self):
        file = open(os.path.join(config.get_data_location(), 'locations_chunks', 'list'), 'w+')
        for chunk in self.chunks.keys():
            file.write(chunk + '\n')
            self.chunks[chunk].cleanup()

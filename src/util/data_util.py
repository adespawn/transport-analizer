from dateutil import parser

cache = {}


def average_data(data, count):
    prefix = [0]
    for i in data:
        last = prefix[len(prefix) - 1]
        prefix.append(last + i[1])
    avg_data = []
    for i in range(len(data)):
        data_ind = max(count, i + 1)
        avg_data.append((data[i][0], (prefix[data_ind] - prefix[data_ind - count]) / count))
    return avg_data


def parse_time(time):
    if time not in cache:
        cache[time] = parser.parse(time)
    return cache[time]


def valid_hour(chunk):
    current_hour = chunk['Time'].split(' ')[1].split(':')[0]
    current_min = chunk['Time'].split(' ')[1].split(':')[1]
    if int(current_hour) >= 24:
        current_hour = str(int(current_hour) - 24)
        if len(current_hour) == 1:
            current_hour = '0' + current_hour
    current_time = current_hour + ':' + current_min
    return current_time

def average_data(data, count):
    prefix = [0]
    for i in data:
        last = prefix[len(prefix) - 1]
        prefix.append(last + i[1])
    avg_data = []
    for i in range(len(data)):
        data_ind = max(count, i + 1)
        avg_data.append((data[i][0], (prefix[data_ind] - prefix[data_ind - count])/count))
    return avg_data

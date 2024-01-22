class Filter:
    def __init__(self, filter_type, val1):
        self.type = filter_type
        self.val1 = val1
        pass

    def filter(self, match):
        if self.type == 0:
            return True
        if self.type == 1:
            return match['VehicleNumber'] == self.val1
        if self.type == 2:
            return match['Lines'] == self.val1
        return False
        pass


def full_fileter():
    return Filter(0, None)


def line_filer(line):
    return Filter(1, line)


def vehicle_filer(vehicle):
    return Filter(2, vehicle)

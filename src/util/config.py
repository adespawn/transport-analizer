import os.path


def get_data_location():
    return os.path.join(os.getcwd(), 'data')


def get_result_location():
    return os.path.join(os.getcwd(), 'res')

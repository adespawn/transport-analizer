import logging

import src.parser.create_chunks.reader as locations
import src.parser.create_chunks.locations_chunks as location_chunks
from src.parser.create_chunks import stops_chunks


def create_location_chunks():
    data = locations.Reader('localization.json')
    chunks = location_chunks.Chunks()
    while True:
        line = data.get_next_line()
        if not line:
            break
        chunks.add_line(line)
    logging.info('Vehicle chunks: Read. Starting cleanup')
    chunks.cleanup()


def expected_locations_chunks():
    data = locations.Reader('schedule.json')
    chunks = stops_chunks.Chunks()
    while True:
        line = data.get_next_line()
        if not line:
            break
        chunks.add_line(line)
    chunks.cleanup()


def create_chunks():
    logging.info('Creating stops chunks...')
    expected_locations_chunks()
    logging.info('Creating vehicle chunks...')
    create_location_chunks()


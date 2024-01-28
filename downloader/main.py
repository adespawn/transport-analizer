import pymongo
from threading import Timer
import requests
import json
import time
from datetime import datetime

uri = "mongodb://root:HASŁO_DO_BAZY_DANYCH@localhost:27020"
rootUrl = "https://api.um.warszawa.pl/api/action"
apiKey = "KLUCZ_API"

myClient = pymongo.MongoClient(uri)

warsawDB = myClient["Warszawa"]
localizationC = warsawDB["localization"]
scheduleC = warsawDB["schedule"]
routesC = warsawDB["routes"]

background_tasks = set()


def log(msg):
    log_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{log_time}]: {msg}")


def get_jsoned_url(url, repeat=5):
    try:
        time.sleep(0.2)  # To avoid spamming the server
        data = requests.get(url).text
        json_data = json.loads(data)['result']
        return json_data
    except Exception:
        if repeat > 0:
            return get_jsoned_url(url, repeat - 1)


# Download schedule data for pair (line, stop)
def get_stop_schedule(id, line, stop_id, stop_count):
    try:
        stop_data = {'checkID': id, 'line': line,
                    'stopID': stop_id, 'stopCount': stop_count}
        stop_info = get_jsoned_url(
            f"{rootUrl}/dbtimetable_get/?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238" +
            f"&busstopId={stop_id}&busstopNr={stop_count}&line={line}&apikey={apiKey}")
        if len(stop_info) == 0:
            return
        for i in range(len(stop_info)):
            old_obj = stop_info[i]
            new_obj = {}
            for entry in old_obj["values"]:
                new_obj[entry['key']] = entry['value']
            stop_info[i] = new_obj
        stop_data["result"] = stop_info
        scheduleC.insert_one(stop_data)
    except Exception as error:
        log(
            f"Got error in getting stop schedule (id: {id}," +
            f"line: {line}, stopId:{stop_id}, stopCount:{stop_count}):\n{str(error)}")
    return


# Download all the lines routes and download the schedule for all the stops


def get_schedule():
    try:
        id = int(datetime.today().timestamp())
        log(f"Started getting schedule (id: {id})")
        all_routes = get_jsoned_url(
            f"{rootUrl}/public_transport_routes/?apikey={apiKey}")
        routes_obj = {"id": str(id), "routes": all_routes}
        routesC.insert_one(routes_obj)

        checked = dict()

        for i in all_routes:
            for j in all_routes[i]:
                for k in all_routes[i][j]:
                    stop = all_routes[i][j][k]
                    unique_stop = (i, stop['nr_zespolu'], stop['nr_przystanku'])
                    if unique_stop in checked:
                        continue
                    get_stop_schedule(
                        id, i, stop['nr_zespolu'], stop['nr_przystanku'])
        log(f"Finished getting schedule (id: {id})")
    except Exception as error:
        log(f"Got error in getting schedule (id: {id}):\n{str(error)}")
    return


async def async_database(find, insert):
    try:
        exists = localizationC.count_documents(find)
        if exists == 0:
            localizationC.insert_one(insert)
    except Exception as error:
        log(f"Got error in inserting into DB:\n{error.with_traceback}")


def get_locations(type):
    try:
        url = (f"{rootUrl}/busestrams_get/?resource_id=20f2e5503e-927d-4ad3-9500-4ab9e55deb59"
               + f"&apikey={apiKey}&type={str(type)}")
        data = get_jsoned_url(url, 3)
        localizationC.insert_many(data)
        log(f"Successfully got location data type {type}")
    except Exception as error:
        log(f"Got error in getting locations:\n{str(error)}")


def schedule_loop():
    try:
        Timer(1.0, get_schedule).start()
    except Exception as error:
        log(f"Error in the main loop:\n{str(error)}")
    finally:
        # Run the schedule loop every day
        Timer(60.0 * 60.0 * 24.0, schedule_loop).start()
    return


def location_loop():
    try:
        Timer(0.2, get_locations, [1]).start()
        Timer(0.8, get_locations, [2]).start()
    except Exception as error:
        log(f"Error in the main loop:\n{str(error)}")
    finally:
        Timer(6.0, location_loop).start()


def main():
    Timer(0.1, location_loop).start()
    Timer(60.0 * 60.0, schedule_loop).start()


# asyncio.run(main())
if __name__ == "__main__":
    main()

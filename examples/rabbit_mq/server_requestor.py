import csv
import requests
import time
from requests.auth import HTTPBasicAuth


def dump_periodic_data(has_to_finish, interval: int):
    guest_auth = HTTPBasicAuth("guest", "guest")
    header = ["Time", "QueueMessages"]

    with open("rabbit_server_load.csv", "w", encoding="UTF8") as file:
        wrt = csv.writer(file)
        wrt.writerow(header)
        i = 0

        while not has_to_finish():
            response = requests.get("http://localhost:15672/api/queues", auth=guest_auth).json()

            if len(response) > 0:
                queue = response[0]
                if "messages" in queue:
                    msg_number = queue["messages"]
                    wrt.writerow([i * interval, msg_number])
                else:
                    wrt.writerow([i * interval, 0])
            else:
                wrt.writerow([i * interval, 0])

            i += 1
            time.sleep(interval)

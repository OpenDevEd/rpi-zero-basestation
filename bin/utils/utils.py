import os
import csv
import sys

sys.path.append("../")
import config
from datetime import datetime


def is_folder_exists_and_create(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def is_log_path_exists_and_create(log_path):
    # split the path into a list
    path_list = log_path.split("/")
    # current path
    path = ""
    # loop through the list and add the path to the current path after checking if it exists
    for folder in path_list:
        path = path + folder + "/"
        is_folder_exists_and_create(path)


def is_log_path_time_exists_and_create(log_path):
    # split the path into a list
    # create date time folder DD-MM-YYYY /hour
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d")
    hour = now.strftime("%H")
    is_log_path_exists_and_create(log_path + "/" + date_time + "/" + hour)
    return log_path + "/" + date_time + "/" + hour + "/"


def print_output(result, message, do_print, log):
    if result["error"] == "NO_ERROR":
        # check if it json if so print it pretty
        if do_print:
            if isinstance(result["data"], dict):
                print(f"{message}:")
                for key, value in result["data"].items():
                    print(f"    {key}: {value}")
            else:
                # if data is empty prunt no data
                if result["data"] is None or result["data"] == "":
                    print(f"{message}: no data")
                else:
                    print(f'{message}: {result["data"]}')
        if log:
            if isinstance(result["data"], dict):
                res = {}
                for key, value in result["data"].items():
                    res[key] = value
                return res

    else:
        print(f'Error getting {message}: {result["error"]}')


def update_csv_with_json(csv_file, additional_data):
    path = is_log_path_time_exists_and_create(config.LOG_PATH)
    now = datetime.now()
    csv_file = f"{path}{csv_file}-{config.ID}-{now.strftime('%Y-%m-%d')}-{now.hour}.csv"
    existing_data = []
    updated_data = []
    if os.path.isfile(csv_file):
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)
    if type(additional_data) == list:
        for row in additional_data:
            row["time_created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data = existing_data + additional_data
    elif type(additional_data) == dict:
        additional_data["time_created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data = existing_data
        updated_data.append(additional_data)

    unique_keys = []
    for key_set in updated_data:
        for key in key_set.keys():
            if key not in unique_keys:
                unique_keys.append(key)
    new_data = []
    new_unique_keys = []
    for key in updated_data:
        spic_data = {}
        for v in key:
            if type(key[v]) == dict:
                for k, t in key[v].items():
                    new_key = f"{v}::{k}"
                    spic_data[new_key] = t
                    if new_key not in new_unique_keys:
                        new_unique_keys.append(new_key)
            else:
                if v not in new_unique_keys:
                    new_unique_keys.append(v)
                spic_data[v] = key[v]
        new_data.append(spic_data)
    headers = list(new_unique_keys)
    with open(csv_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(new_data)

    print(
        f"CSV file '{csv_file}' updated successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} !"
    )

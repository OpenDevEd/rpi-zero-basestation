import os
import csv
import sys
import os
import pathlib
import json


import config
from datetime import datetime, timezone
import requests


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
    csv_file = f"{path}{csv_file}-{config.ID}_{now.strftime('%Y-%m-%d')}_{now.hour}.csv"
    existing_data = []
    updated_data = []

    if os.path.isfile(csv_file):
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)
            # check if the file is empty

    if type(additional_data) == list:
        for row in additional_data:
            # convert datetime to iso-8601 format with timezone 2023-07-08T22:02:40+01:00 not 2023-07-19T14:27:04.096051+00:00
            # change z for +00:00
            dt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
            dt = dt[:-2] + ":" + dt[-2:]
            row["time_created"] = dt

        updated_data = existing_data + additional_data
    elif type(additional_data) == dict:
        dt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
        dt = dt[:-2] + ":" + dt[-2:]
        additional_data["time_created"] = dt
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


def get_all_subfolders(path, extention=""):
    subfolders = []
    files = []
    try:
        for f in os.scandir(path):
            if f.is_dir():
                subfolders.append(f.path)
                res = get_all_subfolders(f.path)
                subfolders.extend(res[0])
                files.extend(res[1])
            else:
                if pathlib.Path(f.path).suffix == extention or extention == "":
                    files.append(f.path)
    except PermissionError:
        pass
    except:
        pass
    # return subfolders and files
    return [subfolders, files]


def upload_file_to_api(url, file_path):
    # Open the file and read its contents
    with open(file_path, "rb") as file:
        file_contents = file.read()
    # Set the request headers
    # Convert the bytes object to a string
    file_path = file_path.replace(config.LOG_PATH, "logs")
    file_contents_str = file_contents.decode("utf-8")

    # Set the request headers
    headers = {"Content-Type": "application/json"}
    body = json.dumps({"fileName": file_path, "body": file_contents_str})

    # Send the file contents in the request body
    response = requests.post(url, headers=headers, data=body)

    # Check the response status code
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error uploading file: {response.text}")


def upload_logs_files_to_api(url, folder_path):
    # get all files in the folder
    files = get_all_subfolders(folder_path)[1]

    # loop through the files and upload them
    for file in files:
        upload_file_to_api(url, file)

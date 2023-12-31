import sys

sys.path.append("../utils/")
sys.path.append("../")
import utils
import db
from datetime import datetime, timezone

import config


def get_date_time():
    dt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    dt = dt[:-2] + ":" + dt[-2:]
    return dt


def get_file_name(file_path):
    dt = get_date_time()
    return file_path + "_" + dt + ".csv"


def chunk_and_send(table_name, file_path):
    # get last row in data_transmission table
    last_row = db.db_last_row_data_transmission()
    datalogs_length = db.db_get_dataLogs_length()
    if datalogs_length == 0:
        print("No data to send")
    if last_row is None:
        if datalogs_length <= config.DATA_CHUNK_SIZE:
            row_id = db.db_data_transmission_create(0, datalogs_length, "in progress")
            file_name = get_file_name(file_path)

            try:
                db.db_data_to_csv(
                    table_name, file_name, 0, datalogs_length, "sensor_test"
                )
                utils.upload_file_to_api(config.SERVER_URL, file_name)
            except:
                print("Failed to send data on last row is None and data length < 100")
                db.db_data_transmission_update(row_id, "failed")
            db.db_data_transmission_update(row_id, "done")
        else:
            for i in range(0, datalogs_length, config.DATA_CHUNK_SIZE):
                to_id = min(i + config.DATA_CHUNK_SIZE, datalogs_length)
                row_id = db.db_data_transmission_create(i, to_id, "in progress")
                file_name = get_file_name(file_path)
                try:
                    db.db_data_to_csv(
                        table_name,
                        file_name,
                        i,
                        to_id,
                        "sensor_test",
                    )
                    utils.upload_file_to_api(config.SERVER_URL, file_name)
                except:
                    print(
                        "Failed to send data on last row is None and data length > 100"
                    )
                    db.db_data_transmission_update(row_id, "failed")
                db.db_data_transmission_update(row_id, "done")
    else:
        # continue from last row
        if last_row.to_id >= datalogs_length and last_row.status == "done":
            print("No data to send")
        # check if last row  to_id is less than datalogs_length and data_chunk_size
        elif (
            last_row.to_id < datalogs_length
            and last_row.to_id + config.DATA_CHUNK_SIZE >= datalogs_length
        ):
            row_id = db.db_data_transmission_create(
                last_row.to_id, datalogs_length, "in progress"
            )
            file_name = get_file_name(file_path)

            try:
                db.db_data_to_csv(
                    table_name,
                    file_name,
                    last_row.to_id,
                    datalogs_length,
                    "sensor_test",
                )
                utils.upload_file_to_api(config.SERVER_URL, file_name)
            except:
                print(
                    "Failed to send data on last row is not None and data length < 100"
                )
                db.db_data_transmission_update(row_id, "failed")
            db.db_data_transmission_update(row_id, "done")
        # check if last row  to_id is less than datalogs_length and data_chunk_size
        elif (
            last_row.to_id < datalogs_length
            and last_row.to_id + config.DATA_CHUNK_SIZE < datalogs_length
        ):
            for i in range(last_row.to_id, datalogs_length, config.DATA_CHUNK_SIZE):
                to_id = min(i + config.DATA_CHUNK_SIZE, datalogs_length)
                row_id = db.db_data_transmission_create(i, to_id, "in progress")
                file_name = get_file_name(file_path)

                try:
                    db.db_data_to_csv(
                        table_name,
                        file_name,
                        i,
                        to_id,
                        "sensor_test",
                    )
                    utils.upload_file_to_api(config.SERVER_URL, file_name)
                except:
                    print(
                        "Failed to send data on last row is not None and data length > 100"
                    )
                    db.db_data_transmission_update(row_id, "failed")
                db.db_data_transmission_update(row_id, "done")
        else:
            print("No data to send")


# send logs to server

# chunk_and_send("dataLogs", "dataLogs")



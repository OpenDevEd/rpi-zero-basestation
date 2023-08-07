import paho.mqtt.client as mqtt
import json
import csv
import os
from datetime import datetime
import sys

sys.path.append("../utils")
import utils
import db


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    topic = msg.topic
    #
    # print(msg.payload.decode('utf-8'))
    # check if it array if yes pass it
    save_data(topic, payload)


def save_data(topic, data):
    try:
        topic = topic.strip().split("/")
        topic = topic[1]
        if topic != "bridge":
            data = json.loads(data)
            data["topic"] = topic

            db.db_data_log_create("zigbee", data, "json")
            # TODO: convert to config
            db.db_data_event_create(
                "Data Logging",
                "Success",
                "Sensor Reading",
                "Zigbee sensor reading",
                "Zigbee",
            )
    except:
        print("unknown error")
        db.db_data_event_create(
            "Data Logging",
            "Failure",
            "Sensor Reading",
            "Zigbee sensor reading",
            "Zigbee",
        )


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()

import paho.mqtt.client as mqtt
import json
import csv
import os
from datetime import datetime
import utils.utils as utils


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
            print(f"{topic}:")
            utils.update_csv_with_json("Zigbee-sensor", data)
            for key, value in data.items():
                print(f"\t{key}: {value}")
    except json.decoder.JSONDecodeError:
        print("json error")
    except IndexError:
        print("index error")
    except:
        print("unknown error")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()

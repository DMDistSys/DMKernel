#!/usr/bin/env python
import paho.mqtt.client as mqtt
from paho.mqtt import publish
import logging
import threading
import copy
import json

__author__ = "dcpulido91@gmail.com"


class MqttHandler(threading.Thread):
    def __init__(self,
                 conf=None,
                 callback=None):
        threading.Thread.__init__(self)
        if conf is not None:
            self.conf = conf
        else:
            self.conf = dict(host="localhost",
                             port=1883,
                             timeout=60,
                             subscribe=["MqttHand/#"])
        self.connected = False
        self.client = mqtt.Client()
        self.callback_ = callback
        self.buffer = []

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.conf["host"],
                            self.conf["port"],
                            self.conf["timeout"])
        for sub in self.conf["subscribe"]:
            logging.info("MQTT:Subscribe "+sub)
            self.client.subscribe(sub)
        self.client.loop_forever()

    def on_connect(self,
                   client,
                   userdata,
                   flags,
                   rc):
        self.connected = True

    def on_message(self,
                   client,
                   userdata,
                   msg):
        payload = json.loads(msg.payload)
        message = dict(topic=msg.topic,
                       payload=payload)
        if self.callback_ is not None:
            self.callback_(message)
        else:
            self.buffer.append(message)

    def on_publish(self,
                   path,
                   payload,
                   host="localhost"):
        if host is not None:
            hh = host
        else:
            hh = self.conf["host"]
        publish.single(path,
                       payload,
                       hostname=hh)

    def get_buffer(self):
        toret = copy.deepcopy(self.buffer)
        self.buffer = []
        return toret

    def stop(self):
        self.client.disconnect()
        self.connected = False

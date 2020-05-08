import json
import logging

import sys
sys.path.insert(0, './interfaces')  # noqa
sys.path.insert(0, './schema_validation')  # noqa

from MqttHandler import MqttHandler
from SchemaValidator import SchemaValidator

from abc import ABC, abstractmethod


class Component(ABC):
    def __init__(self, conf):
        self.validator_ = SchemaValidator()
        self.conf_validation(conf)
        self.iface_ = MqttHandler(self.conf_["comm_iface"],
                                  callback=self.proc)

    def start(self):
        self.iface_.start()

    def stop(self):
        self.iface_.stop()

    @abstractmethod
    def proc(self, msg):
        pass

    def conf_validation(self, conf):
        if self.validator_.validate_schema(conf)[1] != "kernel_conf_schema":
            raise RuntimeError("Wrong kernel configuration format")
        self.conf_ = conf

    def msg_validation(self, msg):
        return True if self.validator_.validate_schema(msg)[1] == \
            "command_msg_schema" else False

    def get_command(self, msg):
        return msg["payload"]["command"]

    def get_topic(self, msg):
        return msg["topic"]

    def send_msg(self, topic, msg):
        if self.msg_validation(msg):
            self.iface_.on_publish(
                topic, json.dumps(msg))
        else:
            logging.error("Incorrect msg format")

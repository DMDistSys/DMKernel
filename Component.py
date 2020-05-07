import json
import logging

import sys
sys.path.insert(0, './interfaces')  # noqa

from MqttHandler import MqttHandler
from abc import ABC, abstractmethod


class Component(ABC):
    def __init__(self, conf):
        self.conf_ = conf
        if "comm_iface" not in conf.keys():
            self.conf_["comm_iface"] = None
        self.iface_ = MqttHandler(self.conf_["comm_iface"],
                                  callback=self.proc)

    @abstractmethod
    def proc(self, msg):
        pass

    def get_command(self, msg):
        return msg["payload"]["command"]

    def send_msg(self, msg):
        if "command" in msg.keys():
            self.iface_.on_publish(
                "/DMKernel/Info", json.dumps(msg))
        else:
            logging.error("msg not sent due no command on it")

    def start(self):
        self.iface_.start()

    def stop(self):
        self.iface_.stop()

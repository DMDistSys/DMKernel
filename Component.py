# -*- coding: utf-8 -*-
"""Component base class implementation.

Component base class is the main interface of the components with the
middleware features.

"""

import json
import logging

import sys
sys.path.insert(0, './interfaces')  # noqa
sys.path.insert(0, './schema_validation')  # noqa

from MqttHandler import MqttHandler
from SchemaValidator import SchemaValidator

from abc import ABC, abstractmethod


class Component(ABC):
    """Base class to generate new components.

    Attributes:
        validator_ (SchemaValidator): schema validation class.
        iface_ (MqttHandler): communication interface.

    """

    def __init__(self, conf):
        """CTOR.

        Args:
            conf (dict): kernel configuration parameters.

        """
        self.validator_ = SchemaValidator()
        self.conf_validation(conf)
        self.iface_ = MqttHandler(self.conf_["comm_iface"],
                                  callback=self.proc)

    def start(self):
        """Starts the component thread."""
        self.iface_.start()

    def stop(self):
        """Stops the component thread."""
        self.iface_.stop()

    @abstractmethod
    def proc(self, msg):
        """Abstract function that is going to be executed everytime
        the comm interface receives a message.

        Args:
            msg: msg from other component.

        Returns:
            None.

        """
        pass

    def conf_validation(self, conf):
        """Validates kernel configuration parameters.

        Args:
            conf: configuration parameters to validate.

        Returns:
            raises a RuntimeError if the format is wrong.

        """
        if self.validator_.validate_schema(conf)[1] != "kernel_conf_schema":
            raise RuntimeError("Wrong kernel configuration format")
        self.conf_ = conf

    def msg_validation(self, msg):
        """Validates msg format.

        Args:
            msg: msg to validate.

        Returns:
            True if OK False if not.

        """
        return True if self.validator_.validate_schema(msg)[1] == \
            "command_msg_schema" else False

    def get_command(self, msg):
        """Retruns command of msg from comm iface"""
        return msg["payload"]["command"]

    def get_topic(self, msg):
        """Retruns topic of msg from comm iface"""
        return msg["topic"]

    def send_msg(self, topic, msg):
        """Sends a message to other component.

        Args:
            msg: msg to send.

        """
        if self.msg_validation(msg):
            self.iface_.on_publish(
                topic, json.dumps(msg))
        else:
            logging.error("Incorrect msg format")

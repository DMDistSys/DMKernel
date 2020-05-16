import unittest
import sys
import time
sys.path.insert(0, '../')  # noqa
sys.path.insert(0, './interfaces')  # noqa
from MqttHandler import MqttHandler  # noqa


class TestMqttHand(unittest.TestCase):
    def test_init_connected(self):
        mq = MqttHandler()
        self.assertEqual(mq.connected, False)

    def test_init_NoConf_host(self):
        mq = MqttHandler()
        self.assertEqual(mq.conf["host"], "localhost")

    def test_init_NoConf_port(self):
        mq = MqttHandler()
        self.assertEqual(mq.conf["port"], 1883)

    def test_init_Conf_host(self):
        mq = MqttHandler(dict(host="192.169.0.1", port=1884))
        self.assertEqual(mq.conf["host"], "192.169.0.1")

    def test_init_Conf_port(self):
        mq = MqttHandler(dict(host="192.169.0.1", port=1884))
        self.assertEqual(mq.conf["port"], 1884)

    def test_start(self):
        mq = MqttHandler(dict(host="localhost",
                              port=1883,
                              timeout=60,
                              subscribe=["MqttHandler"]))
        mq.start()
        time.sleep(0.1)
        con = mq.connected
        mq.stop()
        self.assertEqual(con, True)

    def test_disconnect(self):
        mq = MqttHandler(dict(host="localhost",
                              port=1883,
                              timeout=60,
                              subscribe=["MqttHandler"]))
        mq.start()
        time.sleep(0.1)
        mq.stop()
        con = mq.connected
        self.assertEqual(con, False)

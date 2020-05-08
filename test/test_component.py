import unittest
import sys
import copy
sys.path.insert(0, './')  # noqa
sys.path.insert(0, './interfaces')  # noqa

from Component import Component


class TestGoodComponent(Component):
    def __init__(self, conf):
        super().__init__(conf)

    def proc(self, msg):
        pass


conf = {
    "component_name": "test",
    "comm_iface": {
        "host": "localhost",
        "port": 1883,
        "timeout": 60,
        "subscribe": [
            "/DMKernel/Commands"
        ]
    }
}

msg = dict(payload=dict(command="command"), topic="test")


class TestMqttHand(unittest.TestCase):
    def test_wrong_impl_no_proc(self):
        class TestWrongComponent(Component):
            def __init__(self, conf):
                super().__init__(conf)
        try:
            ins = TestWrongComponent(conf)
            self.assertEqual(ins.conf_, False)
        except TypeError:
            self.assertEqual(True, True)

    def test_impl_proc(self):

        try:
            ins = TestGoodComponent(conf)
            self.assertEqual(ins.conf_, conf)
        except TypeError:
            self.assertEqual(True, False)

    def test_CTOR_conf(self):
        ins = TestGoodComponent(conf)
        self.assertEqual(ins.conf_, conf)

    def test_CTOR_wrong_conf(self):
        aux = copy.deepcopy(conf)
        del aux["component_name"]
        try:
            ins = TestGoodComponent(aux)
            print(ins)
            self.assertEqual(True, False)
        except RuntimeError:
            self.assertEqual(True, True)

    def test_msg_validation(self):
        ins = TestGoodComponent(conf)
        self.assertEqual(ins.msg_validation(dict(command="command",
                                                 timestamp=1,
                                                 source="source",
                                                 data=dict())), True)

    def test_get_command(self):
        ins = TestGoodComponent(conf)
        self.assertEqual(ins.get_command(msg), "command")

    def test_get_command_wrong(self):
        ins = TestGoodComponent(conf)
        try:
            ins.get_command(dict())
            self.assertEqual(True, False)
        except KeyError:
            self.assertEqual(True, True)

    def test_get_topic(self):
        ins = TestGoodComponent(conf)
        self.assertEqual(ins.get_topic(msg), "test")

    def test_get_topic_wrong(self):
        ins = TestGoodComponent(conf)
        try:
            ins.get_topic(dict())
            self.assertEqual(True, False)
        except KeyError:
            self.assertEqual(True, True)

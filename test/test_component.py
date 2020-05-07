import unittest
import sys
sys.path.insert(0, './')  # noqa
sys.path.insert(0, './interfaces')  # noqa

from Component import Component


class TestGoodComponent(Component):
    def __init__(self, conf):
        super().__init__(conf)

    def proc(self, msg):
        pass


conf = {
    "comm_iface": {
        "host": "localhost",
        "port": 1883,
        "timeout": 60,
        "subscribe": [
            "/DMKernel/Commands"
        ],
        "publish": "/DMKernel/Info"
    }
}


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

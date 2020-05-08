import unittest
import sys

sys.path.insert(0, './schema_validation')  # noqa
from SchemaValidator import SchemaValidator


class TestSchemaValidator(unittest.TestCase):
    def test_schema_not_found(self):
        val = SchemaValidator()
        self.assertEqual(val.validate_schema(dict(name="name")), (False, None))

    def test_msg_schema_OK(self):
        val = SchemaValidator()
        self.assertEqual(val.validate_schema(dict(command="command",
                                                  timestamp=1,
                                                  source="source",
                                                  data=dict())),
                         (True, "command_msg_schema"))

    def test_conf_kernel_OK(self):
        val = SchemaValidator()
        self.assertEqual(val.validate_schema(dict(component_name="component_name",
                                                  comm_iface=dict(
                                                      host="host",
                                                      port="1",
                                                      timeout="1",
                                                      subscribe=list())
                                                  )),
                         (True, "kernel_conf_schema"))

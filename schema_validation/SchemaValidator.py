from schema import SchemaError

from schemas.MsgSchema import command_msg_schema
from schemas.ConfSchema import kernel_conf_schema


class SchemaValidator:
    def __init__(self):
        self.validation_schemas_ = dict(command_msg_schema=command_msg_schema,
                                        kernel_conf_schema=kernel_conf_schema)

    def validate_schema(self, schema):
        for key, value in self.validation_schemas_.items():
            try:
                value.validate(schema)
                return (True, key)
            except SchemaError:
                pass
        return (False, None)


if __name__ == "__main__":
    val = SchemaValidator()

    print(val.validate_schema(dict(name="hola")))
    print(val.validate_schema(
        dict(command="hola", timestamp=1, source="dklsjf", data=dict())))

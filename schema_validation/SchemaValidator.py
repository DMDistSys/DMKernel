# -*- coding: utf-8 -*-
"""SchemaValidatorclass implementation.

Class that validates critical dictionaries in orther to validate
correct formats.

"""

from schema import SchemaError

from schemas.MsgSchema import command_msg_schema
from schemas.ConfSchema import kernel_conf_schema


class SchemaValidator:
    """SchemaValidatorclass class.

    Attributes:
        validation_schemas_ (dcit): dictionary with the schemas.

    """

    def __init__(self):
        """CTOR"""
        self.validation_schemas_ = dict(command_msg_schema=command_msg_schema,
                                        kernel_conf_schema=kernel_conf_schema)

    def validate_schema(self, schema):
        """Validate a given dictionary against stored schemas.

        Args:
            schema: dictinoary to validate.

        Returns:
            tuple (bool, str):
                bool = True if ok False if not.
                str = id of the schema None if not found.

        """
        for key, value in self.validation_schemas_.items():
            try:
                value.validate(schema)
                return (True, key)
            except SchemaError:
                pass
        return (False, None)

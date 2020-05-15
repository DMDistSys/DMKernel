# -*- coding: utf-8 -*-
"""Msg Schemas.

Schemas to validate messages.

"""

from schema import Schema, Use, Optional

command_msg_schema = Schema({
    "source": Use(str),
    "command": Use(str),
    "timestamp": Use(float),
    "data": Optional(Use(dict))
})

# -*- coding: utf-8 -*-
"""Msg Schemas.

Schemas to validate messages.

"""

from schema import Schema, Use

command_msg_schema = Schema({
    "source": Use(str),
    "command": Use(str),
    "timestamp": Use(int),
    "data": Use(dict)
})

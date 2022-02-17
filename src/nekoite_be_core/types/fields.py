import typing as _t

import marshmallow.fields as _fields
from marshmallow import Schema
from marshmallow.fields import (
    UUID,
    Bool,
    Boolean,
    Date,
    DateTime,
    Decimal,
    Dict,
    Email,
    Field,
    Float,
    Int,
    Integer,
    IPv4,
    IPv6,
    List,
    Number,
    Str,
    String,
    Time,
    TimeDelta,
    Url,
)


class Nested(_fields.Nested):
    def __init__(self, dict: _t.Dict[str, _t.Any], *args, **kwargs):
        _fields.Nested.__init__(self, Schema.from_dict(dict), *args, **kwargs)

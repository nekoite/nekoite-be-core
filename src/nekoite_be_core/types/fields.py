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

import nekoite_be_core.view as _v


class Nested(_fields.Nested):
    def __init__(self, dict: _t.Dict[str, _t.Any], *args, **kwargs):
        _fields.Nested.__init__(self, Schema.from_dict(dict), *args, **kwargs)


class Pagination(_fields.Field):
    default_error_messages = {"invalid_pagination": "Not a valid pagination."}

    def _serialize(self, value: _v.Pagination, attr: str, obj: _t.Any, **kwargs):
        if value is None:
            return None
        return value.pagination_dict

    def _deserialize(
        self,
        value: _t.Dict[str, int],
        attr: _t.Optional[str],
        data: _t.Optional[_t.Mapping[str, _t.Any]],
        **kwargs
    ) -> _t.Optional[_v.Pagination]:
        if value is None:
            return None
        try:
            return _v.Pagination.from_dict(value)
        except (KeyError, ValueError) as e:
            raise self.make_error("invalid_pagination") from e

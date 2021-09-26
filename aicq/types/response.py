import typing

from pydantic import validator

from .base import ICQObject, Field

class Response(ICQObject):

    ok: typing.Optional[bool]
    description: typing.Optional[str]
    data: typing.Any

    @validator("data")
    def validate_data(cls, value: dict, values: dict):
        if value.get("ok") is not None:
            values["ok"] = value["ok"]
            del value["ok"]
        if value.get("description") is not None:
            values["description"] = value["description"]
            del value["description"]

        return value
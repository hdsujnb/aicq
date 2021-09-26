import typing

from .base import ICQObject, Field

class User(ICQObject):

    id: int = Field(alias="userId")
    first_name: typing.Optional[str] = Field(alias="firstName")
    last_name: typing.Optional[str] = Field(alias="lastName")
    nick: typing.Optional[str]
    about: typing.Optional[str]
    photo: typing.Optional[typing.List["Photo"]]

class Photo(ICQObject):

    url: str
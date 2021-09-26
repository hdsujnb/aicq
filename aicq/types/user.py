import typing

from .base import ICQObject, Field
from ..utils.mixins import ContextInstanceMixin

class User(ICQObject, ContextInstanceMixin):

    id: typing.Optional[int] = Field(alias="userId")
    first_name: typing.Optional[str] = Field(alias="firstName")
    last_name: typing.Optional[str] = Field(alias="lastName")
    nick: typing.Optional[str]
    about: typing.Optional[str]
    photo: typing.Optional[typing.List["Photo"]]

class Photo(ICQObject):

    url: str
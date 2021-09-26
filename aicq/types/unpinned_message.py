import typing

from .base import ICQObject, Field
from .chat import Chat

class UnpinnedMessage(ICQObject):

    timestamp: typing.Optional[int]
    id: int = Field(alias="msgId")
    chat: typing.Optional[Chat]
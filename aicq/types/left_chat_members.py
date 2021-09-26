import typing

from .base import ICQObject, Field
from .chat import Chat
from .user import User

class LeftChatMembers(ICQObject):

    chat: typing.Optional[Chat]
    members: typing.List[User] = Field(alias="leftMembers")
    removed_by: typing.Optional[User] = Field(alias="removedBy")
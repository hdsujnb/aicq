import typing

from .base import ICQObject, Field
from .chat import Chat
from .user import User

class NewChatMembers(ICQObject):

    chat: typing.Optional[Chat]
    members: typing.List[User] = Field(alias="newMembers")
    added_by: User = Field(alias="addedBy")
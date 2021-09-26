import typing

from enum import Enum
from pydantic import validator

from .base import ICQObject, Field
from .message import Message
from .edited_message import EditedMessage
from .deleted_message import DeletedMessage
from .pinned_message import PinnedMessage
from .unpinned_message import UnpinnedMessage
from .new_chat_members import NewChatMembers
from .left_chat_members import LeftChatMembers
from .callback_query import CallbackQuery

class Events(ICQObject):

    events: typing.Optional[typing.List["Event"]] = []

class Event(ICQObject):

    id: int = Field(alias="eventId")
    type: "EventType"
    payload: typing.Union[
        Message,
        EditedMessage,
        DeletedMessage,
        PinnedMessage,
        UnpinnedMessage,
        NewChatMembers,
        LeftChatMembers,
        CallbackQuery
    ]

    @validator("payload", pre=True)
    def validate_payload(cls, value, values):
        type_ = values["type"]
        if type_ == EventType.NEW_MESSAGE:
            return Message(**value)
        elif type_ == EventType.EDITED_MESSAGE:
            return EditedMessage(**value)
        elif type_ == EventType.DELETED_MESSAGE:
            return DeletedMessage(**value)
        elif type_ == EventType.PINNED_MESSAGE:
            return PinnedMessage(**value)
        elif type_ == EventType.UNPINNED_MESSAGE:
            return UnpinnedMessage(**value)
        elif type_ == EventType.NEW_CHAT_MEMBERS:
            return NewChatMembers(**value)
        elif type_ == EventType.LEFT_CHAT_MEMBERS:
            return LeftChatMembers(**value)
        elif type_ == EventType.CALLBACK_QUERY:
            return CallbackQuery(**value)

class EventType(Enum):

    NEW_MESSAGE = "newMessage"
    EDITED_MESSAGE = "editedMessage"
    DELETED_MESSAGE = "deletedMessage"
    PINNED_MESSAGE = "pinnedMessage"
    UNPINNED_MESSAGE = "unpinnedMessage"
    NEW_CHAT_MEMBERS = "newChatMembers"
    LEFT_CHAT_MEMBERS = "leftChatMembers"
    CALLBACK_QUERY = "callbackQuery"
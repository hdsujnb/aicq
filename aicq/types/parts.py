import typing

from enum import Enum
from pydantic import validator

from .user import User
from .format import Format, FormatItem
from .base import ICQObject, Field
if typing.TYPE_CHECKING:
    from .message import Message

class Part(ICQObject):

    type: "PartType"
    payload: typing.Union[
        "Sticker",
        "Voice",
        "FilePart",
        "MentionPart",
        "Forward",
        "Reply"
    ]

    @validator("payload", pre=True)
    def payload_object(cls, value, values):
        type_ = values["type"]
        if type_ == PartType.STICKER:
            return Sticker(**value)
        elif type_ == PartType.MENTION:
            return MentionPart(**value)
        elif type_ == PartType.VOICE:
            return Voice(**value)
        elif type_ == PartType.FILE:
            return FilePart(**value)
        elif type_ == PartType.FORWARD:
            return Forward(**value)
        elif type_ == PartType.REPLY:
            return Reply(**value)
        elif type_ == PartType.INLINE_KEYBOARD_MARKUP:
            return value

class Sticker(ICQObject):

    file_id: str = Field(alias="fileId")

class MentionPart(User):
    pass

class Voice(ICQObject):

    file_id: str = Field(alias="fileId")

class FilePart(ICQObject):

    file_id: str = Field(alias="fileId")
    type: "FileType"
    caption: typing.Optional[str]
    format: typing.Optional[Format]

class Forward(ICQObject):

    message: "Message"

class Reply(Forward):
    pass

class PartType(Enum):

    STICKER = "sticker"
    MENTION = "mention"
    VOICE = "voice"
    FILE = "file"
    FORWARD = "forward"
    REPLY = "reply"
    INLINE_KEYBOARD_MARKUP = "inlineKeyboardMarkup"

class FileType(Enum):

    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
from .message import Message
from .base import Field

class EditedMessage(Message):

    edited_timestamp: int = Field(alias="editedTimestamp")
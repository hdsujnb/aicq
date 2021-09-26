from .base import (
    ICQObject,
    Field
)
from .chat import (
    BaseChat,
    Chat,
    PrivateChat,
    GroupChat,
    ChannelChat,
    Admins,
    Admin,
    Members,
    Member,
    Users,
    User,
    ChatType,
    get_chat_by_type
)
from .event import (
    Events,
    Event,
    EventType
)
from .message import Message
from .edited_message import EditedMessage
from .deleted_message import DeletedMessage
from .pinned_message import PinnedMessage
from .unpinned_message import UnpinnedMessage
from .new_chat_members import NewChatMembers
from .left_chat_members import LeftChatMembers
from .callback_query import CallbackQuery
from .format import (
    Format,
    FormatItem,
    Bold,
    Italic,
    Underline,
    Strikethrough,
    Link,
    Mention,
    InlineCode,
    Pre,
    OrderedList,
    UnorderedList,
    Quote
)
from .parts import (
    Part,
    Sticker,
    MentionPart,
    Voice,
    FilePart,
    Forward,
    Reply,
    PartType,
    FileType
)
from .response import Response
from .user import (
    User,
    Photo
)
from .parse_mode import ParseMode
from .message import Message
from .action import Action
from .file import File
from .keyboard import (
    TextButton,
    UrlButton,
    ButtonStyle,
    InlineKeyboardMarkup
)

__all__ = (
    "ICQObject",
    "Field",
    "BaseChat",
    "Chat",
    "PrivateChat",
    "GroupChat",
    "ChannelChat",
    "Admins",
    "Admin",
    "Members",
    "Member",
    "Users",
    "User",
    "ChatType",
    "get_chat_by_type",
    "Events",
    "Event",
    "EventType",
    "Message",
    "EditedMessage",
    "DeletedMessage",
    "PinnedMessage",
    "UnpinnedMessage",
    "NewChatMembers",
    "LeftChatMembers",
    "CallbackQuery",
    "Format",
    "FormatItem",
    "Bold",
    "Italic",
    "Underline",
    "Strikethrough",
    "Link",
    "Mention",
    "InlineCode",
    "Pre",
    "OrderedList",
    "UnorderedList",
    "Quote",
    "Part",
    "Sticker",
    "Voice",
    "File",
    "FilePart",
    "MentionPart",
    "Forward",
    "Reply",
    "PartType",
    "FileType",
    "Response",
    "User",
    "Photo",
    "ParseMode",
    "Message",
    "Action",
    "File",
    "TextButton",
    "UrlButton",
    "ButtonStyle",
    "InlineKeyboardMarkup"
)

for _entity_name in __all__:
    _entity = globals()[_entity_name]
    if not hasattr(_entity, "update_forward_refs"):
        continue
    _entity.update_forward_refs(**globals())
"""I borrowed this function from aiogram, thanks!)"""
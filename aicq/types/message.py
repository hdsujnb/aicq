import typing

from .base import ICQObject, Field
from .chat import Chat
from .user import User
from .format import Format
from .parts import Part
from .parse_mode import ParseMode

class Message(ICQObject):

    timestamp: typing.Optional[int]
    id: int = Field(alias="msgId")
    chat: typing.Optional[Chat]
    from_user: typing.Optional[User] = Field(alias="from")
    text: typing.Optional[str]
    format: typing.Optional[Format]
    parts: typing.Optional[typing.List[Part]]
    file_id: typing.Optional[str] = Field(alias="fileId")

    async def answer(self,
                     text: str = None,
                     reply_message_id: typing.List[int] = None,
                     forward_chat_id: int = None,
                     forward_message_id: typing.List[int] = None,
                     inline_keyboard_markup: typing.Any = None,
                     format: Format = None,
                     parse_mode: ParseMode = None
                    ) -> "Message":
        return await self.bot.send_message(
            chat_id=self.chat.id,
            text=text,
            reply_message_id=reply_message_id,
            forward_chat_id=forward_chat_id,
            forward_message_id=forward_message_id,
            inline_keyboard_markup=inline_keyboard_markup,
            format=format,
            parse_mode=parse_mode
        )

    async def answer_file(self,
                          file_id: str = None,
                          file: typing.Any = None,
                          caption: str = None,
                          reply_message_id: typing.List[int] = None,
                          forward_chat_id: int = None,
                          forward_message_id: typing.List[int] = None,
                          inline_keyboard_markup: typing.Any = None,
                          format: Format = None,
                          parse_mode: ParseMode = None
                         ) -> "Message":
        return await self.bot.send_file(
            chat_id=self.chat.id,
            file_id=file_id,
            file=file,
            caption=caption,
            reply_message_id=reply_message_id,
            forward_chat_id=forward_chat_id,
            forward_message_id=forward_message_id,
            inline_keyboard_markup=inline_keyboard_markup,
            format=format,
            parse_mode=parse_mode
        )

    async def answer_voice(self,
                           file_id: str = None,
                           file: typing.Any = None,
                           reply_message_id: typing.List[int] = None,
                           forward_chat_id: int = None,
                           forward_message_id: typing.List[int] = None,
                           inline_keyboard_markup: typing.Any = None) -> "Message":
        return await self.bot.send_voice(
            chat_id=self.chat.id,
            file_id=file_id,
            file=file,
            reply_message_id=reply_message_id,
            forward_chat_id=forward_chat_id,
            forward_message_id=forward_message_id,
            inline_keyboard_markup=inline_keyboard_markup
        )
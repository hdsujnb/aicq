import typing

from .base import ICQObject, Field
from .chat import Chat
from .user import User
from .message import Message

class CallbackQuery(ICQObject):

    id: str = Field(alias="queryId")
    callback_data: str = Field(alias="callbackData")
    chat: typing.Optional[Chat]
    from_user: typing.Optional[User]
    message: Message

    async def answer(self,
                     text: str = None,
                     show_alert: bool = False,
                     url: str = None) -> "CallbackQuery":
        return await self.bot.answer_callback_query(
            id=self.id,
            text=text,
            show_alert=show_alert,
            url=url
        )
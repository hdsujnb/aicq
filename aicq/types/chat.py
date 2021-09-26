from aicq.types import action
import typing

from enum import Enum

from .base import ICQObject, Field
from .user import User
from .response import Response


def get_chat_by_type(data: dict):
    type = ChatType(data.get("type"))
    if type == ChatType.PRIVATE:
        return PrivateChat(**data)
    elif type == ChatType.GROUP:
        return GroupChat(**data)
    elif type == ChatType.CHANNEL:
        return ChannelChat(**data)

class BaseChat(ICQObject):

    type: "ChatType"

class Chat(BaseChat):

    id: str = Field(alias="chatId")
    title: typing.Optional[str]

    async def delete_members(self,
                             *members) -> Response:
        return await self.bot.delete_chat_members(
            self.id,
            *members
        )

    async def set_avatar(self,
                         image: typing.Any) -> Response:
        return await self.bot.set_chat_avatar(
            chat_id=self.id,
            image=image
        )

    async def send_action(self,
                          *actions) -> Response:
        return await self.bot.send_action(
            self.id,
            *actions
        )

    async def get_info(self) -> typing.Union["PrivateChat",
                                             "GroupChat",
                                             "ChannelChat"
                                            ]:
        return await self.bot.get_chat_info(
            self.id
        )

    async def get_admins(self) -> "Admins":
        return await self.bot.get_chat_admins(
            self.id
        )

    async def get_members(self) -> "Members":
        return await self.bot.get_chat_members(
            self.id
        )

    async def get_blocked_users(self) -> "Users":
        return await self.bot.get_chat_blocked_users(
            self.id
        )

    async def get_pending_users(self) -> "Users":
        return await self.bot.get_chat_pending_users(
            self.id
        )

    async def block_user(self,
                         id: str,
                         delete_last_messages: bool = False) -> Response:
        return await self.bot.block_user(
            chat_id=self.id,
            user_id=id,
            delete_last_messages=delete_last_messages
            )

    async def unblock_user(self,
                           id: str) -> Response:
        return await self.bot.unblock_user(
            chat_id=self.id,
            user_id=id
        )

    async def resolve_pending(self,
                              approve: bool,
                              user_id: str = None,
                              everyone: bool = None) -> Response:
        return await self.bot.resolve_pending(
            chat_id=self.id,
            approve=approve,
            user_id=id,
            everyone=everyone
        )

    async def set_title(self,
                        title: str) -> Response:
        return await self.bot.set_chat_title(
            chat_id=self.id,
            title=title
        )
    
    async def set_about(self,
                        about: str) -> Response:
        return await self.bot.set_chat_about(
            chat_id=self.id,
            about=about
        )

    async def set_rules(self,
                        rules: str) -> Response:
        return await self.bot.set_chat_rules(
            chat_id=self.id,
            rules=rules
        )

    async def pin_message(self,
                          id: str) -> Response:
        return await self.bot.pin_message(
            chat_id=self.id,
            id=id
        )
    
    async def unpin_message(self,
                          id: str) -> Response:
        return await self.bot.unpin_message(
            chat_id=self.id,
            id=id
        )

class PrivateChat(BaseChat, User):
    
    is_bot: typing.Optional[bool] = Field(alias="isBot")
    language: typing.Optional[str]

class GroupChat(BaseChat):

    title: str
    about: typing.Optional[str]
    rules: typing.Optional[str]
    invite_link: typing.Optional[str] = Field(alias="inviteLink")
    is_public: typing.Optional[bool] = Field(alias="public")
    join_moderation: typing.Optional[bool] = Field(alias="joinModeration")

class ChannelChat(GroupChat):
    pass

class Admins(ICQObject):

    admins: typing.List["Admin"]

class Members(ICQObject):

    members: typing.List["Member"]

class Member(ICQObject):

    id: int = Field(alias="userId")
    is_creator: typing.Optional[bool] = Field(alias="creator", default=False)

class Admin(Member):
    pass

class Users(ICQObject):

    users: typing.List["User"]

class User(Member):
    pass

class ChatType(Enum):

    PRIVATE = "private"
    GROUP = "group"
    CHANNEL = "channel"
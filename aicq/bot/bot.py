import json

from aicq.types.message import Message
import typing

from .base import BaseBot, api
from ..utils.payload import generate_payload
from ..utils.mixins import ContextInstanceMixin

from .. import types

class Bot(ContextInstanceMixin, BaseBot):

    # Self

    async def get_me(self) -> types.User:
        result = await self.request(api.Methods.GET_ME)

        return types.User(**result.data)

    # Messages

    async def send_message(self,
                           chat_id: str,
                           text: str = None,
                           reply_message_id: typing.List[int] = None,
                           forward_chat_id: int = None,
                           forward_message_id: typing.List[int] = None,
                           inline_keyboard_markup: typing.Any = None,
                           format: types.Format = None,
                           parse_mode: types.ParseMode = None
                          ) -> types.Message:
        result = await self.request(api.Methods.SEND_MESSAGE, generate_payload(
            chatId=chat_id,
            text=text,
            replyMsgId=reply_message_id,
            forwardChatId=forward_chat_id,
            forwardMsgId=forward_message_id,
            inlineKeyboardMarkup=inline_keyboard_markup,
            format=format,
            parseMode=parse_mode
        ))
        
        return types.Message(**result.data)

    async def send_file(self,
                        chat_id: str,
                        file_id: str = None,
                        file: typing.Any = None,
                        caption: str = None,
                        reply_message_id: typing.List[int] = None,
                        forward_chat_id: int = None,
                        forward_message_id: typing.List[int] = None,
                        inline_keyboard_markup: typing.Any = None,
                        format: types.Format = None,
                        parse_mode: types.ParseMode = None
                        ) -> types.Message:
        result = await self.request(api.Methods.SEND_FILE, generate_payload(
            chatId=chat_id,
            fileId=file_id,
            file=file,
            caption=caption,
            replyMsgId=reply_message_id,
            forwardChatId=forward_chat_id,
            forwardMsgId=forward_message_id,
            inlineKeyboardMarkup=inline_keyboard_markup,
            format=format,
            parseMode=parse_mode
        ))

        return types.Message(**result.data)

    async def send_voice(self,
                         chat_id: str,
                         file_id: str = None,
                         file: typing.Any = None,
                         reply_message_id: typing.List[int] = None,
                         forward_chat_id: int = None,
                         forward_message_id: typing.List[int] = None,
                         inline_keyboard_markup: typing.Any = None) -> types.Message:
        result = await self.request(api.Methods.SEND_VOICE, generate_payload(
            chatId=chat_id,
            fileId=file_id,
            file=file,
            replyMsgId=reply_message_id,
            forwardChatId=forward_chat_id,
            forwardMsgId=forward_message_id,
            inlineKeyboardMarkup=inline_keyboard_markup
        ))

        return types.Message(**result.data)

    async def edit_message(self,
                           chat_id: str,
                           id: int,
                           text: str,
                           inline_keyboard_markup: typing.Any = None,
                           format: types.Format = None,
                           parse_mode: types.ParseMode = None) -> types.Message:
        result = await self.request(api.Methods.EDIT_MESSAGE, generate_payload(
            chatId=chat_id,
            msgId=id,
            text=text,
            inlineKeyboardMarkup=inline_keyboard_markup,
            format=format,
            parseMode=parse_mode
        ))

        return Message(**result.data)

    async def delete_message(self,
                             chat_id: str,
                             id: int) -> types.Response:
        result = await self.request(api.Methods.DELETE_MESSAGE, generate_payload(
            chatId=chat_id,
            msgId=id
        ))

        return result

    async def answer_callback_query(self,
                                    id: str,
                                    text: str = None,
                                    show_alert: bool = False,
                                    url: str = None) -> types.CallbackQuery:
        result = await self.request(api.Methods.ANSWER_CALLBACK_QUERY, generate_payload(
            queryId=id,
            text=text,
            showAlert=api.validate_bool(show_alert),
            url=url
        ))

        return result

    # Chats

    async def delete_chat_members(self,
                                 chat_id: str,
                                 *members) -> types.Response:
        members = [{"sn": str(member_id)} for member_id in members]
        result = await self.request(api.Methods.DELETE_CHAT_MEMBER, generate_payload(
            chatId=chat_id,
            members=json.dumps(members)
        ))

        return result

    async def set_chat_avatar(self,
                              chat_id: str,
                              image: typing.Any) -> types.Response:
        result = await self.request(api.Methods.SET_CHAT_AVATAR, generate_payload(
            chatId=chat_id,
            image=image
        ))

        return result

    async def send_action(self,
                          chat_id: str,
                          *actions) -> types.Response:
        actions = list(actions)
        result = await self.request(api.Methods.SEND_ACTION, generate_payload(
            chatId=chat_id,
            actions=actions
        ))
        
        return result

    async def get_chat_info(self,
                            chat_id: str) -> typing.Union[types.PrivateChat,
                                                          types.GroupChat,
                                                          types.ChannelChat
                                                         ]:
        result = await self.request(api.Methods.GET_CHAT_INFO, generate_payload(
            chatId=chat_id
        ))
        
        return types.get_chat_by_type(result.data)

    async def get_chat_admins(self,
                              chat_id: str) -> types.Admins:
        result = await self.request(api.Methods.GET_CHAT_ADMINS, generate_payload(
            chatId=chat_id
        ))

        return types.Admins(**result.data)

    async def get_chat_members(self,
                              chat_id: str) -> types.Members:
        result = await self.request(api.Methods.GET_CHAT_MEMBERS, generate_payload(
            chatId=chat_id
        ))

        return types.Members(**result.data)

    async def get_chat_blocked_users(self,
                                     chat_id: str) -> types.Users:
        result = await self.request(api.Methods.GET_CHAT_BLOCKER_USERS, generate_payload(
            chatId=chat_id
        ))

        return types.Users(**result.data)

    async def get_chat_pending_users(self,
                                     chat_id: str) -> types.Users:
        result = await self.request(api.Methods.GET_CHATS_PENDING_USERS, generate_payload(
            chatId=chat_id
        ))

        return types.Users(**result.data)

    async def block_user(self,
                         chat_id: str,
                         user_id: str,
                         delete_last_messages: bool = False) -> types.Response:
        result = await self.request(api.Methods.BLOCK_USER, generate_payload(
            chatId=chat_id,
            userId=user_id,
            delLastMessages=api.validate_bool(delete_last_messages)
        ))
        
        return result

    async def unblock_user(self,
                         chat_id: str,
                         user_id: str) -> types.Response:
        result = await self.request(api.Methods.BLOCK_USER, generate_payload(
            chatId=chat_id,
            userId=user_id
        ))
        
        return result

    async def resolve_pending(self,
                         chat_id: str,
                         approve: bool,
                         user_id: str = None,
                         everyone: bool = None) -> types.Response:
        result = await self.request(api.Methods.BLOCK_USER, generate_payload(
            chatId=chat_id,
            approve=api.validate_bool(approve),
            userId=user_id,
            everyone=api.validate_bool(everyone)
        ))
        
        return result

    async def set_chat_title(self,
                             chat_id: str,
                             title: str) -> types.Response:
        result = await self.request(api.Methods.SET_CHAT_TITLE, generate_payload(
            chatId=chat_id,
            title=title
        ))

        return result

    async def set_chat_about(self,
                             chat_id: str,
                             about: str) -> types.Response:
        result = await self.request(api.Methods.SET_CHAT_ABOUT, generate_payload(
            chatId=chat_id,
            about=about
        ))

        return result

    async def set_chat_rules(self,
                             chat_id: str,
                             rules: str) -> types.Response:
        result = await self.request(api.Methods.SET_CHAT_RULES, generate_payload(
            chatId=chat_id,
            rules=rules
        ))

        return result

    async def pin_message(self,
                          chat_id: str,
                          id: str) -> types.Response:
        result = await self.request(api.Methods.PIN_MESSAGE, generate_payload(
            chatId=chat_id,
            msgId=id
        ))

        return result

    async def unpin_message(self,
                          chat_id: str,
                          id: str) -> types.Response:
        result = await self.request(api.Methods.UNPIN_MESSAGE, generate_payload(
            chatId=chat_id,
            msgId=id
        ))

        return result

    # Files

    async def get_file_info(self,
                            file_id: str) -> types.Response:
        result = await self.request(api.Methods.GET_FILE_INFO, generate_payload(
            fileId=file_id
        ))

        return result

    async def get_events(self,
                         last_event_id: int = 0,
                         poll_time: int = 60) -> types.Events:
        result = await self.request(api.Methods.GET_EVENTS, generate_payload(
            lastEventId=last_event_id,
            pollTime=poll_time
        ))

        return types.Events(**result.data)
import logging
import asyncio
import re
from http import HTTPStatus

from enum import Enum
from pydantic import BaseModel
import aiohttp

from ..types.response import Response
from ..utils.exceptions import ICQAPIError, ValidationError, NetworkError

BASE_API_URL = "https://api.icq.net/bot/v1/{}"

class ICQAPIServer(BaseModel):

    base: str = BASE_API_URL

    def api_url(self, method: str):
        return self.base.format(method)

    @classmethod
    def from_base(cls, base: str):
        return cls(
            base=base
        )

def validate_token(token: str):
    if not isinstance(token, str):
        raise ValidationError(f"The token is invalid! It should be of type str instead of {type(token)}")

    if re.match(r"001\.\d+\.\d+:\d+", token):
        return True
    else:
        raise ValidationError("Token is invalid!")

def validate_bool(bool_: bool):
    if isinstance(bool_, bool):
        return str(bool_).lower()
    else:
        return bool_

def pre_check_result(response: aiohttp.ClientResponse):
    if response.content_type != "application/json":
        raise NetworkError(f"Invalid content type: {response.content_type}")

    if response.ok:
        return True
    else:
        raise ICQAPIError(f"Request returned code {response.status}")

def check_result(response: Response):
    if response.ok is False:
        if response.description:
            if "Server error" in response.description:
                logging.error("Server error. I am missing this error...")
                return False
            raise ICQAPIError(response.description)
        else:
            raise ICQAPIError("Unknown error")

    return response

def default_data(data: dict, token: str):
    data["token"] = token

async def make_request(server: ICQAPIServer, token: str, method: str, data=None, **kwargs):
    url = server.api_url(method)
    if data is None:
        data = {}
    default_data(data, token)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, **kwargs) as response:
                if pre_check_result(response):
                    return check_result(Response(data=await response.json()))
    except aiohttp.ClientError as e:
        raise NetworkError(f"Aiohttp returned an error: {e}")
    except asyncio.exceptions.TimeoutError:
        return Response()


class Methods(Enum):

    # Self

    GET_ME = "self/get"

    # Messages

    SEND_MESSAGE = "messages/sendText"
    SEND_FILE = "messages/sendFile"
    SEND_VOICE = "messages/sendVoice"
    EDIT_MESSAGE = "messages/editText"
    DELETE_MESSAGE = "messages/deleteMessages"
    ANSWER_CALLBACK_QUERY = "messages/answerCallbackQuery"

    # Chats

    DELETE_CHAT_MEMBER = "chats/members/delete"
    SET_CHAT_AVATAR = "chats/avatar/set"
    SEND_ACTION = "chats/sendActions"
    GET_CHAT_INFO = "chats/getInfo"
    GET_CHAT_ADMINS = "chats/getAdmins"
    GET_CHAT_MEMBERS = "chats/getMembers"
    GET_CHAT_BLOCKER_USERS = "chats/getBlockedUsers"
    GET_CHATS_PENDING_USERS = "chats/getPendingUsers"
    BLOCK_USER = "chats/blockUser"
    UNBLOCK_USER = "chats/unblockUser"
    RESOLVE_PENDING = "chats/resolvePending"
    SET_CHAT_TITLE = "chats/setTitle"
    SET_CHAT_ABOUT = "chats/setAbout"
    SET_CHAT_RULES = "chats/setRules"
    PIN_MESSAGE = "chats/pinMessage"
    UNPIN_MESSAGE = "chats/unpinMessage"

    # Files

    GET_FILE_INFO = "files/getInfo"

    # Events

    GET_EVENTS = "events/get"
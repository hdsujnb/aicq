from abc import ABC, abstractmethod
from enum import Enum

from ..filters.filters import Filter
from ... import types

class StateGroup(Enum):
    pass

class State(Filter):

    def __init__(self, state: StateGroup):
        self.state = state

    async def check(self, message: types.Message):
        state = await message.dispatcher.storage.get_state(message.chat.id, message.from_user.id)
        return state == self.state

class BaseStorage(ABC):

    @abstractmethod
    async def get_state(self, chat_id: str, user_id: str):
        pass

    @abstractmethod
    def set_state(self, chat_id: str, user_id: str, state: StateGroup):
        pass

    @abstractmethod
    def get_data(self, chat_id: str, user_id: str):
        pass

    @abstractmethod
    def update_data(self, chat_id: str, user_id: str, **kwargs):
        pass

    @abstractmethod
    def reset_data(self, chat_id: str, user_id: str):
        pass
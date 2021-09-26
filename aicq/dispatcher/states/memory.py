from copy import deepcopy

from .states import BaseStorage, StateGroup

class MemoryStorage(BaseStorage):

    def __init__(self):
        self.data = {}

    def resolve_address(self, chat_id: str, user_id: str):
        if not chat_id in self.data:
            self.data[chat_id] = {}
        if not user_id in self.data[chat_id]:
            self.data[chat_id][user_id] = {"state": None, "data": {}}

        return chat_id, user_id

    async def get_state(self, chat_id: str, user_id: str):
        chat_id, user_id = self.resolve_address(chat_id, user_id)
        return self.data[chat_id][user_id]["state"]

    async def get_data(self, chat_id: str, user_id: str):
        chat_id, user_id = self.resolve_address(chat_id, user_id)
        return deepcopy(self.data[chat_id][user_id]["data"])

    async def update_data(self, chat_id: str, user_id: str, **kwargs):
        chat_id, user_id = self.resolve_address(chat_id, user_id)
        self.data[chat_id][user_id]["data"].update(kwargs)

    async def set_state(self, chat_id: str, user_id: str, state: StateGroup):
        chat_id, user_id = self.resolve_address(chat_id, user_id)
        self.data[chat_id][user_id]["state"] = state

    async def reset_data(self, chat_id: str, user_id: str):
        chat_id, user_id = self.resolve_address(chat_id, user_id)
        self.data[chat_id][user_id]["state"] = None
        self.data[chat_id][user_id]["data"] = {}
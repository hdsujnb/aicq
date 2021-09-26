import typing

from .filters import Filter
from ...types.message import Message
from ...types.callback_query import CallbackQuery

class Command(Filter):

    def __init__(self,
                 commands: typing.Union[typing.List[str], str],
                 prefix: str = "/",
                 ignore_case: bool = True):
        if isinstance(commands, str):
            commands = [commands]
        
        self.commands = [f"{prefix}{command.lower()}" for command in commands]
        self.ignore_case = ignore_case

    async def check(self, message: Message):
        if not isinstance(message, Message):
            raise TypeError("The 'message' parameter must be a Message instance")

        text = message.text.lower() if self.ignore_case else message.text
        if text not in self.commands:
            return False

class Text(Filter):

    def __init__(self, text: str):
        self.text = text
        self.startswith_ = False
        self.endswith_ = False
        self.contains_ = False
        self.equals_ = False

    def startswith(self, toggle: bool = True):
        self.startswith_ = toggle
        return self

    def endswith(self, toggle: bool = True):
        self.endswith_ = toggle
        return self

    def contains(self, toggle: bool = True):
        self.contains_ = toggle
        return self

    def equals(self, toggle: bool = True):
        self.equals_ = toggle
        return self

    async def check(self, obj: typing.Union[Message, CallbackQuery]):
        if isinstance(obj, Message):
            text = obj.text
        elif isinstance(obj, CallbackQuery):
            text = obj.callback_data

        if self.startswith_:
            return text.startswith(self.text)

        if self.endswith_:
            return text.endswith(self.text)

        if self.contains_:
            return self.text in text

        if self.equals_:
            return text == self.text
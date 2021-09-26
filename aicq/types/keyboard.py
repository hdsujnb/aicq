import typing
import json

from enum import Enum

from .base import ICQObject, Field

class ButtonStyle(Enum):

    BASE = "base"
    PRIMARY = "primary"
    ATTENTION = "attention"

class InlineKeyboardMarkup:

    def __init__(self, row_width: int = 8):
        self.keyboard: typing.Optional[typing.List[typing.List[typing.Union["TextButton", "UrlButton"]]]] = [[]]
        self.row_width: typing.Optional[int] = row_width

    def add(self, button: typing.Union["TextButton", "UrlButton"]):
        current_row = self.keyboard[-1]
        current_row.append(button.to_dict())
        return self

    def row(self):
        self.keyboard.append([])

    def __str__(self):
        return json.dumps(self.keyboard)

class TextButton:

    def __init__(self, text: str, callback_data: str, style: ButtonStyle = ButtonStyle.BASE,):
        self.text = text
        self.style = style
        self.callback_data = callback_data

    def to_dict(self):
        return {
            "text": self.text,
            "style": self.style.value,
            "callbackData": self.callback_data
        }

class UrlButton:

    def __init__(self, text: str, url: str, style: ButtonStyle = ButtonStyle.BASE,):
        self.text = text
        self.style = style
        self.url = url

    def to_dict(self):
        return {
            "text": self.text,
            "style": self.style.value,
            "url": self.url
        }
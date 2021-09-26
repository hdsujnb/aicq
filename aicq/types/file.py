from enum import Enum

from .base import ICQObject, Field

class File(ICQObject):

    type: str
    size: int
    file_name: str = Field(alias="filename")
    url: str
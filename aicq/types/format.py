import typing

from .base import ICQObject, Field

class Format(ICQObject):

    bold: typing.Optional[typing.List["Bold"]]
    italic: typing.Optional[typing.List["Italic"]]
    underline: typing.Optional[typing.List["Underline"]]
    strikethrough: typing.Optional[typing.List["Strikethrough"]]
    link: typing.Optional[typing.List["Link"]]
    mention: typing.Optional[typing.List["Mention"]]
    inline_code: typing.Optional[typing.List["InlineCode"]]
    pre: typing.Optional[typing.List["Pre"]]
    ordered_list: typing.Optional[typing.List["OrderedList"]]
    unordered_list: typing.Optional[typing.List["UnorderedList"]]
    quote: typing.Optional[typing.List["Quote"]]

class FormatItem(ICQObject):

    offset: int
    length: int

class Bold(FormatItem):
    pass

class Italic(FormatItem):
    pass

class Underline(FormatItem):
    pass

class Strikethrough(FormatItem):
    pass

class Link(FormatItem):
    
    link: str

class Mention(FormatItem):
    pass

class InlineCode(FormatItem):
    pass

class Pre(FormatItem):

    code: str

class OrderedList(FormatItem):
    pass

class UnorderedList(FormatItem):
    pass

class Quote(FormatItem):
    pass
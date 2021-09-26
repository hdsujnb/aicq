import typing

from pydantic import BaseModel, Field

if typing.TYPE_CHECKING:
    from ..bot.bot import Bot
    from ..dispatcher.dispatcher import Dispatcher

class ICQObject(BaseModel):

    def __str__(self):
        return str(self.dict(exclude_none=True))

    @property
    def bot(self) -> "Bot":
        from ..bot.bot import Bot
        bot = Bot.get_current()
        if bot is None:
            raise RuntimeError("The bot instance is not installed."
                               "To fix this set the current instance: "
                               "'Bot.set_current (bot_instance)'")
        return bot

    @property
    def dispatcher(self) -> "Dispatcher":
        from ..dispatcher.dispatcher import Dispatcher
        dp = Dispatcher.get_current()
        if dp is None:
            raise RuntimeError("The dispatcher instance is not installed."
                               "To fix this set the current instance: "
                               "'Dispatcher.set_current (dispatcher_instance)'")
        return dp
import logging

from aicq import Bot, Dispatcher, types
from aicq.dispatcher import Command
from aicq.contrib.i18n import I18nMiddleware

logging.basicConfig(level=logging.INFO)
bot = Bot("TOKEN")
dp = Dispatcher(bot)

i18n = I18nMiddleware("messages", default="en")
_ = i18n.gettext
dp.middleware.setup(i18n)

@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await message.answer(_("Hello, {first_name}!").format(first_name=message.from_user.first_name))

dp.start()
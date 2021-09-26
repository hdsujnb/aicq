from aicq import Bot, Dispatcher
from aicq import types

bot = Bot("TOKEN")
dp = Dispatcher(bot)

@dp.message_handler()
async def echo_handler(message: types.Message):
    await message.answer(message.text)

dp.start()
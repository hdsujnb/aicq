import logging

from aicq import Bot, Dispatcher
from aicq.dispatcher import Command, Text
from aicq import types

logging.basicConfig(level=logging.INFO)
bot = Bot("TOKEN")
dp = Dispatcher(bot)

STICKER = "L8g8g000v5udrL6pbxrN285fa5489b1ad"

@dp.message_handler(Command("start"))
async def start_handler(message: types.Message):
    await message.answer_file(STICKER)
    await message.answer(
        text="Hey! I am a bot written with aicq.",
        inline_keyboard_markup=(types.InlineKeyboardMarkup(row_width=1)
        .add(
            types.TextButton("Show the cat", "cat", types.ButtonStyle.ATTENTION)
        )
        .add(types.UrlButton("Github repository", "https://github.com/hdsujnb/aicq", types.ButtonStyle.PRIMARY))
        )
    )

@dp.callback_query_handler(Text("cat").startswith())
async def cat_handler(call: types.CallbackQuery):
    await call.message.answer_file(file=open("examples/cat.png", "rb"), caption="🐱")
    await call.answer("The cat has been send!")

dp.start()
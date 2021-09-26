import logging

from aicq import Bot, Dispatcher, types
from aicq.dispatcher import StateGroup, State, Command, MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot("TOKEN")
"""
MemoryStorage is the default storage.
You can make custom storage (see https://github.com/hdsujnb/aicq/blob/dev-1.x/aicq/dispatcher/states/states.py)
"""
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StateGroup):

    FIRST_NAME = 1
    AGE = 2

@dp.message_handler(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Hey! What is your name?")
    await dp.storage.set_state(message.chat.id, message.from_user.id, Form.FIRST_NAME)

@dp.message_handler(State(Form.FIRST_NAME))
async def first_name_state(message: types.Message):
    await dp.storage.update_data(message.chat.id, message.from_user.id, first_name=message.text)
    await message.answer("Good. How old are you?")
    await dp.storage.set_state(message.chat.id, message.from_user.id, Form.AGE)

@dp.message_handler(State(Form.AGE))
async def age_state(message: types.Message):
    age = message.text
    first_name = (await dp.storage.get_data(message.chat.id, message.from_user.id))["first_name"]
    await message.answer(f"Your name is {first_name} and you are {age} years old")
    await dp.storage.reset_data(message.chat.id, message.from_user.id)

dp.start()
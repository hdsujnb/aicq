from aicq import Bot, Dispatcher
from aicq.dispatcher import Filter
from aicq import types

bot = Bot("TOKEN")
dp = Dispatcher(bot)

class AdminFilter(Filter):

    def __init__(self, *admins: list[int]):
        self.admins = list(admins)

    async def check(self, message: types.Message):
        if not message.from_user.id in self.admins:
            await message.answer("You must be an administrator for this.")
            await message.answer_file(STICKER_NO)
            return False

STICKER_OK = "2cPaklJ6Jp04Zcz8O9lLu55a8436e61ab"
STICKER_NO = "28g8g000ZCIU1mit2sv4Ep5e8317531ab"

@dp.message_handler(AdminFilter(760666737))
async def handler_only_for_admins(message: types.Message):
    await message.answer_file(STICKER_OK)

dp.start()
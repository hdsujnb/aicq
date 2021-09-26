import logging

from aicq import Bot, Dispatcher, types
from aicq.dispatcher import BaseMiddleware

logging.basicConfig(level=logging.INFO)
bot = Bot("TOKEN")
dp = Dispatcher(bot)

class SimpleMiddleware(BaseMiddleware):

    async def on_pre_process_message(self, message: types.Message):
        logging.info(f"New message! Chat id: {message.chat.id}")

    async def on_post_process_message(self, message: types.Message):
        logging.info("Message processed!")

    """
    You can do the same for other events. (
        on_pre_process_edited_message,
        on_pre_process_deleted_message,
        on_pre_process_pinned_message,
        on_pre_process_unpinned_message,
        on_pre_process_new_chat_members,
        on_pre_process_left_chat_members,
        on_pre_process_callback_query
    )
    """

dp.middleware.setup(SimpleMiddleware())

dp.start()
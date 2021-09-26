import asyncio
import typing

import logging

from ..types.event import Event, Events, EventType
from ..bot.bot import Bot
from .handler import Handler
from .filters.filters import Filter
from .middlewares import MiddlewareManager
from .states.states import BaseStorage
from .states.memory import MemoryStorage
from ..utils.mixins import ContextInstanceMixin

logger = logging.getLogger("aicq")

class Dispatcher(ContextInstanceMixin):

    def __init__(self, bot: Bot, storage: BaseStorage = None, loop: asyncio.AbstractEventLoop = None):

        if not isinstance(bot, Bot):
            raise TypeError("The 'bot' parameter must be a Bot instance")

        self.bot = bot
        self.storage = storage if storage else MemoryStorage()
        self.middleware = MiddlewareManager(self)
        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.message_handlers = Handler(self, "message")
        self.edited_message_handlers = Handler(self, "edited_message")
        self.deleted_message_handlers = Handler(self, "deleted_message")
        self.pinned_message_handlers = Handler(self, "pinned_message")
        self.unpinned_message_handlers = Handler(self, "unpinned_message")
        self.new_chat_members_handlers = Handler(self, "new_chat_members")
        self.left_chat_members_handlers = Handler(self, "left_chat_members")
        self.callback_query_handlers = Handler(self, "callback_query")

        self.on_startup = [self._bot_info]
        self.on_shutdown = [self._bye_message, self.stop_polling]
        self._polling = False

    async def process_event(self, event: Event):
        if event.type == EventType.NEW_MESSAGE:
            return await self.message_handlers.notify(event.payload)
        elif event.type == EventType.EDITED_MESSAGE:
            return await self.edited_message_handlers.notify(event.payload)
        elif event.type == EventType.DELETED_MESSAGE:
            return await self.deleted_message_handlers.notify(event.payload)
        elif event.type == EventType.PINNED_MESSAGE:
            return await self.pinned_message_handlers.notify(event.payload)
        elif event.type == EventType.UNPINNED_MESSAGE:
            return await self.unpinned_message_handlers.notify(event.payload)
        elif event.type == EventType.NEW_CHAT_MEMBERS:
            return await self.new_chat_members_handlers.notify(event.payload)
        elif event.type == EventType.LEFT_CHAT_MEMBERS:
            return await self.left_chat_members_handlers.notify(event.payload)
        elif event.type == EventType.CALLBACK_QUERY:
            return await self.callback_query_handlers.notify(event.payload)

    async def process_events(self, events: Events):
        tasks = [self.process_event(event) for event in events.events]
        return await asyncio.gather(*tasks)

    async def stop_polling(self, *args):
        if self._polling:
            self._polling = False

    async def _start_polling(self, last_event_id: int = 0, poll_time: int = 60):
        if self._polling:
            raise RuntimeError("Polling already started")
        self._polling = True

        last_event_id = last_event_id
        while self._polling:
            events = await self.bot.get_events(last_event_id, poll_time)
            if events.events:
                last_event_id = events.events[-1].id
                await self.loop.create_task(self.process_events(events))

    def _start(self, poll_time: int = 60):
        Bot.set_current(self.bot)
        Dispatcher.set_current(self)
        logger.info("Start polling...")
        self.loop.create_task(self._start_polling(poll_time=poll_time))
        self.loop.run_forever()

    async def _on_startup(self):
        for callback in self.on_startup:
            await callback(self)

    async def _on_shutdown(self):
        for callback in self.on_shutdown:
            await callback(self)

    def start(self, poll_time: int = 20):
        self.loop.run_until_complete(self._on_startup())
        try:
            self._start(poll_time=poll_time)
        except (KeyboardInterrupt, SystemExit):
            self.loop.run_until_complete(self._on_shutdown())
            self.loop.stop()

    async def _bot_info(self, *args):
        user = await self.bot.get_me()
        logger.info(f"Bot info: {user.first_name} [@{user.nick}]")

    async def _bye_message(self, *args):
        logger.info("Goodbye. Have a good day!")

    def register_message_handler(self, handler: typing.Callable, *filters: typing.Optional[typing.Tuple[Filter]]):
        self.message_handlers.register(handler, *filters)

    def message_handler(self, *filters: typing.Optional[typing.Tuple[Filter]]):
        def decorator(callback: typing.Callable):
            self.register_message_handler(callback, *filters)
            return callback
        return decorator

    def register_edited_message_handler(self, handler: typing.Callable, *filters: typing.Optional[typing.Tuple[Filter]]):
        self.edited_message_handlers.register(handler, *filters)

    def edited_message_handler(self, *filters: typing.Optional[typing.Tuple[Filter]]):
        def decorator(callback: typing.Callable):
            self.register_edited_message_handler(callback, *filters)
            return callback
        return decorator

    def register_deleted_message_handler(self, handler: typing.Callable, *filters: typing.Optional[typing.Tuple[Filter]]):
        self.deleted_message_handlers.register(handler, *filters)

    def deleted_message_handler(self, *filters: typing.Optional[typing.Tuple[Filter]]):
        def decorator(callback: typing.Callable):
            self.register_deleted_message_handler(callback, *filters)
            return callback
        return decorator

    def register_pinned_message_handler(self, handler: typing.Callable, *filters: typing.Optional[typing.Tuple[Filter]]):
        self.pinned_message_handlers.register(handler, *filters)

    def pinned_message_handler(self, *filters: typing.Optional[typing.Tuple[Filter]]):
        def decorator(callback: typing.Callable):
            self.register_pinned_message_handler(callback, *filters)
            return callback
        return decorator

    def register_unpinned_message_handler(self, handler: typing.Callable, *filters: typing.Optional[typing.Tuple[Filter]]):
        self.unpinned_message_handlers.register(handler, *filters)

    def unpinned_message_handler(self, *filters: typing.Optional[typing.Tuple[Filter]]):
        def decorator(callback: typing.Callable):
            self.register_unpinned_message_handler(callback, *filters)
            return callback
        return decorator

    def register_new_chat_members_handler(self, handler: typing.Callable, *filters: typing.Optional[typing.Tuple[Filter]]):
        self.new_chat_members_handlers.register(handler, *filters)

    def new_chat_members_handler(self, *filters: typing.Optional[typing.Tuple[Filter]]):
        def decorator(callback: typing.Callable):
            self.register_new_chat_members_handler(callback, *filters)
            return callback
        return decorator

    def register_left_chat_members_handler(self, handler: typing.Callable, *filters: typing.Optional[typing.Tuple[Filter]]):
        self.left_chat_members_handlers.register(handler, *filters)

    def left_chat_members_handler(self, *filters: typing.Optional[typing.Tuple[Filter]]):
        def decorator(callback: typing.Callable):
            self.register_left_chat_members_handler(callback, *filters)
            return callback
        return decorator

    def register_callback_query_handler(self, handler: typing.Callable, *filters: typing.Optional[typing.Tuple[Filter]]):
        self.callback_query_handlers.register(handler, *filters)

    def callback_query_handler(self, *filters: typing.Optional[typing.Tuple[Filter]]):
        def decorator(callback: typing.Callable):
            self.register_callback_query_handler(callback, *filters)
            return callback
        return decorator
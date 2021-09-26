import typing
from dataclasses import dataclass

from .filters.filters import Filter, execute_filters

class Handler:

    def __init__(self, dispatcher, middleware_key: str = None):
        self.dispatcher = dispatcher
        self.middleware_key = middleware_key
        self.handlers: typing.List[Handler.HandlerObj] = []

    def register(self, handler: typing.Callable, *filters):
        self.handlers.append(Handler.HandlerObj(handler, list(filters)))

    def unregister(self, handler: typing.Callable):
        for handler_ in self.handlers:
            if handler == handler_.handler:
                self.handlers.remove(handler_)
                return True
        
        raise ValueError("This handler is not registered!")

    async def notify(self, *args):
        data = {}
        if self.middleware_key:
            middlewares_result = await self.dispatcher.middleware.trigger(data, f"pre_process_{self.middleware_key}", *args)
            if middlewares_result is False:
                return False
        for handler in self.handlers:
            if handler.filters:
                filters_result = await execute_filters(data, handler.filters, *args)
                if filters_result is False:
                    continue
            await handler.handler(*args, **data)
            break
        await self.dispatcher.middleware.trigger(data, f"post_process_{self.middleware_key}", *args)

    @dataclass
    class HandlerObj:
        handler: typing.Callable
        filters: typing.Optional[typing.List[Filter]] = None
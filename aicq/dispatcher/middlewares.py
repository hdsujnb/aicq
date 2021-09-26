import typing

if typing.TYPE_CHECKING:
    from .dispatcher import Dispatcher

class MiddlewareManager:

    def __init__(self, dispatcher: "Dispatcher"):
        self.dispatcher = dispatcher
        self.bot = dispatcher.bot
        self.middlewares: typing.List["BaseMiddleware"] = []

    def setup(self, middleware):
        if not isinstance(middleware, BaseMiddleware):
            raise TypeError(f"The 'middleware' parameter must be a BaseMiddleware instance")
        if middleware._configured:
            raise ValueError("That middleware is already used!")

        self.middlewares.append(middleware)
        middleware.setup(self)

    async def trigger(self, data: dict, action: str, *args):
        for middleware in self.middlewares:
            result = await middleware.trigger(action, *args)
            if isinstance(result, bool):
                if result is False:
                    return False
                else:
                    continue

            elif isinstance(result, dict):
                data.update(result)

            else:
                continue
        
class BaseMiddleware:

    def __init__(self):
        self._configured = False
        self._manager = None

    @property
    def manager(self) -> MiddlewareManager:
        if self._manager is None:
            raise RuntimeError("Middleware is not configured!")
        return self._manager
    
    def setup(self, manager: MiddlewareManager):
        self._manager = manager
        self._configured = True

    async def trigger(self, action, *args):
        handler_name = f"on_{action}"
        handler = getattr(self, handler_name, None)
        if not handler:
            return None
        return await handler(*args)
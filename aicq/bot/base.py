import aiohttp

from . import api

class BaseBot:

    def __init__(
        self,
        token: str,
        validate_token: bool = True,
        timeout: aiohttp.ClientTimeout = 60,
        server: api.ICQAPIServer = api.ICQAPIServer()
    ):
        if validate_token:
            api.validate_token(token)

        self._timeout = timeout
        self.server = server
        self.token = token

    async def request(self, method: api.Methods, data: dict = None, **kwargs):
        return await api.make_request(server=self.server, token=self.token, method=method.value, data=data, timeout=self._timeout, **kwargs)
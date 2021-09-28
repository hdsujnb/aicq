# aICQ (asyncICQ)
Lightweight modern asynchronous framework for [**ICQ BOT API**](https://icq.com/botapi/#/) written in python.

## Installation
```shell
pip install aicq
```

## Examples
### Echo bot
```python
from aicq import Bot, Dispatcher, types

bot = Bot("TOKEN")
dp = Dispatcher(bot)

@dp.message_handler()
async def echo_handler(message: types.Message):
    await message.answer(message.text)

dp.start()
```

## Official resources:
- Russian community: [@aicq_ru](https://icq.im/aicq_ru)
- Issues: [Github issues tracker](https://github.com/hdsujnb/aicq/issues)

## Developers
- hdsujnb: [@hdsujnb](https://t.me/hdsujnb)
## Helpers
- Yakov Till: [@YakovTill](https://t.me/YakovTill)

import gettext
import os
from contextvars import ContextVar

from .. import types
from ..dispatcher import BaseMiddleware

class I18nMiddleware(BaseMiddleware):

    ctx_locale = ContextVar("ctx_user_locale", default=None)

    def __init__(self, domain, path=None, default="en"):

        super(I18nMiddleware, self).__init__()

        if path is None:
            path = os.path.join(os.getcwd(), "locales")
        
        self.domain = domain
        self.path = path
        self.default = default
        self.locales = self.find_locales()

    def find_locales(self):
        translations = {}

        for name in os.listdir(self.path):
            if not os.path.isdir(os.path.join(self.path, name)):
                continue
            mo_path = os.path.join(self.path, name, "LC_MESSAGES", self.domain + ".mo")

            if os.path.exists(mo_path):
                with open(mo_path, "rb") as fp:
                    translations[name] = gettext.GNUTranslations(fp)
            elif os.path.exists(mo_path[:-2] + "po"):
                raise RuntimeError(f"Found locale '{name}' but this language is not compiled!")

        return translations

    def gettext(self, singular, plural=None, n=1, locale=None) -> str:
        if locale is None:
            locale = self.ctx_locale.get()

        if locale not in self.locales:
            if n == 1:
                return singular
            return plural

        translator = self.locales[locale]

        if plural is None:
            return translator.gettext(singular)
        return translator.ngettext(singular, plural, n)

    async def get_user_locale(self):
        user = types.User.get_current()
        locale = (await user.bot.get_chat_info(user.id)).language
        if locale and locale in self.locales:
            return locale
        return self.default

    async def on_pre_process_message(self, message: types.Message):
        locale = await self.get_user_locale()
        self.ctx_locale.set(locale)
import gettext
import os

class lang:
    _locale = 'en_US'
    _gettext = None
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(lang, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def setlocale(self, locale):
        change_locale = False
        if not self._locale == locale:
            self._locale = locale
            change_locale = True
        if change_locale:
            self.translate()

    def translate(self):
        data = dict(
            domain=os.getenv('LOCALE_DOMAIN', 'project'),
            localedir=os.getenv('LOCALE_DIR', 'locale'),
            languages=[self._locale]
        )
        translate = gettext.translation(**data)
        translate.install()
        self._gettext = translate.gettext

    @property
    def gettext(self):
        if not self._gettext:
            self.translate()
        return self._gettext

_language = lang()

class t:
    _lang = _language
    def __init__(self, message):
        self._message = message

    def __str__(self):
        _ = self._lang.gettext
        return _(self._message)

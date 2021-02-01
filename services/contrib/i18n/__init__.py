import locale
import gettext
import os


class t:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        try:
            current_locale = '.'.join(locale.getlocale(locale.LC_MESSAGES))
        except TypeError:
            current_locale = 'en_US.UTF-8'
        translation = gettext.translation(
            domain=os.getenv('LOCALE_DOMAIN', 'messages'),
            localedir=os.getenv('LOCALE_DIR', 'locale'),
            languages=[current_locale],
            fallback=True
        )
        translation.install()
        return translation.gettext(self.message)
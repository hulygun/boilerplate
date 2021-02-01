from accounts.consts import ErrorCodes
from i18n import t as _

USER_ERRORS = {
    ErrorCodes.INVALID_PASSWORD: _('Invalid password'),
    ErrorCodes.INVALID_SIGN: _('Invalid sign'),
    ErrorCodes.INVALID_TOKEN: _('Invalid token'),
    ErrorCodes.PASSWORDS_DO_NOT_MATCH: _('Passwords do not match'),
    ErrorCodes.USER_EXIST: _('User exist'),
    ErrorCodes.USER_NOT_CONFIRMED: _('User not confirmed'),
    ErrorCodes.USER_NOT_FOUND: _('User not found'),
    ErrorCodes.WRONG_PASSWORD: _('Wrong password')
}

class TokenType:
    REFRESH = 'refresh'
    ACCESS = 'access'

TOKEN_TYPE_EXPIRE = {
    TokenType.REFRESH: 60 * 60 * 24 * 7,
    TokenType.ACCESS: 60 * 60
}
from accounts.consts import ErrorCodes

USER_ERRORS = {
    ErrorCodes.INVALID_PASSWORD: 'Invalid password',
    ErrorCodes.INVALID_SIGN: 'Invalid sign',
    ErrorCodes.INVALID_TOKEN: 'Invalid token',
    ErrorCodes.PASSWORDS_DO_NOT_MATCH: 'Passwords do not match',
    ErrorCodes.USER_EXIST: 'User exist',
    ErrorCodes.USER_NOT_CONFIRMED: 'User not confirmed',
    ErrorCodes.USER_NOT_FOUND: 'User not found',
    ErrorCodes.WRONG_PASSWORD: 'Wrong password'
}

class TokenType:
    REFRESH = 'refresh'
    ACCESS = 'access'

TOKEN_TYPE_EXPIRE = {
    TokenType.REFRESH: 60 * 60 * 24 * 7,
    TokenType.ACCESS: 60 * 60
}
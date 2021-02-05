import os


class SignExpiries:
    """Expirations members of module"""
    REGISTRATION_EMAIL = 60 * 60 * 24  # 1 day


class ErrorCodes:
    """User errors return codes"""
    INVALID_PASSWORD = 1
    INVALID_SIGN = 2
    INVALID_TOKEN = 3
    PASSWORDS_DO_NOT_MATCH = 4
    USER_EXIST = 5
    USER_NOT_CONFIRMED = 6
    USER_NOT_FOUND = 7
    WRONG_PASSWORD = 8


class MessageTypes:
    """Type of available user messages"""
    CONFIRM = int(os.getenv('MESSAGE_CONFIRM'))
    WELCOME = int(os.getenv('MESSAGE_WELCOME'))
    RESTORE = int(os.getenv('MESSAGE_RESTORE'))

import os
from enum import Enum


class NotificationInterface:
    """Constants of availables message interfaces"""
    VOID = 'void'
    FILE = 'file'
    TELEGRAM = 'telegram'
    EMAIL = 'email'
    SMS = 'sms'


class MessageType(Enum):
    CONFIRM = int(os.getenv('MESSAGE_CONFIRM'))
    WELCOME = int(os.getenv('MESSAGE_WELCOME'))
    RESTORE = int(os.getenv('MESSAGE_RESTORE'))
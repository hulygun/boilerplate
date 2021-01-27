from .interfaces import MessageInterface


class Interface:
    """Constants of availables message interfaces"""
    VOID = 'void'
    TELEGRAM = 'telegram'
    EMAIL = 'email'
    SMS = 'sms'


INTERFACE_MAPPING = {
    Interface.VOID: MessageInterface
}
from .const import INTERFACE_MAPPING, Interface
from .entries import Message


def send_message(interface_repr: str, message_data: dict, **attachments) -> bool:
    """send message"""
    interface = INTERFACE_MAPPING.get(interface_repr, Interface.VOID)
    message = Message(**message_data)
    return interface.send_message(message, **attachments)

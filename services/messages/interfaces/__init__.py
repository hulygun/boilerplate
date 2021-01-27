from typing import Any

from ..entries import Message


class MessageInterface:
    """
    Parent class for use message interfaces
    """
    @staticmethod
    def send_message(mesage: Message, **attachments: Any) -> bool:
        """send message via interface"""
        raise NotImplementedError('Your interface code must implemented "send_message" method')

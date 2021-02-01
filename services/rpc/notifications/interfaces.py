import os
from typing import Optional

from jinja2 import Template, Environment, PackageLoader

from notifications.const import MessageType
from notifications.entries import Message


class BaseMessageInterface:
    _suffix: Optional[str] = None
    """
    Base class for use message interfaces
    """
    def __init__(self, message_type: int, recipient: str, sender: str = None, topic: str = None, **context):
        self.message_type = message_type
        self.sender = sender
        self.recipient = recipient
        self.topic = topic
        self.context = context

    @property
    def template(self) -> Template:
        tpl_name = MessageType(self.message_type).name.lower()
        if self._suffix: tpl_name += f'_{self._suffix}'
        tpl_name += '.tpl'

        env = Environment(
            loader=PackageLoader('notifications', 'tpl')
        )
        template = env.get_template(tpl_name)
        return template

    @property
    def message(self) -> Message:
        return Message(
            sender=self.sender or self.get_sender(),
            recipient=self.recipient,
            topic=self.topic or self.get_topic(),
            message=self.template.render(**self.context)
        )

    def send_message(self) -> bool:
        """send message via interface"""
        raise NotImplementedError('Your interface code must implemented "send_message" method')


    def get_sender(self) -> str:
        """get sender"""
        raise NotImplementedError('Your interface code must implemented "send_message" method')


    def get_topic(self) -> str:
        """get topic"""
        raise NotImplementedError('Your interface code must implemented "send_message" method')


class FileLogBackendInterface(BaseMessageInterface):
    def send_message(self) -> bool:
        try:
            with open('./messages.log', 'a') as file:
                file.writelines([
                    'sender: ' + self.message.sender + '\n',
                    'recipient: ' + self.message.recipient + '\n',
                    'topic: ' + self.message.topic + '\n',
                    'text: ' + self.message.message + '\n',
                    '' + '\n'
                ])
        except:
            return False

        return True

    def get_sender(self) -> str:
        return 'info@email.com'

    def get_topic(self) -> str:
        if self.message_type == MessageType.CONFIRM:
            return 'Confirmation mail'
        else:
            return 'default'
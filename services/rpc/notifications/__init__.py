import inspect
from . import interfaces
from notifications.interfaces import BaseMessageInterface


def get_interface(class_name: str):
    modules = inspect.getmembers(interfaces, inspect.isclass)
    interface = next(filter(lambda obj: obj[0] == class_name, modules), (None, None))
    return interface[1]


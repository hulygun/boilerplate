from notifications import get_interface


def send_message(backend: str, message_type: int, recipient: str, sender: str = None, topic: str = None, **context):
    try:
        backend = get_interface(backend)(message_type, recipient, sender, topic, **context)
        result = backend.send_message()
    except:
        result = False

    return result

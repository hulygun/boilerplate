from typing import Optional

from pydantic import BaseModel

class Message(BaseModel):
    sender: str
    recipient: str
    message: str
    topic: Optional[str]

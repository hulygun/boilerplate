from typing import Optional

from pydantic import BaseModel


class Callback(BaseModel):
    entry: str
    id: Optional[str]
    action: str
    data: dict = dict()
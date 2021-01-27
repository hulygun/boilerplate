"""
Test autodoc description
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import PrivateAttr
from pydantic.main import BaseModel
from pytz import UTC


class User(BaseModel):
    """User model

    :id: user identificator
    :email: user email
    :phone: user phone
    """
    email: str
    id: UUID
    is_active: bool = False
    password: Optional[str]


class UserTokens(BaseModel):
    """User tokens

    :dt: now datetime
    :fingerprint: web client fingerprint for user detecting
    :access_token: user access token
    :refresh_token: user refresh token (use for recovery user access when access token died)
    """
    expired: datetime = datetime.now(UTC)
    fingerprint: str
    access_token: str
    refresh_token: str
from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, Request, HTTPException
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext
from playhouse.shortcuts import model_to_dict
from pytz import UTC
from redis import Redis
from starlette import status

from accounts.entries import User
from api.const import REDIS_HOST, REDIS_AUTH_DB
from .const import TOKEN_TYPE_EXPIRE, TokenType
from .models import DBUser
from api.helpers import get_fingerprint

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)

def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)


class RedisUserToken:

    _token_type = None
    _expired = None

    redis = Redis(host=REDIS_HOST, db=REDIS_AUTH_DB, decode_responses=True)

    def __init__(self, user_id: str, token: str, fingerprint: str):
        self.user_id = user_id
        self.token = token
        self.fingerprint = fingerprint

    def store_token(self, token_type: str) -> RedisUserToken:
        self.redis.setex(self.redis_key, TOKEN_TYPE_EXPIRE[token_type], token_type)
        self._token_type = token_type
        return self

    @property
    def redis_key(self) -> str:
        return ':'.join([self.user_id, self.token, self.fingerprint])

    @property
    def token_type(self) -> str:
        if not self._token_type:
            self._token_type = self.redis.get(self.redis_key)
            self.redis.close()
        return self._token_type

    @property
    def expired(self) -> datetime:
        if not self._expired:
            self._expired = datetime.now(UTC) + timedelta(seconds=self.redis.ttl(self.redis_key))
            self.redis.close()
        return self._expired

    @classmethod
    def from_key(cls, key: str) -> RedisUserToken:
        user_id, token, fingerprint = key.split(':')
        return cls(user_id, token, fingerprint)

    @classmethod
    def get_tokens(cls, **kwargs) -> List[RedisUserToken]:
        queryset = list(map(cls.from_key, cls.redis.scan_iter(
            '{user_id}:{token}:{fingerprint}'.format(
                user_id=kwargs.get('user_id', '*'),
                token=kwargs.get('token', '*'),
                fingerprint=kwargs.get('fingerprint', '*')

            )
        )))
        cls.redis.close()
        return queryset

    @classmethod
    def get_obj(cls, token: str) -> Optional[RedisUserToken]:
        key = cls.redis.scan_iter('*:{}:*'.format(token), count=1)
        cls.redis.close()
        if not key:
            return
        return cls.from_key(key)

    @classmethod
    def delete(cls, *keys) -> None:
        cls.redis.delete(*keys)


oauth2_scheme = APIKeyHeader(name='api-key')

def current_user(request: Request, token: str = Depends(oauth2_scheme)):
    fingerprint = get_fingerprint(request)
    token_obj = RedisUserToken.get_tokens(token=token, fingerprint=fingerprint)
    if token_obj and token_obj[0].token_type == TokenType.ACCESS:
        db_user = model_to_dict(DBUser.get(DBUser.id == token_obj[0].user_id), exclude=['password'])
        return User(**db_user)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )






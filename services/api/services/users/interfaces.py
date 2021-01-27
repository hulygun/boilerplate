from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Optional, Dict
from uuid import UUID, uuid4

from playhouse.shortcuts import model_to_dict
from pytz import UTC
from redis import Redis

from .const import TokenType, TOKEN_TYPE_EXPIRE
from .models import DBUser
from accounts.entries import User, UserTokens
from accounts.interfaces import UserBaseDBIterface
from .utils import encrypt_password, check_encrypted_password, RedisUserToken
from api.const import REDIS_HOST, REDIS_SIGN_DB, SIGN_EXPIRIES


class UserInterface(UserBaseDBIterface):
    user = DBUser

    def activate_user(self, user: User) -> None:
        """Set user to active"""
        query = self.user.update(is_active=True).where(self.user.id == user.id.hex)
        query.execute()

    def check_exist(self, **kwargs) -> bool:
        """Check exist user by keyword args"""
        return bool(self.user.select().where(self.user.email == kwargs['email']).count())

    def clear_tokens(self, user_id: UUID, fingerprint: str) -> None:
        """Clear user tokens by fingerprint"""
        exists_tokens = RedisUserToken.get_tokens(user_id=user_id.hex, fingerprint=fingerprint)
        RedisUserToken.delete(*[tobj.redis_key for tobj in exists_tokens])

    def create_user(self, email: str) -> User:
        """Create user db record"""
        user = self.user.create(email=email, id=uuid4())
        return User(**model_to_dict(user))

    def generate_sign(self, user: User, expiries: int) -> str:
        """Generate unique secret key for acces without another user credentials"""
        secret = token_urlsafe(64)
        self.redis(REDIS_SIGN_DB).setex(secret, SIGN_EXPIRIES, user.id.hex)
        return secret

    def get_tokens(self, user: User, fingerprint: str) -> UserTokens:
        """Get user access and refresh tokens"""
        exists_tokens = RedisUserToken.get_tokens(user_id=user.id.hex, fingerprint=fingerprint)
        data = {TokenType.ACCESS: None, TokenType.REFRESH: None}
        expired = None
        for token_obj in exists_tokens:
            data[token_obj.token_type] = token_obj.token
            if token_obj.token_type == TokenType.ACCESS:
                expired = token_obj.expired
        if not (exists_tokens and  all(data.values())):
            expired = datetime.now(UTC) + timedelta(seconds=TOKEN_TYPE_EXPIRE[TokenType.ACCESS])
            if exists_tokens:
                RedisUserToken.delete(*[tobj.redis_key for tobj in exists_tokens])
            for token_type in data.keys():
                data[token_type] = token_urlsafe(32)
                token_obj = RedisUserToken(user_id=user.id.hex, token=data[token_type], fingerprint=fingerprint)
                token_obj.store_token(token_type)
        output = {
            'access_token': data[TokenType.ACCESS],
            'refresh_token': data[TokenType.REFRESH],
            'fingerprint': fingerprint,
            'expired': expired
        }
        return UserTokens(**output)


    def get_user_by_field(self, **kwargs) -> Optional[User]:
        """Get user by field value or none"""
        if 'id' in kwargs:
            db_user = self.user.get(self.user.id == kwargs['id'])
        elif 'email' in kwargs:
            db_user = self.user.get(self.user.email == kwargs['email'])
        else:
            token = kwargs.get('refresh_token', None) or kwargs.get('access_token', None)
            token_obj = RedisUserToken.get_tokens(token=token)
            db_user = None
            if token_obj:
                token_obj = token_obj[0]
                db_user = self.user.get(self.user.id == token_obj.user_id)
        return User(**model_to_dict(db_user))

    def send_message(self, message_type: int, recipient: User, extra: Dict = None) -> None:
        """Send message"""
        with open('./messages.log', 'a') as file:
            file.writelines([
                'recipient:' + recipient.email + '\n',
                'message type:' + str(message_type) + '\n',
                'text:' + extra.__repr__() + '\n',
                '' + '\n'
            ])

    def set_user_password(self, user: User, password: str) -> None:
        """Set user password"""
        query = self.user.update(password=encrypt_password(password)).where(self.user.id == user.id.hex)
        query.execute()

    def uuid_by_sign(self, sign: UUID) -> Optional[UUID]:
        """Get user_uuid by sign"""
        return self.redis(REDIS_SIGN_DB).get(sign)

    def verificate_password(self, user: User, password: str) -> bool:
        """Verification of user password"""
        print(user.password)
        return check_encrypted_password(password, user.password)

    @staticmethod
    def redis(db: int) -> Redis:
        return Redis(host=REDIS_HOST, db=db, decode_responses=True)

from datetime import datetime
from typing import Optional, Dict
from uuid import uuid4, UUID

import aiounittest

from .consts import ErrorCodes
from .entries import User, UserTokens
from .interfaces import UserBaseDBIterface
from .stories import UserStory


# Mocks
MOCK_USER = {
    'email': 'user1@test.com',
    'password': 'password',
    'confirm_password': 'password'
}

EXIST_EMAIL = 'exist@email.com'

class TestDataInterface(UserBaseDBIterface):
    def activate_user(self, user: User) -> None:
        return

    def check_exist(self, **kwargs) -> bool:
        return EXIST_EMAIL in kwargs.get('email')

    def create_user(self, email: str, phone: str) -> User:
        return User(email=email, phone=phone, id=1)

    def generate_sign(self, user: User, expiries: int) -> UUID:
        return uuid4()

    def get_tokens(self, user: User, fingerprint: str) -> UserTokens:
        return UserTokens(
            dt=datetime.now(),
            fingerprint=fingerprint,
            access_token=uuid4(),
            refresh_token=uuid4()
        )

    def get_user_by_field(self, **kwargs) -> Optional[User]:
        return User(
            email=MOCK_USER['email'],
            id=1,
            is_active=True
        )

    def send_message(self, message_type: int, recipient: User, extra: Dict = None) -> None:
        return

    def set_user_password(self, user: User, password: str) -> None:
        return

    def uuid_by_sign(self, sign: UUID) -> Optional[UUID]:
        return uuid4()

    def verificate_password(self, user: User, password: str) -> bool:
        return password is MOCK_USER['password']


# Tests
class UserStoryTestCase(aiounittest.AsyncTestCase):
    story = None

    def setUp(self) -> None:
        self.story = UserStory(interface=TestDataInterface())

    async def test_create(self):
        """Test create user"""

        user_data = MOCK_USER

        # create normal user
        result = await self.story.create(**user_data)
        self.assertTrue(result.is_success)
        self.assertEqual(user_data['email'], result.value.email)

        # create user with exist email
        user_data['email'] = EXIST_EMAIL
        result = await self.story.create(**user_data)
        self.assertFalse(result.is_success)
        self.assertTrue(result.failure_because(ErrorCodes.USER_EXIST))
        self.assertFalse(result.failure_because(ErrorCodes.PASSWORDS_DO_NOT_MATCH))

        # # create user with no equal password
        user_data['confirm_password'] += 'qwerty'
        result = await self.story.create(**user_data)
        self.assertFalse(result.is_success)
        self.assertTrue(result.failure_because(ErrorCodes.PASSWORDS_DO_NOT_MATCH))
        self.assertFalse(result.failure_because(ErrorCodes.USER_EXIST))

    async def test_confirm(self):
        """Test confirm user"""
        result = await self.story.confirm(sign=uuid4())
        self.assertTrue(result.is_success)

    async def test_get_credentials(self):
        """Test authorize user"""
        user_data = {
            'email': MOCK_USER['email'],
            'password': MOCK_USER['password'],
            'fingerprint': '123'
        }
        # get with true credentials
        result = await self.story.get_credentials(**user_data)
        self.assertTrue(result.is_success)

        # get with wrong credentials
        user_data['password'] += 'qwerty'
        result = await self.story.get_credentials(**user_data)
        self.assertFalse(result.is_success)
        self.assertTrue(result.failure_because(ErrorCodes.WRONG_PASSWORD))
        self.assertFalse(result.failure_because(ErrorCodes.USER_NOT_CONFIRMED))

    async def test_password_change(self):
        """Test change password"""
        user_data = {
            'user': User(
                email=MOCK_USER['email'],
                id=1
            ),
            'password': 'new_password',
            'confirm_password': 'new_password'
        }
        # Normal change
        result = await self.story.password_change(**user_data)
        self.assertTrue(result.is_success)

        # Passwords do not match
        user_data['confirm_password'] += 'qwerty'
        result = await self.story.password_change(**user_data)
        self.assertTrue(result.failure_because(ErrorCodes.PASSWORDS_DO_NOT_MATCH))
        self.assertFalse(result.failure_because(ErrorCodes.USER_NOT_CONFIRMED))

    async def test_password_recovery(self):
        """Test recovery user password"""
        result = await self.story.password_recovery(email=MOCK_USER['email'])
        self.assertTrue(result.is_success)

    async def test_refresh(self):
        """Test refresh user tokens"""
        result = await self.story.refresh(refresh_token=uuid4(), fingerprint='123')
        self.assertTrue(result.is_success)






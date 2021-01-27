from typing import Optional, Dict
from uuid import UUID

from .entries import User, UserTokens


class UserBaseDBIterface:  # pragma: no cover
    """User data interface"""
    def activate_user(self, user: User) -> None:
        """Set user to active"""
        raise NotImplementedError('Not defined')

    def check_exist(self, **kwargs) -> bool:
        """Check exist user by keyword args"""
        raise NotImplementedError('Not defined')

    def clear_tokens(self, user_id: UUID, fingerprint: str) -> None:
        """Clear user tokens by fingerprint"""
        raise NotImplementedError('Not defined')

    def create_user(self, email: str) -> User:
        """Create user db record"""
        raise NotImplementedError('Not defined')

    def generate_sign(self, user: User, expiries: int) -> UUID:
        """Generate unique secret key for acces without another user credentials"""
        raise NotImplementedError('Not defined')

    def get_tokens(self, user: User, fingerprint: str) -> UserTokens:
        """Get user access and refresh tokens"""
        raise NotImplementedError('Not defined')

    def get_user_by_field(self, **kwargs) -> Optional[User]:
        """Get user by field value or none"""
        raise NotImplementedError('Not defined')

    def send_message(self, message_type: int, recipient: User, extra: Dict = None) -> None:
        """Send message"""
        raise NotImplementedError('Not defined')

    def set_user_password(self, user: User, password: str) -> None:
        """Set user password"""
        raise NotImplementedError('Not defined')

    def uuid_by_sign(self, sign: UUID) -> Optional[UUID]:
        """Get user_uuid by sign"""
        raise NotImplementedError('Not defined')

    def verificate_password(self, user: User, password: str) -> bool:
        """Verification of user password"""
        raise NotImplementedError('Not defined')

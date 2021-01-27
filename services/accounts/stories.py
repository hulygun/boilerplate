from contrib.blp.returns import Success, Failure, Result
from contrib.blp.stories import story
from .consts import SignExpiries, ErrorCodes, MessageTypes
from .interfaces import UserBaseDBIterface


class UserStory:
    """
    Implement business logic for work with User entity. Class include pipelines for available processes, interface for
    communicate with another modules of project.

    .. note:: Implement the interface from UserBaseDBIterface for easy way

    :Available pipelines:

    * **confirm** - confirm user registration via sign. e.q:

       .. code-block:: python

          story = UserStory(UserBaseDBIterface)
          data = {'sign': UUID('fd71e5cc-48ac-48fd-826e-bf68af93fbc9')}
          story.confirm(**data)

    * **create** - create user. e.q:

       .. code-block:: python

          story = UserStory(UserBaseDBIterface)
          data = request.data  # {'email': 'dummy@email.com', 'password': 'qwerty', 'confirm_password': 'querty'}
          story.create(**data)

    * **get_credentials** - get user tokens. e.q:

       .. code-block:: python

          story = UserStory(UserBaseDBIterface)
          data = request.data  # {'email': 'dummy@email.com', 'password': 'qwerty', 'fingerprint': 'querty'}
          story.get_credentials(**data)

    * **password_change**  - change user password. e.q:

       .. code-block:: python

          story = UserStory(UserBaseDBIterface)
          user = User(id=1, email='dummy@email.com')
          data = request.data  # {'password': 'qwerty', 'confirm_password': 'querty'}
          story.password_change(user=user, **data)

    * **password_recovery** - recovery user password via recovery email. e.q:

       .. code-block:: python

          story = UserStory(UserBaseDBIterface)
          story.password_recovery(email=request.data['email'])

    * **refresh** - refresh user tokens. e.q:

       .. code-block:: python

          story = UserStory(UserBaseDBIterface)
          data = request.data  # {'refresh_token': 'qwerty', 'fingerprint': 'querty'}
          story.refresh(user=user, **data)
    """

    def __init__(self, interface: UserBaseDBIterface):
        self.interface = interface

    ################
    # User stories #
    ################
    @story('sign')
    def confirm(I):
        I.check_sign
        I.get_user_by_uuid
        I.activate_user
        I.send_welcome_message

    @story('confirm_password', 'email', 'password')
    def create(I):
        I.validate_password
        I.compare_passwords
        I.check_exists_users
        I.create_user
        I.set_password
        I.generate_sign
        I.send_confirm_message
        I.return_user

    @story('email', 'password', 'fingerprint')
    def get_credentials(I):
        I.get_user_by_email
        I.check_valid_password
        I.check_confirm_user
        I.get_user_tokens
        I.return_tokens

    @story('password', 'confirm_password', 'user')
    def password_change(I):
        I.compare_passwords
        I.set_password

    @story('email')
    def password_recovery(I):
        I.get_user_by_email
        I.generate_sign
        I.send_recovery_message

    @story('refresh_token', 'fingerprint')
    def refresh(I):
        I.get_user_by_token
        I.check_confirm_user
        I.clear_tokens
        I.get_user_tokens
        I.return_tokens

    ####################
    # Steps of stories #
    ####################
    def activate_user(self, ctx):
        self.interface.activate_user(ctx.user)
        return Success()

    def check_confirm_user(self, ctx):
        if not ctx.user.is_active:
            return Failure(ErrorCodes.USER_NOT_CONFIRMED)
        return Success()

    def check_exists_users(self, ctx):
        if self.interface.check_exist(email=ctx.email):
            return Failure(ErrorCodes.USER_EXIST, False)
        return Success()

    def check_sign(self, ctx):
        user_uuid = self.interface.uuid_by_sign(ctx.sign)
        if not user_uuid:
            return Failure(ErrorCodes.INVALID_SIGN, False)
        ctx.user_uuid = user_uuid
        return Success()

    def check_valid_password(self, ctx):
        if not self.interface.verificate_password(ctx.user, ctx.password):
            return Failure(ErrorCodes.WRONG_PASSWORD, False)
        return Success()

    def clear_tokens(self, ctx):
        self.interface.clear_tokens(ctx.user.id, ctx.fingerprint)
        return Success()

    def compare_passwords(self, ctx):
        if ctx.password != ctx.confirm_password:
            return Failure(ErrorCodes.PASSWORDS_DO_NOT_MATCH, False)
        return Success()

    def create_user(self, ctx):
        ctx.user = self.interface.create_user(email=ctx.email)
        return Success()

    def generate_sign(self, ctx):
        ctx.sign = self.interface.generate_sign(ctx.user, expiries=SignExpiries.REGISTRATION_EMAIL)
        return Success()

    def get_user_by_email(self, ctx):
        user = self.interface.get_user_by_field(email=ctx.email)
        if not user:
            return Failure(ErrorCodes.USER_NOT_FOUND, False)
        ctx.user = user
        return Success()

    def get_user_by_token(self, ctx):
        user = self.interface.get_user_by_field(refresh_token=ctx.refresh_token, fingerprint=ctx.fingerprint)
        if not user:
            return Failure(ErrorCodes.INVALID_TOKEN, False)
        ctx.user = user
        return Success()

    def get_user_by_uuid(self, ctx):
        user = self.interface.get_user_by_field(id=ctx.user_uuid)
        if not user:
            return Failure(ErrorCodes.USER_NOT_FOUND)
        ctx.user = user
        return Success()

    def get_user_tokens(self, ctx):
        ctx.tokens = self.interface.get_tokens(ctx.user, ctx.fingerprint)
        return Success()

    def return_tokens(self, ctx):
        return Result(ctx.tokens)

    def return_user(self, ctx):
        return Result(ctx.user.dict(exclude='password'))

    def send_confirm_message(self, ctx):
        self.interface.send_message(message_type=MessageTypes.CONFIRM, recipient=ctx.user, extra={'sign': ctx.sign})
        return Success()

    def send_recovery_message(self, ctx):
        self.interface.send_message(message_type=MessageTypes.RECOVERY, recipient=ctx.user, extra={'sign': ctx.sign})
        return Success()

    def send_welcome_message(self, ctx):
        self.interface.send_message(message_type=MessageTypes.WELCOME, recipient=ctx.user)
        return Success()

    def set_password(self, ctx):
        self.interface.set_user_password(ctx.user, ctx.password)
        return Success()

    def validate_password(self, ctx):
        return Success()

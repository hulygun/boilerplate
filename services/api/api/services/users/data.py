from pydantic.main import BaseModel


class UserAuthData(BaseModel):
    email: str
    password: str


class UserCreateData(UserAuthData):
    confirm_password: str


class Token(BaseModel):
    token: str


class Email(BaseModel):
    email: str


class Passwords(BaseModel):
    password: str
    confirm_password: str

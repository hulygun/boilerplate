from fastapi import APIRouter, Depends, HTTPException, Request

from .const import USER_ERRORS
from .data import UserCreateData, UserAuthData, Token, Email, Passwords
from .interfaces import UserInterface
from accounts.stories import UserStory
from api.depends import get_db
from api.db import db
from api.helpers import get_fingerprint
from .utils import current_user

router = APIRouter(tags=['users'])


@router.post('/create', dependencies=[Depends(get_db)])
def create(user: UserCreateData):
    """
    Docstring with markup support
    **item** item
    """
    with db.atomic():
        story = UserStory(UserInterface())
        result = story.create(email=user.email, password=user.password, confirm_password=user.confirm_password)
        if result.is_failed:
            raise HTTPException(status_code=400, detail=USER_ERRORS[result.value[0]])
        return result.value


@router.post('/confirm/{secret}', dependencies=[Depends(get_db)])
def confirm(secret: str):
    """
    Docstring with markup support
    **item** item
    """
    with db.atomic():
        story = UserStory(UserInterface())
        result = story.confirm(sign=secret)
        if result.is_failed:
            raise HTTPException(status_code=404, detail=USER_ERRORS[result.value[0]])
        return result.value


@router.post('/auth', dependencies=[Depends(get_db)])
def auth(request: Request, login: UserAuthData = Depends()):
    """
    Docstring with markup support
    **item** item
    """
    story = UserStory(UserInterface())
    result = story.get_credentials(fingerprint=get_fingerprint(request),**login.dict())
    if result.is_failed:
        raise HTTPException(status_code=400, detail=USER_ERRORS[result.value[0]])
    return result.value


@router.post('/refresh_tokens', dependencies=[Depends(get_db)])
def refresh_tokens(token: Token, request: Request):
    """
    Docstring with markup support
    **item** item
    """
    story = UserStory(UserInterface())
    result = story.refresh(fingerprint=get_fingerprint(request), refresh_token=token.token)
    if result.is_failed:
        raise HTTPException(status_code=400, detail=USER_ERRORS[result.value[0]])
    return result.value


@router.post('/password_recovery', dependencies=[Depends(get_db)])
def password_recovery(email: Email):
    """
    Docstring with markup support
    **item** item
    """
    story = UserStory(UserInterface())
    result = story.password_recovery(email=email.email)
    if result.is_failed:
        raise HTTPException(status_code=400, detail=USER_ERRORS[result.value[0]])
    return result.value


@router.post('/password_change', dependencies=[Depends(get_db)])
def password_change(passwords: Passwords, user = Depends(current_user)):
    """
    Docstring with markup support
    **item** item
    """
    story = UserStory(UserInterface())
    result = story.password_change(user=user, **passwords.dict())
    if result.is_failed:
        raise HTTPException(status_code=400, detail=USER_ERRORS[result.value[0]])
    return result.value


@router.get('/me', dependencies=[Depends(get_db)])
def me(user = Depends(current_user)):
    """
    Docstring with markup support
    **item** item
    """
    return user.dict(exclude={'password'})
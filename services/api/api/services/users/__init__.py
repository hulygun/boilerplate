from fastapi import APIRouter, Depends, HTTPException, Request, Response
from starlette import status

from accounts.entries import User, UserTokens
from .const import USER_ERRORS
from .data import UserCreateData, UserAuthData, Token, Email, Passwords
from .interfaces import UserInterface
from accounts.stories import UserStory
from api.depends import get_db
from api.db import db
from api.helpers import get_fingerprint
from .utils import current_user

router = APIRouter(tags=['users'])


@router.post('/create', dependencies=[Depends(get_db)], name='registration', response_model=User)
async def create(user: UserCreateData):
    """
    ## Regiter new user

    Create db record for user. The user will receive confirmation email with continue registration on email, after
    success action. Link expiration date subject change in the project settings. Also there you can change the domain
    to go from the letter.

    **usage in frontend:**
    ```javascript
    $user = await axios.post('{API_DOMAIN}/users/create', {
        email: "test@e.mail",
        password: "123",
        confirm_password: "123"
    })
    ```
    """
    with db.atomic():
        story = UserStory(UserInterface())
        result = await story.create(email=user.email, password=user.password, confirm_password=user.confirm_password)
        if result.is_failed:
            raise HTTPException(status_code=400, detail=USER_ERRORS[result.value[0]])
        return result.value


@router.post('/confirm/{secret}', dependencies=[Depends(get_db)], name='confirm registration')
async def confirm(secret: str):
    """
    ## Activate user

    **usage in frontend:**
    ```javascript
    await axios.post('{API_DOMAIN}/users/confirm/{secret}', {})
    ```
    """
    with db.atomic():
        story = UserStory(UserInterface())
        result = await story.confirm(sign=secret)
        if result.is_failed:
            raise HTTPException(status_code=404, detail=USER_ERRORS[result.value[0]])
        return Response(status_code=status.HTTP_200_OK)


@router.post('/auth', dependencies=[Depends(get_db)], name='authorization', response_model=UserTokens)
async def auth(request: Request, login: UserAuthData):
    """
    ## Get user tokens

    Get user credentials for usage in project. The server gives a couple of tokens: **access_token** and
    **refresh_token**. Tokens is unique for browser fingerprint. This way each user can have multiple tokens

    **ACCESS_TOKEN** - usage for access to project resources. default expired at 1 hout
    
    **REFRESH_TOKEN** - usage for refresh all user tokens. default expired at 7 days

    **usage in frontend:**
    ```javascript
    $tokens = await axios.post('{API_DOMAIN}/users/auth', {
        email: "test@e.mail",
        password: "123",
    })
    ```
    """
    story = UserStory(UserInterface())
    result = await story.get_credentials(fingerprint=get_fingerprint(request),**login.dict())
    if result.is_failed:
        raise HTTPException(status_code=400, detail=str(USER_ERRORS[result.value[0]]))
    return result.value


@router.post('/refresh_tokens', dependencies=[Depends(get_db)], response_model=UserTokens)
async def refresh_tokens(token: Token, request: Request):
    """
    ## Refresh user tokens

    **usage in frontend:**
    ```javascript
    $tokens = await axios.post('{API_DOMAIN}/users/refresh_tokens', {})
    ```
    """
    story = UserStory(UserInterface())
    result = await story.refresh(fingerprint=get_fingerprint(request), refresh_token=token.token)
    if result.is_failed:
        raise HTTPException(status_code=400, detail=USER_ERRORS[result.value[0]])
    return result.value


@router.post('/password_recovery', dependencies=[Depends(get_db)], name='recovery password')
async def password_recovery(email: Email):
    """
    ## Recovery user password

    Send recovery message to user email

    **usage in frontend:**
    ```javascript
    await axios.post('{API_DOMAIN}/users/password_recovery', {})
    ```
    """
    story = UserStory(UserInterface())
    result = await story.password_recovery(email=email.email)
    if result.is_failed:
        raise HTTPException(status_code=400, detail=USER_ERRORS[result.value[0]])
    return Response(status_code=status.HTTP_200_OK)


@router.post('/password_change', dependencies=[Depends(get_db)], name='change password')
async def password_change(passwords: Passwords, user = Depends(current_user)):
    """
    ## Change user password

    **usage in frontend:**
    ```javascript
    await axios.post('{API_DOMAIN}/users/password_change', {})
    ```
    """
    story = UserStory(UserInterface())
    result = await story.password_change(user=user, **passwords.dict())
    if result.is_failed:
        raise HTTPException(status_code=400, detail=USER_ERRORS[result.value[0]])
    return Response(status_code=status.HTTP_200_OK)


@router.get('/me', dependencies=[Depends(get_db)], name='profile', response_model=User)
async def me(user = Depends(current_user)):
    """
    ## Self profile

    **usage in frontend:**
    ```javascript
    $profile = await axios.get('{API_DOMAIN}/users/me', {})
    ```
    """
    return user.dict(exclude={'password'})

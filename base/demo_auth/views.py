import secrets
from time import time
from typing import Annotated, Any
import uuid

from fastapi import APIRouter, Depends, HTTPException, Header, status, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

demo_auth_router = APIRouter(
    prefix='/demo_auth',
    tags=['Demo Auth'],
)

security = HTTPBasic()

@demo_auth_router.get('/basic-auth/')
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        'message': 'Auth is success!',
        'username': credentials.username,
        'password': credentials.password,
    }


usernames_to_passwords = {
    'gipard': '1234qwwer',
    'admin': 'admin',
}

static_auth_token_to_username = {
    '8eeb8bfc66238aab10f885f6099c7f17': 'gipard',
    '65b99d2fe4f37c4dfe6f31343c7b0235': 'admin',
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password',
        headers={'WWW-Authenticate': 'Basic'},
    )
    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc
    
    if not secrets.compare_digest(
        credentials.password.encode('utf-8'),
        correct_password.encode('utf-8'),
    ):
        raise unauthed_exc

    return credentials.username


def get_username_by_static_auth_token(
    static_token: str = Header(alias='X-auth-token'),
) -> str:
    unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='token invalid',
    headers={'WWW-Authenticate': 'Static-token'},
)
    if static_token not in static_auth_token_to_username:
        raise unauthed_exc
    
    return static_auth_token_to_username[static_token]


@demo_auth_router.get('/basik-auth-username/')
def demo_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        'message': f'Hi, {auth_username}',
        'username': auth_username
    }


@demo_auth_router.get('/basik-static-token-auth-username/')
def demo_auth_some_http_header(
    auth_username: str = Depends(get_username_by_static_auth_token),
):
    return {
        'message': f'Hi, {auth_username}',
        'username': auth_username
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = 'web-app-session-id'

def generate_session_id() -> str:
    return uuid.uuid4().hex

def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
):
    unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='not authenticated',
    headers={'WWW-Authenticate': 'Cookie-auth'},
)
    if session_id not in COOKIES:
        raise unauthed_exc
    return COOKIES[session_id]


@demo_auth_router.post('/login-cookie/')
def demo_auth_login_set_cookie(
    responce: Response,
    # username: str = Depends(get_auth_user_username),
    username: str = Depends(get_username_by_static_auth_token),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        'username': username,
        'login_at': int(time()),
    }
    responce.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {
        'message': f'Hi, {username}',
        'login-statuc': 'ok'
    }


@demo_auth_router.get('/login-cookie/')
def demo_auth_check_cookie(
    responce: Response,
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data['username']
    return {
        'message': f'Hi, {username}',
    }


@demo_auth_router.get('/logout-cookie/')
def demo_auth_logout_cookie(
    responce: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    responce.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data['username']
    return {
        'message': f'Bye, {username}',
    }



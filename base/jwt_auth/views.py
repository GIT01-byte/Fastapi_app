from fastapi import (
    APIRouter, 
    Depends,
    )

from jwt_auth.services import (
    create_access_token,
    create_refresh_token
    )

from jwt_auth.dependencies import (
    get_current_active_auth_user,
    get_current_token_payload,
    http_bearer,
    validate_auth_user,
    get_current_auth_user_for_refresh,
    )

from jwt_auth.schemas import (
    UserSchema,
    TokenInfo,
    )


jwt_auth_router = APIRouter(
    prefix='/jwt_auth',
    tags=['JWT Auth'],
    dependencies=[Depends(http_bearer)],
)


@jwt_auth_router.post('/login/')
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@jwt_auth_router.post(
    '/refresh/',
    response_model=TokenInfo,
    response_model_exclude_none=True,
    )
def auth_refresh_jwt(
    user: UserSchema = Depends(get_current_auth_user_for_refresh)
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )

@jwt_auth_router.get('/users/me/')
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get('iat')
    return {
        'username': user.username,
        'email': user.email,
        'logged_in_at': iat,
    }

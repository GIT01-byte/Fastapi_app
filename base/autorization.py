from fastapi import Depends, FastAPI, HTTPException, Response
from authx import AuthX, AuthXConfig
from pydantic import BaseModel
import uvicorn


app = FastAPI()

config = AuthXConfig(
    JWT_SECRET_KEY='SECRET_KEY',
    JWT_ACCESS_COOKIE_NAME='my_access_token',
    JWT_TOKEN_LOCATION=['cookies']
    )

security = AuthX(config=config)


class UserLoginSchema(BaseModel):
    username: str
    password: str


@app.post('/login/',
        summary='Autorization',
        tags=['Autorization'],
    )
def login(creds: UserLoginSchema, response: Response):
    if creds.username == 'test' and creds.password == 'test':
        token = security.create_access_token(uid='12345')
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    raise HTTPException(status_code=401, detail='Incorrect username or password')


@app.get('/protected/',
        summary='Protected', tags=['Autorization'],
        dependencies=[Depends(security.access_token_required)])
def protected():
    return {'data': 'TOP_SECRET'}


if __name__ == '__main__':
    uvicorn.run(f'{__name__}:app', reload=True)

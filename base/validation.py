import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, ConfigDict

app = FastAPI()


class UserScheme(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=1000)

    model_config = ConfigDict(extra='forbid')


users = []


@app.post('/user',
          summary='Добавить юзера',
          tags=['Юзеры']
          )
def add_user(user: UserScheme):
    users.append(user)
    return {'succes': True,
            'message': f'Юзер успешно добавлен!'
            }


@app.get('/user',
         summary='Получить юзеров',
         tags=['Юзеры']
         )
def get_users():
    return users


class UserAgeScheme(UserScheme):
    age: int = Field(ge=0, le=130)


data = {
    'email': 'abcg@mail.ru',
    'bio': 'None_bio_blayt',
    'age': 15,
}

data_wo_age = {
    'email': 'abcg@mail.ru',
    'bio': 'None_bio_blayt',
}

if __name__ == '__main__':
    uvicorn.run(f'{__name__}:app', reload=True)

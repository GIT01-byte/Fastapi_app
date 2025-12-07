from jwt_auth.schemas import UserSchema

from jwt_auth.utils.bcrypt_utils import hash_password


user_example1 = UserSchema(
    username='gipard',
    password=hash_password('1234qwer'),
    email='gipard123@gmail.com',
)
user_example2 = UserSchema(
    username='tiger',
    password=hash_password('tiger_is_my_life_909912'),
    email='wild_tiger123@gmail.com',
)


users_db: dict[str, UserSchema] = {
    user_example1.username: user_example1,
    user_example2.username: user_example2,
}

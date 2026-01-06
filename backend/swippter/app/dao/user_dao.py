import bcrypt
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from app.core.exceptions import UnauthorizedError, UnprocessableError
from app.dao.base_dao import BaseDAO
from app.models.user import User
from app.utils.utilities import (
    F,
    create_reset_message,
    generate_password_hash,
    generate_salt,
)


class UserDAO(BaseDAO):

    __instance = None

    def __init__(self):
        super().__init__(User)
        self.model = User

    def authenticate_user(self, *args, **kwargs):
        user = self.fetch_one(raise_error=True, **{F.EMAIL: kwargs[F.EMAIL]})
        if bcrypt.checkpw(
            kwargs[F.PASSWORD].encode(F.UTF8), user.password.encode(F.UTF8)
        ):
            return user
        else:
            raise UnauthorizedError(msg=F.INCORRECT_CREDENTIALS)

    def generate_password_reset_token(self, **kwargs):
        user = self.fetch_one(email=kwargs[F.EMAIL])
        uidb64 = urlsafe_base64_encode(force_bytes(user.uuid))
        token = default_token_generator.make_token(user)
        return create_reset_message(uidb64, token)

    def change_user_password(self, user, **kwargs):
        password = kwargs[F.PASSWORD]
        if bcrypt.checkpw(password.encode(F.UTF8), user.password.encode(F.UTF8)):
            raise UnprocessableError(
                msg=F.NEW_PASSWORD_CANNOT_BE_SAME_AS_CURRENT_PASSWORD
            )
        salt = generate_salt()
        new_password = generate_password_hash(password, salt)
        self.update({F.PASSWORD: new_password, F.SALT: salt}, **{F.PK: user.id})

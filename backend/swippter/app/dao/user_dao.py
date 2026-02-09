import bcrypt
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from app.core.exceptions import (
    InvalidRoleValueError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    PasswordConflictError,
    InvalidUIDB64Error,
    InvalidTokenError
)
from app.dao.base_dao import BaseDAO
from app.models.user import User, RoleEnum
from app.utils.utilities import (
    F,
    create_reset_message,
    generate_password_hash,
    generate_salt,
)
from swippter.settings import RESET_EMAIL
from app.config import Starter

class UserDAO(BaseDAO):

    __instance = None

    def __init__(self):
        super().__init__(User)
        self.model = User
        self.starter = Starter.get_instance()

    def signup_user(self, *args, **kwargs):
        valid_values = [RoleEnum.CONSUMER.value, RoleEnum.SELLER.value]
        if kwargs[F.ROLE] not in valid_values:
            raise InvalidRoleValueError(valid_values)
        email = kwargs[F.EMAIL]
        user = self.fetch(**{F.EMAIL: email})
        if user:
            raise UserAlreadyExistsError()
        kwargs[F.EMAIL] = kwargs[F.EMAIL].lower()
        kwargs[F.SALT] = generate_salt()
        kwargs[F.PASSWORD] = generate_password_hash(kwargs[F.PASSWORD], kwargs[F.SALT])
        return self.create(**kwargs)

    def authenticate_user(self, *args, **kwargs):
        user = self.fetch_one(**{F.EMAIL: kwargs[F.EMAIL].lower()})
        if not user:
            raise InvalidCredentialsError()
        if not bcrypt.checkpw(
            kwargs[F.PASSWORD].encode(F.UTF8), user.password.encode(F.UTF8)
        ):
            raise InvalidCredentialsError()
        return user

    def generate_password_reset_token(self, **kwargs):
        user = self.fetch_one(**{F.EMAIL: kwargs[F.EMAIL].lower()})
        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.uuid))
            token = default_token_generator.make_token(user)
            mail_body = {
                F.SUBJECT: F.RESET_PASSWORD,
                F.MESSAGE: create_reset_message(uidb64, token),
                F.SENDER: RESET_EMAIL,
                F.RECIEVER: kwargs[F.EMAIL],
            }
            # check rabbitmq and celery -> Will implement circuit design pattern
            # trigger_mail_backround.delay(**mail_body)

    def verify_token(self, **kwargs):
        uuid = urlsafe_base64_decode(kwargs[F.UIDB64]).decode()
        user = self.fetch_one(**{F.UUID: uuid})
        if not user:
            raise InvalidUIDB64Error()
        if default_token_generator.check_token(user, kwargs[F.TOKEN]) != True:
            raise InvalidTokenError()
        return user

    def change_user_password(self, user, **kwargs):
        password = kwargs[F.PASSWORD]
        if bcrypt.checkpw(password.encode(F.UTF8), user.password.encode(F.UTF8)):
            raise PasswordConflictError()
        salt = generate_salt()
        new_password = generate_password_hash(password, salt)
        self.update({F.PASSWORD: new_password, F.SALT: salt}, **{F.PK: user.id})

import bcrypt
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from app.core.celery_tasks import trigger_mail_backround
from app.core.exceptions import UnauthorizedError, UnprocessableError
from app.core.exceptions import UnprocessableError, CUSTOM_CODE as CC
from app.dao.base_dao import BaseDAO
from app.models.user import User, RoleEnum
from app.utils.utilities import (
    F,
    create_reset_message,
    generate_password_hash,
    generate_salt,
)
from swippter.settings import RESET_EMAIL


class UserDAO(BaseDAO):

    __instance = None

    def __init__(self):
        super().__init__(User)
        self.model = User

    def signup_user(self, *args, **kwargs):
        valid_values = [RoleEnum.CONSUMER.value, RoleEnum.SELLER.value]
        if kwargs[F.ROLE] not in valid_values:
            raise UnprocessableError(
                errors=[
                    {
                        F.FIELD: F.ROLE,
                        F.CODE: CC.INVALID_ROLE,
                        F.KEY: CC.INVALID_ROLE,
                        F.MSG: F.INVALID_ROLE.format(valid_values),
                    }
                ]
            )
        email = kwargs[F.EMAIL]
        user = self.fetch(**{F.EMAIL: email})
        if user:
            raise UnprocessableError(
                errors=[
                    {
                        F.FIELD: F.EMAIL,
                        F.CODE: CC.EMAIL_ALREADY_TAKEN,
                        F.KEY: CC.EMAIL_ALREADY_TAKEN,
                        F.MSG: F.EMAIL_ALREADY_TAKEN,
                    }
                ]
            )
        kwargs[F.EMAIL] = kwargs[F.EMAIL].lower()
        kwargs[F.SALT] = generate_salt()
        kwargs[F.PASSWORD] = generate_password_hash(kwargs[F.PASSWORD], kwargs[F.SALT])
        return self.create(**kwargs)

    def authenticate_user(self, *args, **kwargs):
        user = self.fetch_one(**{F.EMAIL: kwargs[F.EMAIL].lower()})
        if not user:
            raise UnauthorizedError(
                errors=[
                    {
                        F.FIELD: F.EMAIL,
                        F.CODE: CC.EMAIL_NOT_FOUND,
                        F.KEY: CC.EMAIL_NOT_FOUND,
                        F.MSG: F.EMAIL_NOT_FOUND,
                    }
                ]
            )
        if bcrypt.checkpw(
            kwargs[F.PASSWORD].encode(F.UTF8), user.password.encode(F.UTF8)
        ):
            return user
        else:
            raise UnauthorizedError(msg=F.INCORRECT_CREDENTIALS)

    def generate_password_reset_token(self, **kwargs):
        user = self.fetch_one(**{F.EMAIL: kwargs[F.EMAIL].lower()})
        if not user:
            raise UnprocessableError(
                errors=[
                    {
                        F.FIELD: F.EMAIL,
                        F.CODE: CC.EMAIL_NOT_FOUND,
                        F.KEY: CC.EMAIL_NOT_FOUND,
                        F.MSG: F.EMAIL_NOT_FOUND,
                    }
                ]
            )
        uidb64 = urlsafe_base64_encode(force_bytes(user.uuid))
        token = default_token_generator.make_token(user)
        mail_body = {
            F.SUBJECT: F.RESET_PASSWORD,
            F.MESSAGE: create_reset_message(uidb64, token),
            F.SENDER: RESET_EMAIL,
            F.RECIEVER: kwargs[F.EMAIL],
        }
        trigger_mail_backround.delay(**mail_body)

    def verify_token(self, **kwargs):
        uuid = urlsafe_base64_decode(kwargs[F.UIDB64]).decode()
        user = self.fetch_one(**{F.UUID: uuid})
        if not user:
            raise UnprocessableError(
                errors=[
                    {
                        F.FIELD: F.UIDB64,
                        F.CODE: CC.INVALID_USER,
                        F.KEY: CC.INVALID_USER,
                        F.MESSAGE: F.INVALID_USER,
                    }
                ]
            )
        if default_token_generator.check_token(user, kwargs[F.TOKEN]) != True:
            raise UnprocessableError(
                errors=[
                    {
                        F.FIELD: F.TOKEN,
                        F.CODE: CC.INVALID_RESET_TOKEN,
                        F.KEY: CC.INVALID_RESET_TOKEN,
                        F.MESSAGE: F.INVALID_RESET_TOKEN,
                    }
                ]
            )
        return user

    def change_user_password(self, user, **kwargs):
        password = kwargs[F.PASSWORD]
        if bcrypt.checkpw(password.encode(F.UTF8), user.password.encode(F.UTF8)):
            raise UnprocessableError(
                msg=F.NEW_PASSWORD_CANNOT_BE_SAME_AS_CURRENT_PASSWORD
            )
        salt = generate_salt()
        new_password = generate_password_hash(password, salt)
        self.update({F.PASSWORD: new_password, F.SALT: salt}, **{F.PK: user.id})

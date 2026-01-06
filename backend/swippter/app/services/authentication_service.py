from django.utils.http import urlsafe_base64_decode
from dataclasses import dataclass
from app.pattern.factory.validator_factory import ValidatorFactory
from app.pattern.factory.dao_factory import DAOFactory
from app.services.base_service import BaseService
from app.utils.utilities import generate_password_hash, generate_salt, F
from app.core.celery_tasks import trigger_mail_backround
from swippter.settings import RESET_EMAIL

auth_validator = ValidatorFactory.get_auth_validator()
user_dao = DAOFactory.get_user_dao()

@dataclass
class SignUpResponse:
    token: str
    uuid: str
    first_name: str
    last_name: str
    role: str


class AuthenticationService(BaseService):

    def signup_service(self, *args, **kwargs) -> SignUpResponse:
        auth_validator.signup_validator(kwargs)
        kwargs[F.SALT] = generate_salt()
        kwargs[F.PASSWORD] = generate_password_hash(kwargs[F.PASSWORD], kwargs[F.SALT])
        user = user_dao.create(**kwargs)
        return user

    def signin_service(self, *args, **kwargs):
        auth_validator.signin_validator(kwargs)
        user = user_dao.authenticate_user(**kwargs)
        return user

    def forgot_service(self, *args, **kwargs):
        auth_validator.forgot_validator(kwargs)
        message = user_dao.generate_password_reset_token(**kwargs)
        mail_body = {
            F.SUBJECT: F.RESET_PASSWORD,
            F.MESSAGE: message,
            F.SENDER: RESET_EMAIL,
            F.RECIEVER: kwargs[F.EMAIL],
        }
        trigger_mail_backround.delay(**mail_body)

    def verify_token_service(self, *args, **kwargs):
        auth_validator.verify_token_validator(kwargs)
        uuid = urlsafe_base64_decode(kwargs[F.UIDB64])
        return user_dao.fetch_one(**{F.UUID: uuid})

    def change_password_service(self, user, *args, **kwargs):
        auth_validator.change_password_validator(kwargs)
        user_dao.change_user_password(user,**kwargs)
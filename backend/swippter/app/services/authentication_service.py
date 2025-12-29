from dataclasses import dataclass
from app.pattern.factory.validator_factory import ValidatorFactory
from app.pattern.factory.dao_factory import DAOFactory
from app.services.base_service import BaseService
from app.utils.utilities import generate_password_hash, generate_salt, F

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

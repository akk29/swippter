from app.pattern.factory.dao_factory import DAOFactory
from app.pattern.factory.validator_factory import ValidatorFactory
from app.services.base_service import BaseService

auth_validator = ValidatorFactory.get_auth_validator()
user_dao = DAOFactory.get_user_dao()
class AuthenticationService(BaseService):
        
    def signup_service(self, *args, **kwargs):
        auth_validator.signup_validator(kwargs)
        return user_dao.signup_user(**kwargs)

    def signin_service(self, *args, **kwargs):
        auth_validator.signin_validator(kwargs)        
        return user_dao.authenticate_user(**kwargs)

    def forgot_service(self, *args, **kwargs):
        auth_validator.forgot_validator(kwargs)
        user_dao.generate_password_reset_token(**kwargs)        

    def verify_token_service(self, *args, **kwargs):
        auth_validator.verify_token_validator(kwargs)
        return user_dao.verify_token(**kwargs)

    def change_password_service(self, user, *args, **kwargs):
        auth_validator.change_password_validator(kwargs)
        user_dao.change_user_password(user, **kwargs)
from app.pattern.abstract_factory import DefaultFactory
from app.services.base_service import BaseService

class AuthenticationService(BaseService):

    def __init__(self):
        self.auth_validator = DefaultFactory.get_validator().authentication()
        self.user_dao = DefaultFactory.get_dao().user()
        
    def signup_service(self, *args, **kwargs):
        self.auth_validator.signup(kwargs)
        return self.user_dao.signup(**kwargs)

    def signin_service(self, *args, **kwargs):
        self.auth_validator.signin(kwargs)        
        return self.user_dao.signin(**kwargs)

    def forgot_service(self, *args, **kwargs):
        self.auth_validator.forgot(kwargs)
        self.user_dao.forgot(**kwargs)        

    def verify_token_service(self, *args, **kwargs):
        self.auth_validator.verify_token(kwargs)
        return self.user_dao.verify_token(**kwargs)

    def change_password_service(self, user, *args, **kwargs):
        self.auth_validator.change_password(kwargs)
        self.user_dao.change_password(user, **kwargs)
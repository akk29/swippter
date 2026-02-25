from __future__ import annotations
from app.pattern.abstract_factory import DefaultFactory
from app.services.base_service import BaseService

class AuthenticationService(BaseService):

    def __init__(self):
        self.auth_validator = DefaultFactory.get_validator().authentication()
        self.user_dao = DefaultFactory.get_dao().user()
        
    def signup_service(self, *args, **kwargs):
        self.auth_validator.signup_validator(kwargs)
        return self.user_dao.signup_user(**kwargs)

    def signin_service(self, *args, **kwargs):
        self.auth_validator.signin_validator(kwargs)        
        return self.user_dao.authenticate_user(**kwargs)

    def forgot_service(self, *args, **kwargs):
        self.auth_validator.forgot_validator(kwargs)
        self.user_dao.generate_password_reset_token(**kwargs)        

    def verify_token_service(self, *args, **kwargs):
        self.auth_validator.verify_token_validator(kwargs)
        return self.user_dao.verify_token(**kwargs)

    def change_password_service(self, user, *args, **kwargs):
        self.auth_validator.change_password_validator(kwargs)
        self.user_dao.change_user_password(user, **kwargs)
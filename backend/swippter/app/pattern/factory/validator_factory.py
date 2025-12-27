from app.validators.index_validator import IndexValidator
from app.validators.authentication_validator import AuthValidator

class ValidatorFactory:

    @staticmethod
    def get_index_validator():
        return IndexValidator.get_instance()
    

    @staticmethod
    def get_auth_validator():
        return AuthValidator.get_instance() 
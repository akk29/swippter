from app.dao.user_dao import UserDAO
from app.validators.index_validator import IndexValidator
from app.validators.authentication_validator import AuthValidator
from app.services.index_service import IndexService
from app.services.authentication_service import AuthenticationService

class DAOFactory():

    @staticmethod
    def get_user_dao():
        return UserDAO.get_instance()
    
class ServiceFactory:

    @staticmethod
    def get_index_service():
        return IndexService.get_instance()
    
    @staticmethod
    def get_authentication_service():
        return AuthenticationService.get_instance()
    
class ValidatorFactory:

    @staticmethod
    def get_index_validator():
        return IndexValidator.get_instance()
    

    @staticmethod
    def get_auth_validator():
        return AuthValidator.get_instance() 
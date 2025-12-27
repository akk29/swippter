from app.services.index_service import IndexService
from app.services.authentication_service import AuthenticationService
class ServiceFactory:

    @staticmethod
    def get_index_service():
        return IndexService.get_instance()
    
    @staticmethod
    def get_authentication_service():
        return AuthenticationService.get_instance()
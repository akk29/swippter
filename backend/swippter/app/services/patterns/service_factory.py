from app.services.index_service import IndexService

class ServiceFactory:

    @staticmethod
    def get_index_service():
        return IndexService.get_instance()
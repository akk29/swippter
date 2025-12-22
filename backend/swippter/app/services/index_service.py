from app.utils.utilities import get_http_response
from app.pattern.factory.validator_factory import ValidatorFactory
from app.services.base_service import BaseService

index_validator = ValidatorFactory.get_index_validator()

class IndexService(BaseService):

    __instance = None

    def raise_error_service(self):
        index_validator.raise_error_validator({"a":3, "b":2.72, "c":b'binary data'})
        response = get_http_response({})
        return response
            

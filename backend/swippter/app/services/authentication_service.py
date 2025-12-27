from app.utils.utilities import get_http_response
from app.pattern.factory.validator_factory import ValidatorFactory
from app.services.base_service import BaseService

auth_validator = ValidatorFactory.get_auth_validator()

from dataclasses import dataclass

@dataclass
class SignUpResponse:
    token : str
    uuid: str
    first_name: str
    last_name: str
    role : str
#     {
# 	"code": 201,
# 	"message": "created",
# 	"data": {
# 		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZW1haWwiOiJoaGMxQGMuY29tIiwicm9sZSI6IkNhbmRpZGF0ZSJ9.cdd_sbrB3rBC1bUVM4-sDx8a-PY46FNSvwsNsUwm6LI",
# 		"uuid": "c9f8dfc050c24bf88515f1a61395a88b",
# 		"first_name": "cc1",
# 		"last_name": "cc1",
# 		"role": "Candidate"
# 	}
# }

class AuthenticationService(BaseService):

    def signup_service(self,*args,**kwargs)-> SignUpResponse:
        return {}
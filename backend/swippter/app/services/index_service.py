from rest_framework import status as S
from app.services.base_service import BaseService
from app.utils.utilities import F
from app.core.exceptions import UnprocessableError, CUSTOM_CODE, ExceptionGenerator
from app.services.base_service import BaseService


class IndexService(BaseService):

    def raise_error_service(self):
        errors = ExceptionGenerator.error_generator(
            [
                {
                    F.FIELD: F.USERNAME,
                    F.ERRORS: [
                        {
                            F.CODE: CUSTOM_CODE.EMAIL_ALREADY_TAKEN,
                            F.MSG: F.USERNAME_UNAVAILABLE,
                        },
                        {
                            F.CODE: CUSTOM_CODE.EMAIL_ALREADY_TAKEN,
                            F.MSG: F.USERNAME_NOT_ALLOWED,
                        },
                    ],
                },
                {
                    F.FIELD: F.METHOD,
                    F.ERRORS: [
                        {
                            F.CODE: CUSTOM_CODE.EMAIL_ALREADY_TAKEN,
                            F.MSG: F.USERNAME_UNAVAILABLE,
                        },
                        {
                            F.CODE: CUSTOM_CODE.EMAIL_ALREADY_TAKEN,
                            F.MSG: F.USERNAME_NOT_ALLOWED,
                        },
                    ],
                },
                {
                    F.FIELD: F.APPLICATION_JSON,
                    F.ERRORS: [
                        {
                            F.CODE: CUSTOM_CODE.EMAIL_ALREADY_TAKEN,
                            F.MSG: F.USERNAME_UNAVAILABLE,
                        },
                        {
                            F.CODE: CUSTOM_CODE.EMAIL_ALREADY_TAKEN,
                            F.MSG: F.USERNAME_NOT_ALLOWED,
                        },
                    ],
                },
            ]
        )
        raise UnprocessableError(
            code=S.HTTP_422_UNPROCESSABLE_ENTITY, msg=F.UNPROCESSABLE, errors=errors
        )        

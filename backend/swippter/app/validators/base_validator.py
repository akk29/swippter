from rest_framework import status as S
from app.core.exceptions import UnprocessableError, CUSTOM_CODE, ExceptionGenerator
from app.utils.utilities import F
from typing import Dict
from pydantic import BaseModel, ValidationError
from app.pattern.singleton import SingletonPattern
from app.core.exceptions import UnprocessableError

class BaseValidator(SingletonPattern):

    def set_params(self, model: BaseModel, data: Dict):
        self.model = model
        self.data = data

    def validate_data(self):
        try:
            self.model.model_validate(self.data, strict=True)
        except ValidationError as err:
            errors = ExceptionGenerator.error_generator(
                [
                    {
                        F.FIELD: F.USERNAME,
                        F.ERRORS: [
                            {
                                F.CODE: CUSTOM_CODE.USERNAME_TAKEN,
                                F.MSG: F.USERNAME_UNAVAILABLE,
                            },
                            {
                                F.CODE: CUSTOM_CODE.USERNAME_NOT_ALLOWED,
                                F.MSG: F.USERNAME_NOT_ALLOWED,
                            },
                        ],
                    },
                    {
                        F.FIELD: F.METHOD,
                        F.ERRORS: [
                            {
                                F.CODE: CUSTOM_CODE.USERNAME_TAKEN,
                                F.MSG: F.USERNAME_UNAVAILABLE,
                            },
                            {
                                F.CODE: CUSTOM_CODE.USERNAME_NOT_ALLOWED,
                                F.MSG: F.USERNAME_NOT_ALLOWED,
                            },
                        ],
                    },
                    {
                        F.FIELD: F.APPLICATION_JSON,
                        F.ERRORS: [
                            {
                                F.CODE: CUSTOM_CODE.USERNAME_TAKEN,
                                F.MSG: F.USERNAME_UNAVAILABLE,
                            },
                            {
                                F.CODE: CUSTOM_CODE.USERNAME_NOT_ALLOWED,
                                F.MSG: F.USERNAME_NOT_ALLOWED,
                            },
                        ],
                    },
                ]
            )
            raise UnprocessableError(
                code=S.HTTP_422_UNPROCESSABLE_ENTITY, msg=F.UNPROCESSABLE, errors=errors
            )
            raise UnprocessableError(errors=err)

    def validate(self, model: BaseModel, data: Dict):
        self.set_params(model, data)
        self.validate_data()


"""

"""

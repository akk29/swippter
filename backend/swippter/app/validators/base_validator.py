import json
from collections import defaultdict
from typing import Dict
from pydantic import BaseModel, ValidationError as PydanticValidationError
from rest_framework import status as S
from app.core.exceptions import UnprocessableError, CUSTOM_CODE, ExceptionGenerator
from app.utils.utilities import F
from app.pattern.singleton import SingletonPattern

class BaseValidator(SingletonPattern):

    def set_params(self, model: BaseModel, data: Dict):
        self.model = model
        self.data = data

    def get_custom_code(self,error_type):
        try:   
            data = getattr(CUSTOM_CODE,error_type)     
            return data
        except AttributeError:
            return CUSTOM_CODE.PYDANTIC_VALIDATION

    def validate_data(self):
        '''
        Docstring for validate_data
        Raised Pydantic Error from Subclasses
        Transforming those pydantic errors into general error handler
        :param self: Description
        '''
        try:
            self.model.model_validate(self.data, strict=True)
        except PydanticValidationError as err:
            error_map = defaultdict(lambda: [])
            for error in json.loads(err.json()):
                err = error_map[error[F.LOC][0]]
                err.append(
                    {
                        F.CODE: self.get_custom_code(error[F.TYPE]),
                        F.MSG: error[F.MSG],
                    }
                )
                error_map[error[F.LOC][0]] = err
                final_err = [{F.FIELD: k, F.ERRORS: v} for k, v in error_map.items()]
            errors = ExceptionGenerator.error_generator(final_err)
            raise UnprocessableError(
                code=S.HTTP_422_UNPROCESSABLE_ENTITY,
                msg=F.UNPROCESSABLE,
                errors=errors,
            )

    def validate(self, model: BaseModel, data: Dict):
        self.set_params(model, data)
        self.validate_data()

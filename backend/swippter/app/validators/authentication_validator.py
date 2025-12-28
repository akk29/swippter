from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError
from app.core.exceptions import CUSTOM_CODE as CC
from app.models.user import RoleEnum
from app.utils.utilities import F
from app.validators.base_validator import BaseValidator
from app.pattern.factory.dao_factory import UserDAO

user_dao = UserDAO.get_instance()

class SignUpModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
    first_name: str = Field(min_length=3, max_length=8)
    last_name: str = Field(min_length=3, max_length=8)
    role: int

    @field_validator(F.ROLE)
    @classmethod
    def validate_role(cls, v: int):
        valid_values = [RoleEnum.CONSUMER.value, RoleEnum.SELLER.value]        
        if v not in valid_values:
            raise PydanticCustomError(
                CC.get(CC.INVALID_ROLE),
                F.INVALID_ROLE.format(valid_values),
            )
        return v
    
    @field_validator(F.EMAIL)
    @classmethod
    def validate_email(cls, v: str):        
        user = user_dao.fetch(**{
            F.EMAIL : v
        })
        if user:
            raise PydanticCustomError(
                CC.get(CC.EMAIL_ALREADY_TAKEN),
                F.EMAIL_ALREADY_TAKEN,
            )
        return v

class AuthValidator(BaseValidator):

    def signup_validator(self, data):
        self.validate(SignUpModel, data)
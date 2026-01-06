from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from pydantic_core import PydanticCustomError
from app.core.exceptions import CUSTOM_CODE as CC, UnprocessableError
from app.models.user import RoleEnum
from app.pattern.factory.dao_factory import UserDAO
from app.utils.utilities import F
from app.validators.base_validator import BaseValidator

user_dao = UserDAO.get_instance()


class SignUpModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
    first_name: str = Field(min_length=3, max_length=8)
    last_name: str = Field(min_length=3, max_length=8)
    role: int

    @field_validator(F.ROLE)
    @classmethod
    def validate_role(cls, value: int):
        valid_values = [RoleEnum.CONSUMER.value, RoleEnum.SELLER.value]
        if value not in valid_values:
            raise PydanticCustomError(
                CC.get(CC.INVALID_ROLE),
                F.INVALID_ROLE.format(valid_values),
            )
        return value
    # TODO -> move to dao layer
    @field_validator(F.EMAIL)
    @classmethod
    def validate_email(cls, value: str):
        user = user_dao.fetch(**{F.EMAIL: value})
        if user:
            raise PydanticCustomError(
                CC.get(CC.EMAIL_ALREADY_TAKEN),
                F.EMAIL_ALREADY_TAKEN,
            )
        return value.lower()


class SigninModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
    # TODO -> move to dao layer
    @field_validator(F.EMAIL)
    @classmethod
    def validate_email(cls, value: str):
        user = user_dao.fetch_one(**{F.EMAIL: value})
        if not user:
            raise PydanticCustomError(
                CC.get(CC.EMAIL_NOT_FOUND),
                F.EMAIL_NOT_FOUND,
            )
        return value


class ForgotModel(BaseModel):
    email: EmailStr
    # TODO -> move to dao layer
    @field_validator(F.EMAIL)
    @classmethod
    def validate_email(cls, value: str):
        user = user_dao.fetch_one(**{F.EMAIL: value})
        if not user:
            raise PydanticCustomError(
                CC.get(CC.EMAIL_NOT_FOUND),
                F.EMAIL_NOT_FOUND,
            )
        return value


class VerifyTokenModel(BaseModel):
    uidb64: str
    token: str
    # TODO -> move to dao layer
    @model_validator(mode=F.AFTER)
    def validate_details(self):
        user = user_dao.fetch_one(
            **{F.UUID: urlsafe_base64_decode(self.uidb64).decode()}
        )
        if not user:
            raise UnprocessableError(
                errors=[
                    {
                        F.FIELD: F.UIDB64,
                        F.CODE: CC.INVALID_USER,
                        F.KEY: CC.INVALID_USER,
                        F.MESSAGE: F.INVALID_USER,
                    }
                ]
            )
        if default_token_generator.check_token(user, self.token) != True:
            raise UnprocessableError(
                errors=[
                    {
                        F.FIELD: F.TOKEN,
                        F.CODE: CC.INVALID_RESET_TOKEN,
                        F.KEY: CC.INVALID_RESET_TOKEN,
                        F.MESSAGE: F.INVALID_RESET_TOKEN,
                    }
                ]
            )
        return self


class ChangePasswordModel(BaseModel):
    password: str = Field(min_length=8, max_length=32)

class AuthValidator(BaseValidator):

    def signup_validator(self, data):
        self.validate(SignUpModel, data)

    def signin_validator(self, data):
        self.validate(SigninModel, data)

    def forgot_validator(self, data):
        self.validate(ForgotModel, data)

    def verify_token_validator(self, data):
        return self.validate(VerifyTokenModel, data)

    def change_password_validator(self, data):
        self.validate(ChangePasswordModel, data)
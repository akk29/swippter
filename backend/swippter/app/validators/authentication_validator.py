from pydantic import BaseModel, EmailStr, Field
from app.validators.base_validator import BaseValidator
class SignUpModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
    first_name: str = Field(min_length=3, max_length=8)
    last_name: str = Field(min_length=3, max_length=8)
    role: int

class SigninModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
class ForgotModel(BaseModel):
    email: EmailStr
class VerifyTokenModel(BaseModel):
    uidb64: str
    token: str

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
        self.validate(VerifyTokenModel, data)

    def change_password_validator(self, data):
        self.validate(ChangePasswordModel, data)

from pydantic import BaseModel
from app.validators.base_validator import BaseValidator

class Model(BaseModel):
    a: int
    b: float
    c: str


class AuthValidator(BaseValidator):

    def signup_validator(self,data):
        self.validate(Model,data)
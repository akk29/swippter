from pydantic import BaseModel
from app.validators.base_validator import BaseValidator

class IndexModel(BaseModel):
    a: int
    b: float
    c: str


class IndexValidator(BaseValidator):

    def raise_error_validator(self,data):
        self.validate(IndexModel,data)
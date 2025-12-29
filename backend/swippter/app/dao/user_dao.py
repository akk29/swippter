import bcrypt
from app.core.exceptions import UnauthorizedError
from app.dao.base_dao import BaseDAO
from app.models.user import User
from app.utils.utilities import F, generate_password_hash

class UserDAO(BaseDAO):

    __instance = None

    def __init__(self):
        super().__init__(User)
        self.model = User

    def authenticate_user(self, *args, **kwargs):
        user = self.fetch_one(raise_error=True, **{F.EMAIL: kwargs[F.EMAIL]})        
        hashed = generate_password_hash(kwargs[F.PASSWORD], user.salt)
        # bypass
        # correct implementation
        # if bcrypt.checkpw(user.password.encode(F.UTF8),hashed.encode(F.UTF8)):
        if(user.password.encode(F.UTF8)==hashed.encode(F.UTF8)):
            return user
        else:
            raise UnauthorizedError(msg=F.INCORRECT_CREDENTIALS)

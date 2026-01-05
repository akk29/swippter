import bcrypt
from app.core.exceptions import UnauthorizedError
from app.dao.base_dao import BaseDAO
from app.models.user import User
from app.utils.utilities import F

class UserDAO(BaseDAO):

    __instance = None

    def __init__(self):
        super().__init__(User)
        self.model = User

    def authenticate_user(self, *args, **kwargs):
        user = self.fetch_one(raise_error=True, **{F.EMAIL: kwargs[F.EMAIL]})
        if bcrypt.checkpw(
            kwargs[F.PASSWORD].encode(F.UTF8), user.password.encode(F.UTF8)
        ):
            return user
        else:
            raise UnauthorizedError(msg=F.INCORRECT_CREDENTIALS)

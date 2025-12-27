from app.models.user import User
from app.dao.base_dao import BaseDAO

class UserDAO(BaseDAO):

    __instance = None

    def __init__(self, model):
        super().__init__(User)
        self.model = User
    
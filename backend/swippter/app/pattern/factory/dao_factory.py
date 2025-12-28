from app.dao.user_dao import UserDAO

class DAOFactory():

    @staticmethod
    def get_user_dao():
        return UserDAO.get_instance()
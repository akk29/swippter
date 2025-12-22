from app.dao.user_dao import UserDAO

class DAOFactory():

    @staticmethod
    def get_model_instance():
        return UserDAO.get_instance()
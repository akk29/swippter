from app.validators.index_validator import IndexValidator

class ValidatorFactory:

    @staticmethod
    def get_index_validator():
        return IndexValidator.get_instance()
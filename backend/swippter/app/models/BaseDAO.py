import threading

class BaseDAO:

    _global_lock = threading.Lock()
    _instances = {}
    _locks = {}

    def __init__(self, model):
        self.model = model

    @classmethod
    def get_instance(cls):

        if cls not in cls._locks:
            with cls._global_lock:
                if cls not in cls._locks:
                    cls._locks[cls] = threading.Lock()

        if cls not in cls._instances:
            with cls._locks[cls]:
                if cls not in cls._instances:
                    cls._instances[cls] = cls()
        return cls._instances[cls]

    def create(self,*args,**kwargs):
        pass

    def update(self,*agrs,**kwargs):
        pass

    def delete(self,*args,**kwargs):
        pass

    def fetch(self):
        pass
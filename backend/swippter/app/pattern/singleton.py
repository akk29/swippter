import threading

class SingletonPattern:
    _global_lock = threading.Lock()
    _instances = {}
    _locks = {}

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
import logging
import threading
import traceback

LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s --- %(message)s"

class Logger:

    _instance = None
    _lock = threading.Lock()

    @staticmethod  # On Load
    def setup():
        if Logger._instance is None:
            Logger._lock.acquire()
            try:
                if Logger._instance is None:
                    logger = logging.getLogger(__name__)
                    logger.setLevel(logging.INFO)
                    handler = logging.StreamHandler()
                    formatter = logging.Formatter(LOGGING_FORMAT)
                    handler.setFormatter(formatter)
                    logger.addHandler(handler)
                    logger.propagate = False
                    Logger._instance = logger
                    logger.info('Setting up logger - objID - {}'.format(id(Logger._instance)))
            finally:
                Logger._lock.release()
        return Logger._instance

    @staticmethod  # Inside Application
    def get_logger():
        return Logger.setup()

    @staticmethod
    def log(exception):
        tb = traceback.extract_stack()[:-1]  # Exclude current frame
        last_frame = tb[-3]
        file_name = last_frame.filename
        line_no = last_frame.lineno
        func_name = last_frame.name
        Logger.get_logger().error(
            f"{file_name}:{line_no}:{func_name} - {exception.__repr__()} - {exception.__process_exception__()}"
        )

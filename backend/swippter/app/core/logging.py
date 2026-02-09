import logging
import threading
import traceback
from app.utils.utilities import F

class CustomFormatter(logging.Formatter):

    green = F.LOG_GREEN
    grey = F.LOG_GREY
    yellow = F.LOG_YELLOW
    red = F.LOG_RED
    bold_red = F.LOG_BOLD_RED
    reset = F.LOG_RESET
    format = F.LOGGING_FORMAT

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
        logging.FATAL: red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class Logger:

    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def setup():
        if Logger._instance is None:
            with Logger._lock:
                if Logger._instance is None:
                    logger = logging.getLogger(__name__)
                    logger.setLevel(logging.INFO)
                    handler = logging.StreamHandler()
                    handler.setFormatter(CustomFormatter())
                    logger.addHandler(handler)
                    logger.propagate = False
                    Logger._instance = logger
                    logger.info(F.LOGGER_SETUP.format(id(Logger._instance)))
        return Logger._instance

    @staticmethod
    def get_logger():
        return Logger.setup()

    @staticmethod
    def log_exception(exception):
        tb = traceback.extract_stack()[:-1]
        last_frame = tb[-4]
        file_name = last_frame.filename
        line_no = last_frame.lineno
        func_name = last_frame.name
        Logger.get_logger().error(
            f"{file_name}:{line_no}:{func_name} - {exception.__repr__()} - {exception.__process_exception__()}"
        )
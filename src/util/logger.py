import logging
import queue
import sys
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler

from pythonjsonlogger import jsonlogger

from src.config import APP_NAME, LOGGING_CONSOLE, LOGGING_FILE

# init root logger with null handler
logging.basicConfig(handlers=[logging.NullHandler()])

# formatter
log_format = "%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s"
log_formatter = jsonlogger.JsonFormatter(fmt=log_format, timestamp=True)

# stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(log_formatter)

# init listener
log_queue = queue.Queue()
log_qhandler = QueueHandler(log_queue)
log_qlistener = QueueListener(log_queue, respect_handler_level=True)
log_qlistener.start()


def configure_handlers(console=LOGGING_CONSOLE, log_path=LOGGING_FILE):
    """
    Configure log queue listener to log into file and console.

    Args:
        console (bool): whether to log on console
        log_path (str): path of log file

    Returns:
        logger (logging.Logger): configured logger
    """
    global log_qlistener
    log_qlistener.stop()
    handlers = []

    # rotating file handler
    if log_path:
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 2 ** 20,  # 10 MB
            backupCount=1,  # 1 backup
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_formatter)
        handlers.append(file_handler)

    # console handler
    if console:
        handlers.append(stdout_handler)

    log_qlistener = QueueListener(log_queue, *handlers, respect_handler_level=True)
    log_qlistener.start()
    return log_qlistener


def get_logger(name=APP_NAME):
    """
    Simple logging wrapper that returns logger
    configured to log into file and console.

    Args:
        name (str): name of logger

    Returns:
        logger (logging.Logger): configured logger
    """
    logger = logging.getLogger(name)
    for log_handler in logger.handlers[:]:
        logger.removeHandler(log_handler)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_qhandler)

    return logger


configure_handlers()
logger = get_logger()

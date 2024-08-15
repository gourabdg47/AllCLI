import os
import logging

# Ensure required directories exist
LOG_DIRECTORY = 'logs'
JOURNAL_DIRECTORY = 'journals'

def initialize_folders():
    for directory in [LOG_DIRECTORY, JOURNAL_DIRECTORY]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def setup_logging():
    info_handler = logging.FileHandler(os.path.join(LOG_DIRECTORY, 'app_info.log'))
    error_handler = logging.FileHandler(os.path.join(LOG_DIRECTORY, 'app_error.log'))

    info_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',
        datefmt='%Y-%m-%d %H:%M:%S %A'
    )

    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all logs

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    return logger

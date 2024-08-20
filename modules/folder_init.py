import os
import logging

from configs import config

# Directory constants
LOG_DIRECTORY = config.LOG_DIRECTORY
JOURNAL_DIRECTORY = config.JOURNAL_DIRECTORY
MISSION_DIR = config.MISSION_DIR

def initialize_folders():
    """Ensure required directories exist."""
    for directory in [LOG_DIRECTORY, JOURNAL_DIRECTORY, MISSION_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def setup_logging():
    """Setup logging configuration with info and error handlers."""
    initialize_folders()

    info_handler = logging.FileHandler(os.path.join(LOG_DIRECTORY, 'app_info.log'))
    error_handler = logging.FileHandler(os.path.join(LOG_DIRECTORY, 'app_error.log'))

    info_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all logs

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    return logger

# Initialize and configure the logger globally
logger = setup_logging()

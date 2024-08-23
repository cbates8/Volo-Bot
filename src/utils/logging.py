"""Logging Utils"""

import logging

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """Create a basic logger

    Args:
        name (`str`): Name of the logger. i.e. os.path.basename(__file__)

    Returns:
        `logging.Logger`: A logger with specified name and basic configuration
    """
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    return logging.getLogger(name)

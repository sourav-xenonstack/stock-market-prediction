"""
This files contains methods to create logger instances for logging
with the different logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
"""

# Import Dependencies
import logging

import logging

def create_logger(logger_name: str, log_file: str = 'logs/my_log_file.log') -> logging.Logger:
    """
    Creates a logger with the specified name and log file.

    :param logger_name: The name of the logger.
    :param log_file: The name of the file to write log messages to (default: 'logs/my_log_file.log').
    :return: The logger instance.
    """
    # create logger instance
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # change this to logging.DEBUG to see all log messages in the console

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


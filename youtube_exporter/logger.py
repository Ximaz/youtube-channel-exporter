import logging
import sys

def get_logger(log_file_path: str | None = None):
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    loggine_level = logging.INFO

    logger = logging.getLogger("YTCE")
    logger.setLevel(level=loggine_level)

    if isinstance(log_file_path, str):
        file_handler = logging.FileHandler(filename=log_file_path)
        file_handler.setLevel(level=loggine_level)
        file_handler.setFormatter(fmt=formatter)

        logger.addHandler(hdlr=file_handler)

    log_handler = logging.StreamHandler(stream=sys.stdout)
    log_handler.setLevel(level=loggine_level)
    log_handler.setFormatter(fmt=formatter)

    logger.addHandler(hdlr=log_handler)
    return logger
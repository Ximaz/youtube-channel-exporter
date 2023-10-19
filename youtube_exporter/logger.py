import logging
import sys

def get_logger(log_file_path: str | None = None):
    formatter = logging.Formatter("%(name)s - %(asctime)s - %(levelname)s - %(message)s")

    logger = logging.getLogger("YouTubeChannelExporter")
    logger.setLevel(logging.INFO)

    if isinstance(log_file_path, str):
        file_handler = logging.FileHandler(filename=log_file_path)
        file_handler.setLevel(level=logging.INFO)
        file_handler.setFormatter(fmt=formatter)

        logger.addHandler(hdlr=file_handler)

    log_handler = logging.StreamHandler(stream=sys.stdout)
    log_handler.setLevel(level=logging.INFO)
    log_handler.setFormatter(fmt=formatter)

    logger.addHandler(hdlr=log_handler)
    return logger
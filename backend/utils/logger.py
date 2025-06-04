import os
import logging

def get_logger(name="scraper"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        ch = logging.StreamHandler()

        log_file_path = os.path.join(log_dir, f"{name}.log")
        fh = logging.FileHandler(log_file_path)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

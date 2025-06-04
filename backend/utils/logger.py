import os
import logging

def get_logger(name="scraper"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True) 

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        ch = logging.StreamHandler()
        fh = logging.FileHandler(os.path.join(log_dir, "scraper.log"))
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

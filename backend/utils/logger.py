import os
import logging

def get_logger(name="scraper"):
    # Crea el logger 
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Manejador consola
        ch = logging.StreamHandler()

        # Manejador archivo
        ch.setLevel(logging.INFO)
        log_file_path = os.path.join(log_dir, f"{name}.log")
        fh = logging.FileHandler(log_file_path)

        # Formato del log
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        
        # Añade manejadores al logger
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

import logging


def setup_logger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a console handler
    handler = logging.StreamHandler()

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


logger = setup_logger()
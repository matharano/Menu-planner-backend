import os
import logging

LOGLEVEL = os.environ.get('LOGLEVEL')

def init_logging(name:str, log_level=LOGLEVEL):
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(module)-10s] %(message)s", datefmt='%d/%m/%Y %H:%M:%S')
    rootLogger = logging.getLogger(name)

    fileHandler = logging.FileHandler(f"{name}.log")
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.WARNING)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(log_level)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(log_level)
    return rootLogger

def get_log(name:str) -> logging.Logger:
    if logging.getLogger(name).hasHandlers():
        return logging.getLogger(name)
    else:
        return init_logging(name)
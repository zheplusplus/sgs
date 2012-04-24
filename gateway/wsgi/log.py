import logging

logging.basicConfig()
logger = logging.getLogger('sgs')
logger.setLevel(logging.INFO)

def i(msg):
    return logger.info(msg)

def w(msg):
    return logger.warning(msg)

def e(msg):
    return logger.error(msg)

def c(msg):
    return logger.critical(msg)

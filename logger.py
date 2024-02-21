import logging

logger = logging.getLogger(__name__)
def log_all():
    logger.debug('debug"')
    logger.info('info')
    logger.warning('warning!')
    logger.error('error!!')
    logger.critical('the end!!!')

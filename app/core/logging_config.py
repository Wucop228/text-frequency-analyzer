import sys
import logging

from loguru import logger

def setup_logging():
    logger.remove()
    logger.add(sys.stdout, format="{time:HH:mm:ss} | {level: <8} | {message}", level="INFO")

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            logger.opt(depth=6, exception=record.exc_info).log(
                record.levelname, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.WARNING, force=True)
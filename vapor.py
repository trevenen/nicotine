import logging
import logging.config
import vapor_modes

from typing import Optional

vapor_modes.configure()
logger = logging.getLogger(__name__)

def vapors(smoke: str, choke: Optional[Exception] = None):

    logger.debug(smoke)

    if choke:
        logger.error(choke, exc_info=True)

if __name__ == '__main__':
    vapors()

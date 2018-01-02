import logging
from migration import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(config.get('LOG', 'path'), mode='w', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

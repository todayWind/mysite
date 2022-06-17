import logging
import time
import os
from logging import handlers
from conf import settings


class LogHandler:

    def __init__(self):
        # 根据时间切
        self.fh = handlers.TimedRotatingFileHandler(filename=settings.LOG_PATH, when='D', interval=1, encoding='utf-8')
        self.sh = logging.StreamHandler()
        self.level = logging.INFO
        self.date_fmt = '%Y-%m-%d %H:%M:%S'
        self.format = '%(asctime)s - %(name)s[%(lineno)d] - %(levelname)s -%(module)s:  %(message)s'

    def log_fun(self):
        logging.basicConfig(level=self.level,
                            handlers=[self.sh, self.fh],
                            datefmt=self.date_fmt,
                            format=self.format)


if __name__ == '__main__':
    L = LogHandler()

#coding:utf-8

import time,os,sys
import logging
import logging.config
import traceback

_PATH = os.path.dirname(__file__)
_LogConfingFileName = os.path.join(_PATH,'logconfig.ini')
logging.config.fileConfig(_LogConfingFileName)


class Logger(object):
    def __new__(cls,name='root'):
         logger = logging.getLogger(name)
         return logger


if __name__ == '__main__':
    log = Logger()
    log.info('info')
    log.critical('critical')
    log.warn('warn')
    log.error('error')



#coding:utf-8

import time
import logging
import logging.config
import traceback

class LOG(object):
    _LogConfingFileName = 'logconfig.ini'
    def __new__(cls,name='root'):
        logging.config.fileConfig(cls._LogConfingFileName)
        logger = logging.getLogger(name)
        return logger

class LOG1(logging.getLoggerClass()):

if __name__ == '__main__':
    log = LOG()
    log.info('info')
    log.critical('critical')
    log.warn('warn')
    log.error('error')



#coding:utf-8
#日志
#


import time,os,sys
import logging
import logging.config
import traceback

__od = os.path.dirname
_PATH = __od(__od(os.path.abspath(__file__)))
os.chdir(_PATH)
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



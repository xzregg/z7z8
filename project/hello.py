#!/usr/bin/env python
#coding:utf-8
#项目开始布局
#https://github.com/bueda/tornado-boilerplate


#import tornado.autoreload

import time,os,sys

from tornado.options import define, options
import tornado.web
import tornado.httpserver


from url import URLS
from settings import SETTINGS

application = tornado.web.Application( handlers = URLS,
                                       **SETTINGS)

def single():
    application.listen(8888)
    #tornado.ioloop.PeriodicCallback(lee,3000).start()#增加后台任务
    tornado.ioloop.IOLoop.instance().start()

def mul():
    sockets = tornado.netutil.bind_sockets(8888)
    tornado.process.fork_processes(2)#不同逻辑阻塞时不同ip可以分到不同进程
    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    single()

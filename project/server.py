#!/usr/bin/env python
#coding:utf-8
#项目开始布局
#https://github.com/bueda/tornado-boilerplate


#import tornado.autoreload

import time,os,sys

from tornado.options import define, options
import tornado.web
import tornado.httpserver

from tornado.options import define, options, parse_command_line

from url import URLS
from settings import SETTINGS

define("port", default=9009, help="监听的端口", type=int)
define("process_num", default=1, help="开启的进程数,默认1", type=int)

application = tornado.web.Application( handlers = URLS,**SETTINGS)

def single():
    application.listen(options.port)
    #tornado.ioloop.PeriodicCallback(lee,3000).start()                   #增加后台任务
    tornado.ioloop.IOLoop.instance().start()

def mul():
    if SETTINGS.get('debug',''):
        print '请先关闭DEBUG'
    sockets = tornado.netutil.bind_sockets(options.port)
    tornado.process.fork_processes(options.process_num)                         
    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    print('start server: 0.0.0.0:%s' % options.port)
    if options.process_num >1:
        mul()
    else:
        single()
        

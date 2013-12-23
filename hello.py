#coding:utf-8


#import tornado.autoreload
import tornado.ioloop
import tornado.web
import time
import sys
import os
import logging
import tornado.options
import tornado.gen
from tornado.options import define, options
import threading
from tornado.concurrent import run_on_executor
import MySQLdb
import tornado.httpserver
import uuid

settings = {
    'debug': True,
    'template_path':os.path.join(os.path.dirname(__file__), "templates"),
    'static_path':os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret':'23123123'
}#开启debug模式自动重启


class testThread(threading.Thread):
    num = 0
    def __init__(self,j):
        super(testThread,self).__init__()
        self.setDaemon(True)
        self.j = j
        testThread.num += 1
    def run(self):
        for i in xrange(10):
                self.j.write('%s<br>' % i)
                time.sleep(1)
                self.j.flush()
        self.j.finish('ok')


from base.session import Session
from base import BaseHandler

class MainHandler(BaseHandler):
    #@tornado.gen.engine
    #@tornado.gen.coroutine
    #@tornado.web.asynchronous
    def get(self):
        #self.session['asd'] = dict(zip(range(100),[ str(i)*1440 for i in range(100)]))
        self.write('asd')
        #print self.cookies
        #self.set_cookie('asd','bbb')
        print self.session
        self.session['asad'] = {1:2}
        _k = self.get_argument('k','k')
        _v = self.get_argument('v','v')
        self.session[_k] = _v
        self.finish()
       # print testThread.num
        #self.render('test.html',locals())        #a = '--1'

    def callbacka(self,a='asd'):
        time.sleep(10)
        self.write('<html><body><form action="/" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
        self.finish()


application = tornado.web.Application([
    #(r'/',MainHandler),
    (r'/','hello.MainHandler'),
],**settings)

def lee():
    print 'lee 3s'

def sigle():
    tornado.options.parse_command_line()
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
    sigle()

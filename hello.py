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



settings = {'debug': True}#开启debug模式自动重启

sys.path.insert(0,os.path.dirname(__file__))

class testThread(threading.Thread):
    def __init__(self,j):
        super(testThread,self).__init__()
        self.setDaemon(True)
        self.j = j
    def run(self):
        for i in xrange(10):
                self.j.write('%s<br>' % i)
                time.sleep(1)
                self.j.flush()
        self.j.finish('ok')



class MainHandler(tornado.web.RequestHandler):

    #@tornado.web.asynchronous #取消自动finish
    #@tornado.gen.engine
    #@tornado.web.asynchronous
    #@tornado.gen.coroutine

    @tornado.web.asynchronous
    def get(self):
        args = self.get_argument('test','')
        if args == '123':
            t = testThread(self)
            t.start()
        else:
            self.finish('asd')


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
if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(8888)
    #tornado.ioloop.PeriodicCallback(lee,3000).start()#增加后台任务
    tornado.ioloop.IOLoop.instance().start()

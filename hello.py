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

settings = {'debug': True}#开启debug模式自动重启

sys.path.insert(0,os.path.dirname(__file__))
class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
            res = self.get_res()


    @tornado.web.asynchronous
    @tornado.gen.engine
    def get_res(self):
        print dir(self.request)
        print self.request.uri
        print

        #res  = yield tornado.gen.Task()
        #time.sleep(10)
        self.finish('123')

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
    tornado.ioloop.PeriodicCallback(lee,3000).start()#增加后台任务
    tornado.ioloop.IOLoop.instance().start()

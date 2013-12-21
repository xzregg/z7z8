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


settings = {
   'debug': True,
    'template_path':os.path.join(os.path.dirname(__file__), "templates"),
    'static_path':os.path.join(os.path.dirname(__file__), "static"),
}#开启debug模式自动重启

sys.path.insert(0,os.path.dirname(__file__))

def connetmysql():
    con = MySQLdb.connect(host='127.0.0.1',passwd='123456',db='aa')
    cur = con.cursor()
    cur.execute('select * from bb;')
    return cur.fetchall()

def baidu():
    print 'connect baidu'
    h=httplib.HTTPConnection('www.baidu.com:81')
    h.request('GET','/','')
    r=h.getresponse()
    r.read()

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


class BaseHandler(tornado.web.RequestHandler):
    def render(selfb,template_name,__d={},**kwargs):
            __d = __d or kwargs
            __d.pop('self',0)
            super(BaseHandler,selfb).render(template_name,**__d)

    def initialize(self):
        #print 'initialize' + '-' * 40
        #print self.get_argument('test','')
        #print dir(self.request.cookies)
        self._st = time.time()
        self.log = None
    #所有方法
    def prepare(self):
        #print 'prepare' + '-' * 40
        #print self.get_argument('test','')
        self.session = {'asd':123}
       # print dir(self.request)

    def on_finish(self):
        if self.log:
            print 'log'+'-'*40
        #print 'use time:%s' % (time.time() - self._st)

class MainHandler(BaseHandler):
    #@tornado.web.asynchronous #取消自动finish
    #@tornado.gen.engine
    #@tornado.web.asynchronous
    #@tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self):
        #args = self.get_argument('test','')
        #t = testThread(self)
        #t.start()
        self.write(str(connetmysql()))
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
if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(8888)
    #tornado.ioloop.PeriodicCallback(lee,3000).start()#增加后台任务
    tornado.ioloop.IOLoop.instance().start()

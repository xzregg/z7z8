#coding:utf-8


import sys,os,time,datetime,uuid
import tornado.escape
import tornado.web


from base.session import Session

class BaseHandler(tornado.web.RequestHandler):

    #转马相关
    escape = tornado.escape

    def render(selfb,template_name,__d={},**kwargs):
            __d = __d or kwargs
            __d.pop('self',0)
            super(BaseHandler,selfb).render(template_name,**__d)

    def get_session_id(self):
        sid = self.get_secure_cookie('sid')
        if not sid:
            sid =  uuid.uuid4().get_hex()
            self.set_secure_cookie('sid',sid)
        #print sid
        return sid
    def initialize(self):
        #print 'initialize' + '-' * 40
        #print self.get_argument('test','')
        self.session = Session(self.get_session_id())
        #print self.cookies
        #print self.request
        #print self.get_secure_cookie('sid','ooooo',)
        #print dir(self.request)
        #print self._headers
        #print self.request.headers
        self._st = time.time()
        self.log = None

    def prepare(self,*args,**kwargs):#开始都会运行
        print 'prepare' + '-' * 40
        #print self.get_argument('test','')
       # print dir(self.request)

    def on_finish(self):#结束都会运行
        if self.log:
            print 'log'+'-'*40
        #print 'use time:%s' % (time.time() - self._st)
        self.session.save()

import threading
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


from base.log import Logger
from url import AutoUrl

@AutoUrl.route('^/test/(?P<id>.*)')
class test(BaseHandler):
    def get(self,id):
        L = Logger('bb')
        L.info('asdasdasd')
        self.url = '----------'
        self.write('123')
        self.write('%f'%self.request.request_time())
        self.render('test.html',locals())
    def on_finish(self):
        print('<br>%f[%s]'%(self.request.request_time(),self._request_summary()))
        super(BaseHandler,self).on_finish()
        
@AutoUrl.route('^/route')
class route(BaseHandler):
    def get(self):
        for line in AutoUrl.Handlers:
            self.write(self.escape.xhtml_escape(str(line))+'<br>')

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

    def callback(self,a='asd'):
        time.sleep(10)
        self.write('<html><body><form action="/" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
        self.finish()


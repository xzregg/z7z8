#coding:utf-8


import sys,os,time,datetime,uuid
import tornado.escape
import tornado.web
from settings import DEBUG
from base.session import Session
from base.log import Logger
from url import AutoUrl

class BaseHandler(tornado.web.RequestHandler):
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
        self.session = Session(self.get_session_id())
        if DEBUG:
            print 'initialize' + '-' * 40
            #print self.cookies
            #print self.request
            #print self._headers
            print self.request.headers
        self._st = time.time()
        self.log = DEBUG

    def prepare(self,*args,**kwargs):#开始都会运行
        print 'prepare' + '-' * 40


    def on_finish(self):#结束都会运行
        if self.log:
            print 'log'+'-'*40
        self.session.save()


@AutoUrl.route('^/test/(?P<id>.*)')
class test(BaseHandler):
    def get(self,id):
        L = Logger('bb')
        L.info('asdasdasd')
        self.url = '----------'
        self.write('123')
        self.write('%f'%self.request.request_time())
        self.write('<br>%f[%s]'%(self.request.request_time(),self._request_summary()))
        self.render('test.html',locals())
    def on_finish(self):
        
        super(BaseHandler,self).on_finish()
        
@AutoUrl.route('^/route')
class route(BaseHandler):
    def get(self):
        for line in AutoUrl.Handlers:
            self.write(self.escape.xhtml_escape(str(line))+'<br>')




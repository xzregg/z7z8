#coding:utf-8

import sys,os,time,datetime
import uuid
import tornado.web
from session import Session

class BaseHandler(tornado.web.RequestHandler):
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

    def prepare(self):#开始都会运行
        print 'prepare' + '-' * 40
        #print self.get_argument('test','')
       # print dir(self.request)

    def on_finish(self):#结束都会运行
        if self.log:
            print 'log'+'-'*40
        #print 'use time:%s' % (time.time() - self._st)
        self.session.save()
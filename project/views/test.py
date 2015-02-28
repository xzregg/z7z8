#coding:utf-8


import sys,os,time,datetime,uuid
import tornado.escape
import tornado.web
from views import BaseHandler
from settings import DEBUG
from base.session import Session
from base.log import Logger
from url import AutoUrl

@AutoUrl.route('^/phone[/]?$')
class phone(BaseHandler):
    def get(self):
        self.render('phone.html',locals())

    def post(self,*args,**kwargs):
        return self.get(*args,**kwargs)


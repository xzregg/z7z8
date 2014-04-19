#!/usr/bin/env python
#coding:utf-8
#消息服务器
#

import time,datetime,os,sys
import traceback


from tornado.options import define, options
import tornado.web
import tornado.httpserver
import MySQLdb
import json
import base64
import Queue
import threading
import traceback
import hashlib
import urllib
import tornado.ioloop
import tornado.options
import tornado.httpserver
import functools
import re

from settings import SETTINGS,SIGN_KEY


def get_day_str():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def md5(_str):
    return hashlib.new('md5', _str).hexdigest()


class MessageStore(dict):
    
    def __init__(self,*ar,**kw):
        super(MessageStore,self).__init__(*ar,**kw)

    def __getitem__(self,key):
        if not self.has_key(key):
            super(MessageStore,self).__setitem__(key,set())
        return super(MessageStore,self).__getitem__(key)

            
    def save_html(self,key,html):
        _day_str = get_day_str()
        #file_name = '%s_%s.html' % (key,md5(key+html))
        file_name = '%s.html' %  re.sub(r'\r|\n|\t','',key)
        save_dir = os.path.join(SETTINGS['static_path'],_day_str)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir,mode=0744)
        save_path = os.path.join(save_dir,file_name)
        if not os.path.exists(save_path):
            with  open(save_path,'wb') as fp:
                fp.write(html)
        return '%s/%s' % (_day_str,file_name)

MSG_STORE = MessageStore()

class MessageHandler(tornado.web.RequestHandler):
    def initialize(self):
        self._m = MSG_STORE
         
    def post(self,action):
        return self.get(action)
    
    def check_sign(self):
        '''
        @检查签名 md5(msg,timestmap,SIGN_KEY)
        '''
        if self._k['msg']:
            sign_str = md5('%s%s%s' % (self._k['msg'],self._k['timestmap'],SIGN_KEY))
        print sign_str
        return sign_str == self._k['sign'].encode('utf-8')
 

    def get(self,action):
        keys = ['timestmap','sign','msg','html','to','clear']
        self._k = {}
        for k in keys:
            self._k[k] = self.get_argument(k,'').encode('utf-8','ignore')

        if action == 'get':
            self.get_msg()
        elif action == 'post':
            self.save_msg()
            
    def get_msg(self):
        _msg = '\n'.join(self._m[self._k['to']])
        if self._k['clear']:
            self._m[self._k['to']] = set()
        self.write(_msg)
            
    def save_msg(self):
        if not self.check_sign():
            self.write('sign err!')
            return 
        _msg = self._k['msg']
        if self._k['html']:
            _path = self._m.save_html(self._k['msg'], self._k['html'])
            html_static_url = self.static_url(_path,include_host=True)
            html_static_url = urllib.splitquery(html_static_url)[0]
            _msg += '\nDetails:%s' % html_static_url
            self.write('<a href="%s"> %s </a>' % (html_static_url,html_static_url))

        tolist = [ _to for _to in self._k['to'].split(',') if _to] if ',' in self._k['to'] else [self._k['to']]
        for _to in tolist:
            if _to:
                _m_q = self._m[_to]
                _m_q.add(_msg)
                    
        self.write('MSG_STORE size:%s' % str(MSG_STORE.__sizeof__()))
        
    def get_self_access_address(self):
        return '%s://%s' % (self.request.protocol,self.request.host)   
     
        
        
application = tornado.web.Application( handlers = [(r'/msg/(\w+)[/]?$',MessageHandler),
                                                   ],
                                       **SETTINGS)
SERVER_PORT = 11111
def single():
    application.listen(SERVER_PORT)
    #tornado.ioloop.PeriodicCallback(lee,3000).start()#增加后台任务
    tornado.ioloop.IOLoop.instance().start()

def mul():
    sockets = tornado.netutil.bind_sockets(SERVER_PORT)
    tornado.process.fork_processes(2)#不同逻辑阻塞时不同ip可以分到不同进程
    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    print 'listen port %s' % SERVER_PORT
    single()

#!/usr/bin/env python
#coding:utf-8
#项目开始布局
#https://github.com/bueda/tornado-boilerplate


#import tornado.autoreload

import time,os,sys

from tornado.options import define, options
import tornado.web
import tornado.httpclient
import tornado.httpserver
import urllib,urllib2
from  tornado.template import Template

SETTINGS = {
    'debug': True,
    'template_path':os.path.join(os.path.dirname(__file__), "templates"),
    'static_path':os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret':'23123123',
    "gzip" : True,
}#开启debug模式自动重启

template='''
<form action='/' method="post">
输入网址:<input name="url" type="text" style="width:60%" value="{{url}}"><br>
输入post参数:<br><textarea name="params" style="width:600px;height:200px" >{{params}}</textarea>
<input type="submit" value="提交">
</form>
<br>返回:
<hr>
{{r}}
'''
import hashlib,re

def md5(_str):
    m = hashlib.md5()
    m.update(_str)
    return m.hexdigest()
app_key = '_h0en5ftwx;ohmw#_dcl'

class TestPost(tornado.web.RequestHandler):
    def get(self):
        self.write(template)
        
    def post(self):
        print dir(self.request)
        url = self.get_argument('url','')
        params = self.get_argument('params','')
        if url and params:
            _p = re.sub('\n|\r|&','',params)+app_key
            print _p
            sign = md5(_p)
            t = Template(template)
            r = urllib2.urlopen(url,params+'&sign='+sign)
            r = r.read()
            self.write(t.generate(url=url,params=params,r=r))
            self.write('<br>')
            self.write(sign)
        
application = tornado.web.Application([(r'/',TestPost)],
                                       **SETTINGS)

def single():
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
    tornado.options.parse_command_line()
    single()

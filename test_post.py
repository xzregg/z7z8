#!/usr/bin/env python
#coding:utf-8
#https://github.com/bueda/tornado-boilerplate
#用来模拟post参数的

#import tornado.autoreload

import time,os,sys
from tornado.options import define, options
import tornado.web
import tornado.httpclient
import tornado.httpserver
import urllib,urllib2,urlparse
from  tornado.template import Template
import tornado.httpclient
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import tornado.util
from tornado.util import ObjectDict
from tornado.escape import json_decode, json_encode
import traceback


define("port", default=9888, help="监听的端口", type=int)
define("process_num", default=1, help="开启的进程数,默认1", type=int)

SETTINGS = {
    'debug': True,
    'template_path':os.path.join(os.path.dirname(__file__), "templates"),
    'static_path':os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret':'23123123',
    "gzip" : True,
}#开启debug模式自动重启

_template='''
<form action='/' method="post">
输入网址:<input name="url" type="text" style="width:60%" value="{{ url}}">
<br>
<label><input type="checkbox" name="django_request" vlaue="1" {% if is_django_params_type%}checked="checked"{%end%}>是django Request对象</label>
<br>
输入post参数:<br><textarea name="params" style="width:600px;height:200px" >{{ params }}</textarea>
<input type="submit" value="提交">
</form>
<br>返回:
<hr>
{{r}}
'''

import hashlib,re
import json

def md5(_str):
    m = hashlib.md5()
    m.update(_str)
    return m.hexdigest()
app_key = '_h0en5ftwx;ohmw#_dcl'

class TestPost(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        return self.post()

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        t = Template(_template)
        url = self.get_argument('url','')
        params = self.get_argument('params','')
        is_django_params_type = self.get_argument('django_request','')

        r = ''
        if url:
            method_str = 'POST' if params else 'GET'
            req = tornado.httpclient.HTTPRequest(url=url,
                                                 method=method_str
            )
            
            if params:
                post_data =  params.encode('utf-8')
                if is_django_params_type:
                    try:
                        post_data = post_data
                        post_data_dict = eval(post_data)
                        print post_data_dict
                        if isinstance(post_data_dict,dict):
                            for k in post_data_dict.keys():
                                post_data_dict[k] = post_data_dict[k].encode('utf-8') if isinstance( post_data_dict[k],unicode) else post_data_dict[k]
                        post_data = urllib.urlencode(post_data_dict)
                    except:
                        traceback.print_exc()
                        
                req.body = post_data
                
            print '-' * 40
            print req.url
            print req.body
            
            http_client = tornado.httpclient.AsyncHTTPClient()
            r = yield gen.Task(http_client.fetch, req)
            print '=' * 40
            r = r.body
        self.write(t.generate(url=url,params=params,r=r,is_django_params_type=is_django_params_type))
        self.write('<br>')
        self.finish()

        
application = tornado.web.Application([(r'/.*',TestPost)],
                                       **SETTINGS)

def single():
    print options.port
    application.listen(options.port )
    #tornado.ioloop.PeriodicCallback(lee,3000).start()#增加后台任务
    tornado.ioloop.IOLoop.instance().start()

def mul():
    sockets = tornado.netutil.bind_sockets(options.port )
    tornado.process.fork_processes(2)#不同逻辑阻塞时不同ip可以分到不同进程
    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    single()

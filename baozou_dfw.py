#!/usr/bin/env python
#coding:utf-8
#用来模拟post参数的

import sys
import socket

from tornado.options import define, options
import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpclient
import json
import tornado.web
import tornado.gen
import hashlib
import urllib
from tornado.web import url,StaticFileHandler
import mongoengine
from mongoengine import Document,fields
import datetime,time
import traceback
import os



define("port", default=9888, help="监听的端口", type=int)
define("process_num", default=1, help="开启的进程数,默认1", type=int)

SETTINGS = {
    'debug': True,
    'template_path':os.path.join(os.path.dirname(__file__), "templates"),
    'static_path':os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret':'23123123',
    "gzip" : True,
}

DBNAME = 'dfw'
MONGO_DATABASES = [
    {'host':'127.0.0.1','port': 17000},
]


class DateEncoder(json.JSONEncoder ):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.strftime('%Y-%m-%d %H:%M:%S')   
    return json.JSONEncoder.default(self, obj)

def json_dumps(obj):
    return json.dumps(obj,ensure_ascii = False,cls=DateEncoder)


class User(Document):
    DEFUALT_DATA = {
        'avatar':'',
        'uname':''
    }        
    
    uid = fields.StringField(max_length = 100, verbose_name="uid",unique=True, required= True)  
    data = fields.DictField(verbose_name="玩家数据",default={})
    
    
    uname = fields.StringField(max_length = 100, verbose_name="名字")  
    cid = fields.StringField(max_length = 100, verbose_name="cid")  
    platformInfo = fields.DictField(verbose_name="平台信息",default={})  
    wealth = fields.IntField(verbose_name="财富",default=1000)  
    gem = fields.IntField(verbose_name="宝石",default=1)    
    money = fields.IntField(verbose_name="钱",default=100)
    buildList = fields.DictField(verbose_name="建筑列表")
    avatar = fields.StringField(max_length = 200, verbose_name="图片化身")  
    login_num = fields.IntField(verbose_name="登录参数",default=0)    
    last_time = fields.DateTimeField(default = datetime.datetime.now,verbose_name="最后时间")
    create_time = fields.DateTimeField(default = datetime.datetime.now,verbose_name="创建时间")
    ip = fields.StringField(max_length = 50, verbose_name="ip")  
    
    @classmethod
    def get_or_create(cls,*args,**kwargs):
        created = False
        try:
            o = cls.objects.get(*args,**kwargs)
        except:
            o = cls(*args,**kwargs)
            o.save()
            traceback.print_exc()
            created = True
        return o,created
    
    @classmethod
    def load_new_player_data(cls):
        try:
            with open('newPlayer.json','rb') as fp:
                plater_data_str = fp.read()
                player_data = json.loads(plater_data_str)
                cls.DEFUALT_DATA.update(player_data)
        except:
            traceback.print_exc()
            
def md5(_s):
    return hashlib.new('md5',str(_s)).hexdigest()

User.load_new_player_data()
class BaoZouHandler(tornado.web.RequestHandler):
    '''暴走漫画的api
    '''
    APP_NAME = '大富翁'
    CLINET_ID = '20230303'
    SECRET_KEY = '6bef6c7d4c7a68f4a341d43737f267e9'
    API_ADDRESS = "http://api.ibaozou.com"
    
   
    def generate_post_data(self):
        self.data = {}
        try:
            json_data_str = self.request.body
            self.data = json.loads(json_data_str)
        except:
            pass
    def finish(self,*arge,**kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        super(BaoZouHandler,self).finish(*arge,**kwargs)
    
    @tornado.web.asynchronous
    def get(self):
        self.generate_post_data()
        action_name = self.data.get('actionType', '')
        
        if action_name == 'load':
            self.load_user_info()
        elif action_name == 'save':  
            self.save_user_info()
        else:
            
            self.finish('actionType error')
    
    def __test_async(self):
        url = 'http://api.ibaozou.com/api/v2/users/dfw_show?access_token=dce46ff4d6446ff76c8ad3e5bbee8b22cbbc0662&timestamp=1438050033&user_id=26679416&client_id=20230303&sign=3f5fcb48a340919a901582c08271f95c'   
        client = tornado.httpclient.AsyncHTTPClient()
        try:
            print url
            request = tornado.httpclient.HTTPRequest(url,connect_timeout=10,request_timeout=10)
            client.fetch(request,self.load_user_info_on_response)
        except tornado.httpclient.HTTPError, x:
            self.load_user_info_on_response(x)
        except:
            traceback.print_exc()
        client.close()
        
    def load_user_info(self):
        uri = '/api/v2/users/dfw_show'
        data = {}
        uid = str(self.data.get('user_id',''))
        data['client_id'] = self.CLINET_ID
        data['user_id'] = uid
        data['access_token'] = self.data.get('access_token','')
        if data['user_id'] and data['access_token']:
            data['timestamp'] = str(int(time.time()))
            sign = self.get_sign(data)
            data['sign'] = sign
            url = '%s%s' % (self.API_ADDRESS,uri)
            query_data = urllib.urlencode(data)
            url = '%s?%s' % (url,query_data)

            
            #如果第一次就去访问api
            self.user,created = User.get_or_create(uid = uid)
            if  created:
                client = tornado.httpclient.AsyncHTTPClient()
                try:
                    print url
                    request = tornado.httpclient.HTTPRequest(url,
                                                             headers = {'Connection':'keep-alive'},
                                                             connect_timeout=10,
                                                             request_timeout=10)
                    client.fetch(request,self.load_user_info_on_response)
                except tornado.httpclient.HTTPError, x:
                    traceback.print_exc()
                    self.load_user_info_on_response(x)
                except:
                    traceback.print_exc()
            else:
                self.finish(json_dumps(self.user.data))
                
        else:
            self.finish('not user_id')
            
    def load_user_info_on_response(self, x):
        _r = {
              'msg':"error"
              }
        if hasattr(x, "response") and x.response:
            response = x.response
        else:
            response = x
        print x,type(x)
        if hasattr(response,'body'):
            try:
                body_str = response.body
                print '*' * 40
                print body_str
                print '*' * 40
                user_data = json.loads(body_str)
                self.set_status(response.code)
                user_info = user_data.get('user',{})
                if user_info:
                    uid = str(user_info['user_id'])
                    self.user.data.update(User.DEFUALT_DATA) 
                    self.user.data['uid'] = uid
                    self.user.data['uname'] = user_info['user_name']
                    self.user.data['avatar'] = user_info['avatar']
                    self.user.ip = self.request.remote_ip
                    self.user.login_num += 1
                    self.user.last_time = datetime.datetime.now()
                    self.user.save()
                    _r.update(self.user.data)
                    _r['msg'] = ''
            except Exception,e:
                traceback.print_exc()
                _r['msg'] = str(e)
        self.finish(json_dumps(_r))
        
    def save_user_info(self):
        _r = {
              "actionType" : "save",
              "result" : "fail"
              }
        try:
            user_data = self.data.get('data',{})
            uid = str(self.data.get('user_id',''))
            if uid:
                u,created = User.get_or_create(uid = uid)
                u.data = user_data
                u.save()
                _r['result'] = "success"
        except Exception,e:
            _r['result'] = str(e)
        self.finish(json_dumps(_r))
        
    
    def post(self):
        return self.get()
    

    def get_sign(self,_d):
        sign_str = ''.join([ '%s=%s' % (k,_d[k]) for k in sorted(_d.keys())])
        sign_str = '%s%s' % (sign_str,self.SECRET_KEY)
        sign_str = urllib.quote(sign_str)
        return md5(sign_str)
    
def init_mongoengine():
    hosts = []
    for item in MONGO_DATABASES:
        hosts.append('%s:%s'% (item['host'], item['port']))
    
    print '-' * 40,'init mongoengine connect!'
    mongoengine.register_connection('default', DBNAME, host=','.join(hosts))
    
    
    
init_mongoengine()
application = tornado.web.Application([
        (r"^/dfw/(.*)", StaticFileHandler, {"path":'./dwf'}),
        (r'^/action[/]?$', BaoZouHandler)
                                       ],
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

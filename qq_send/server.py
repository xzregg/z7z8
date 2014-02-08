#!/usr/bin/env python
#coding:utf-8
#window QQ发送信息

import time,datetime,os,sys
from tornado.options import define, options
import tornado.web
import tornado.httpserver
import json
import Queue
import threading
import traceback
try:
    import cPickle as  pickle
except:
    traceback.print_exc()
    import pickle

from settings import SETTINGS



class ParamsStorage(object):
    '''
    @参数存储
    '''
    __file = os.path.join(os.path.dirname(__file__),'Storage.dict')
    def __init__(self):
        pass
    def save(self,_dict):
        with open(self.__file,'wb') as fp:
            pickle.dump(_dict,fp, protocol)
    
    def get(self):
        try : 
            with open(self.__file,'rb') as fp:
                return pickle.load(fp)
        except:
            traceback.print_exc()
            return []
        

class QQHandler(tornado.web.RequestHandler):
    def get(self):
        keys = ['action','qq_cmd']
        self.d = d = {}
        for k in keys:
            d[k] = self.get_argument(k,'')
        
        if hasattr(self,d['action']):
            return apply(getattr(self,d['action']))
              
        params = {"url":'',
                  "md5":'',
                  "interval":'',
                  "qq_title":'',
                  "qq_cmd":'',
                  }
        self.render('index.html',**params )
        
    def start_cmd(self):
        '''开个线程启动系统命令'''
        
        _t = threading.Thread(target=os.system,args=(self.d['qq_cmd'],))
        _t.setDaemon(True)
        _t.start()
        self.write('start_qq_cmd:[%s] OK' % self.d['qq_cmd'])
    
    def post(self):
        return self.get()


application = tornado.web.Application( handlers = [(r'/',QQHandler),
                                                   #(r"/static/(.*)", tornado.web.StaticFileHandler, {"path":SETTINGS['static_path']})
                                                   ],
                                       **SETTINGS)

def single():
    application.listen(22222)
    #tornado.ioloop.PeriodicCallback(lee,3000).start()#增加后台任务
    tornado.ioloop.IOLoop.instance().start()

def mul():
    sockets = tornado.netutil.bind_sockets(22222)
    tornado.process.fork_processes(2)#不同逻辑阻塞时不同ip可以分到不同进程
    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    single()

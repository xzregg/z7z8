#coding:utf-8

import urllib
import urllib2
import tornado
import sys  
    
import os

sys.setdefaultencoding('gb2312')  

url = 'http://www.baidu.com'

rsp = urllib2.urlopen(url)
print rsp.read()


print '-' * 40
print __name__

ss = raw_input(u'输入参数')
print ss


print os.path.join(os.path.dirname(__file__),'Storage.dict')

a = raw_input()



print u'start tornado server!'

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])





import time,datetime,os,sys
from tornado.options import define, options
import tornado.web
import tornado.httpserver
import json
import Queue
import threading
import traceback
import platform
import mimetypes
import hashlib
import urllib

#SYSTEMCODING = sys.getdefaultencoding() 
SYSTEMCODING = 'gb2312'


  
#if platform.system() == 'Windows':
import win32gui
import win32con
import win32api
import win32clipboard as w  
if sys.getdefaultencoding() != 'gbk':
        reload(sys)
        sys.setdefaultencoding('gbk')
try:
    import cPickle as  pickle
except:
    traceback.print_exc()
    import pickle

from settings import SETTINGS,SIGN_KEY

import urllib2,urllib
import threading
    
SIGN_KEY = 'oaksodqweack123'






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
import platform
import mimetypes
import hashlib
import urllib

#SYSTEMCODING = sys.getdefaultencoding() 
SYSTEMCODING = 'gb2312'


  
#if platform.system() == 'Windows':
import win32gui
import win32con
import win32api
import win32clipboard as w  
if sys.getdefaultencoding() != 'gbk':
        reload(sys)
        sys.setdefaultencoding('gbk')
try:
    import cPickle as  pickle
except:
    traceback.print_exc()
    import pickle

from settings import SETTINGS,SIGN_KEY

import urllib2,urllib
import threading
    
SIGN_KEY = 'oaksodqweack123'
    
def get_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def md5(_str):
    return hashlib.new('md5',_str).hexdigest()
class Clipboard:
    '''
    @粘贴板
    '''
    @classmethod
    def getText(cls):  
        w.OpenClipboard()  
        d = w.GetClipboardData(win32con.CF_TEXT)  
        w.CloseClipboard()  
        return d
    @classmethod
    def setText(cls,aString):  
        w.OpenClipboard()  
        w.EmptyClipboard()  
        w.SetClipboardData(win32con.CF_TEXT, aString)  
        w.CloseClipboard()




class MailSender(object):
    '''
    @邮件发送
    '''
    pass


  
EXAMPLE_PARAM = {"url":'',
          "auto_on":'',
          "app_key":'',
          "interval":'60',
          "qq_title":'',
          "qq_cmd":'',
          "use_clipboard":'',
          "use_ctrl":'on'
                  }

class QQSender(object):
    '''
    @QQ发送者
    '''
    def __init__(self,_p):
        self._p = _p
        self.qq_title = _p.get('qq_title')
        self.qq_cmd = _p.get('qq_cmd')
        self.use_clipboard = _p.get('use_clipboard','')
        self.handle = self.get_qwindow_handle()
        
    def get_qwindow_handle(self):
        for _ in xrange(3):
            handle = win32gui.FindWindow(None,  self.qq_title)
            if handle:
                return handle
            else:
                QQSender.start_qqcmd(self.qq_cmd)
                time.sleep(1)
    
    @staticmethod
    def start_qqcmd(target):
        '''开个线程启动系统命令'''
        target = target 
        _t = threading.Thread(target=os.system,args=(target,))
        _t.setDaemon(True)
        _t.start()
    
    
    def send_enter(self):
        if self._p.get('use_ctrl',''):
            win32api.keybd_event(17,0,0,0)#ctrl键位码是17  
            win32gui.SendMessage(self.handle, win32con.WM_KEYDOWN, win32con.VK_RETURN)
            win32gui.SendMessage(self.handle, win32con.WM_KEYUP, win32con.VK_RETURN)
            win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP)
        else:
            win32gui.SendMessage(self.handle, win32con.WM_KEYDOWN, win32con.VK_RETURN)
            win32gui.SendMessage(self.handle, win32con.WM_KEYUP, win32con.VK_RETURN)


    
    def _send_msg(self,msgs):
        msgs = msgs.encode(SYSTEMCODING)
        if self.use_clipboard:
            Clipboard.setText(msgs)
            win32gui.SendMessage(self.handle,win32con.WM_PASTE,0,0)
        else:
            for c in msgs:
                    #print (repr(c),ord(c))
                    if c == '\n':
                        win32gui.SendMessage(self.handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                        win32gui.SendMessage(self.handle, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
                    else:
                        win32gui.SendMessage(self.handle,win32con.WM_CHAR,ord(c),0)
        time.sleep(0.3)
        self.send_enter()

    def send_msg(self,msgs):
        max_num = 1000#qq最多1024
        msg_len = len(msgs)
        extra_step = 1 if msg_len % max_num else 0
        for i in xrange(msg_len / max_num+extra_step):
            msg = msgs[i*max_num:i*max_num+max_num]
            self._send_msg(msg)
        time.sleep(1)

       
class HttpMsgInstance(threading.Thread):
    '''
    @线程消息实例
    '''
    def __init__(self,MessageManager,params,lock):
        super(HttpMsgInstance,self).__init__()
        self.setDaemon(True)
        self.ms = MessageManager
        self.interval = int(params.get('interval',60))
        self.senders = {'QQ':QQSender
                        #'Mail':MailSender
                        }
        self.lock = lock
        self.p = params
        self.on = True
        self.curl_url = HttpMsgInstance.curl_url

    @staticmethod
    def curl_url(url=""):
        _r = ''
        try:
            _r = urllib2.urlopen(url,timeout=5).read()
        except Exception,e:
            traceback.print_exc()
            _r = str(e)
        return _r   


    def send_msg(self,msg):
        try:
            self.lock.acquire()
            for n,s in self.senders.items():
                    if self.p.get('auto_on',''):
                        sender = s(self.p)
                        sender.send_msg(msg)
                          
        except Exception,e:
            traceback.print_exc()
        finally:          
            self.lock.release() 
            
    def run(self):
        while self.on:
            time.sleep(int(self.p.get('interval',60))) 
            if self.ms.on and self.p.get('auto_on',''):
                    print '[%s] - curl url - %s' % (get_now(),self.p.get('url'))
                    msg = self.curl_url(self.p.get('url','')).decode('utf-8')
                    if msg:
                        self.send_msg(msg)
            
            
class MessageManager(threading.Thread):
    def __init__(self):
        super(MessageManager,self).__init__()
        self.setDaemon(True)
        self.ps = ParamsStorage()
        self.lock = threading.Lock()
        self.instance_map = []
        self.on = False
        

       
    @property
    def params(self):
        return  self.ps.params
    
    def save_params(self,index,data):
        if  index+1 > len(self.params) :
            self.params.append(data)
            self.start_instance(data)
        else:
            self.params[index] = data
            self.instance_map[index].p = data
        self.ps.save()
    
    def start_instance(self,p):
        _t = HttpMsgInstance(self,p,self.lock)
        self.instance_map.append(_t)
        _t.start()
        
    def run(self):
        for i,p in enumerate(self.params):
            self.start_instance(p)
            
    def send_msg(self,msg):
        for s in self.instance_map:
            print s
            s.send_msg(msg)
    
    def del_params(self,index):
        if index < self.params.__len__():
            self.params.pop(index)
            self.instance_map[index].on = False
            self.instance_map[index].join()
            self.instance_map.pop(index)
            self.ps.save()

            
                


class MessageHandler(tornado.web.RequestHandler):
    
    def prepare(self):
        pass
    
    def post(self):
        return self.get()
    
    def get(self):
        keys = ['action','qq_cmd']
        self.d = d = {}
        for k in keys:
            d[k] = self.get_argument(k,'')
        
        if hasattr(self,d['action']):
            return apply(getattr(self,d['action']))
        params = Ms.params
        self.render('index.html',params=params,daemon_start=Ms.on)
    
    
    def curl_url(self):
        url = self.get_argument('url','')
        if url:
            response = HttpMsgInstance.curl_url(url)
            self.write(response)
        else:
            self.write('not url')
            
    def save_params(self):
        '''
        @保存参数
        '''
        _d = {}
        index = int(self.get_argument('index','0'))
        for k,v in self.request.arguments.iteritems():
            _d[k] = v[0]
        Ms.save_params(index,_d)
        self.write('成功！')
        
    def del_params(self):
        index = int(self.get_argument('index','0'))
        Ms.del_params(index)
        self.redirect('/')
        
    def send_msg(self):
        msg = self.get_argument('msg','')
        if msg:
            Ms.send_msg(msg)
            self.write('成功!')
        else:
            self.write('没有消息！')
            
    def start_cmd(self):
        QQSender.start_qqcmd(self.d['qq_cmd'])
        self.write('start_qq_cmd:[%s] OK' % self.d['qq_cmd'])
        

    def daemon(self):
        is_start = self.get_argument('start', '')
        if is_start:
            Ms.on = True
        else:
            Ms.on = False
        self.redirect('/')
        
application = tornado.web.Application( handlers = [(r'/',MessageHandler),
                                                   #(r"/static/(.*)", tornado.web.StaticFileHandler, {"path":SETTINGS['static_path']})
                                                   ],
                                       **SETTINGS)
SERVER_PORT = 22222
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


    
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

#SYSTEMCODING = sys.getdefaultencoding() 
SYSTEMCODING = 'gb2312'
if platform.system() == 'Windows':
    import win32gui
    import win32con
    import win32api
    import win32clipboard as w  
try:
    import cPickle as  pickle
except:
    traceback.print_exc()
    import pickle

from settings import SETTINGS

import urllib2,urllib
import threading
    
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
    @发邮件
    '''
    pass


  
EXAMPLE_PARAM = {"url":'',
          "auto_on":'',
          "app_key":'',
          "interval":'',
          "qq_title":'',
          "qq_cmd":'',
          "use_clipboard":'',
          "use_ctrl":'on'
                  }

class QQSender(object):
    '''
    @发到qq
    '''
    def __init__(self,_p):
        self.on = _p['auto_on']
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
            win32gui.SendMessage(self.handle, win32con.WM_KEYDOWN, win32con.VK_RETURN,0)
            win32gui.SendMessage(self.handle, win32con.WM_KEYUP, win32con.VK_RETURN,0)
            win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
        else:
            win32gui.SendMessage(self.handle, win32con.WM_KEYDOWN, win32con.VK_RETURN,0)
            win32gui.SendMessage(self.handle, win32con.WM_KEYUP, win32con.VK_RETURN,0)


    
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
        time.sleep(0.5)
        self.send_enter()

    def send_msg(self,msgs):
        max_num = 1000#qq最多1024
        msg_len = len(msgs)
        extra_step = 1 if msg_len % max_num else 0

        for i in xrange(msg_len / max_num+extra_step):
            msg = msgs[i*max_num:i*max_num+max_num]
            self._send_msg(msg)
            
        time.sleep(1)

class ParamsStorage(object):
    '''
    @参数存储
    '''
    __file = os.path.join(os.path.dirname(__file__),'Storage.dict')
    def __init__(self):
        self.params = self.get()
    
    def save(self):
        with open(self.__file,'wb') as fp:
            pickle.dump(self.params,fp)
    
    def get(self):
        try : 
            with open(self.__file,'rb') as fp:
                return pickle.load(fp)
        except:
            traceback.print_exc()
            return [EXAMPLE_PARAM]
        

class MessageManager(threading.Thread):
    def __init__(self):
        super(MessageManager,self).__init__()
        self.ps = ParamsStorage()
        self.lock = threading.Lock()
        self.senders = {'QQ':QQSender
                        #'Mail':MailSender
                        }

    @property
    def params(self):
        return  self.ps.params
    
    def save_params(self,index,data):
        if  index+1 > len(self.params) :
            self.params.append(data)
        else:
            self.params[index] = data
        self.ps.save()

    @staticmethod
    def curl_url(url=""):
        r = urllib2.urlopen(url,timeout=5)
        return r.read()
    
    def run(self):
        self.setDaemon(True)
        pass
    
    def send_msg(self,msg):
        for n,s in self.senders.items():
            for p in self.params:
                if p.get('auto_on',''):
                    sender = s(p)
                    sender.send_msg(msg)
    
Ms = MessageManager()
#MsSnender.start()

class MessageHandler(tornado.web.RequestHandler):
    
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
        self.render('index.html',params=params)
    
    
    def curl_url(self):
        url = self.get_argument('url','')
        if url:
            response = Ms.curl_url(url)
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
        
    @tornado.web.asynchronous
    def test_msg(self):
        self.write('测试！')
        self.finish()
        
application = tornado.web.Application( handlers = [(r'/',MessageHandler),
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

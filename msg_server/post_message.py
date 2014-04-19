#!/usr/bin/env python
#coding:utf-8
#消息发送相关

import os,sys,datetime,time
import traceback
import urllib,urllib2
import hashlib
import urllib
import threading
import Queue
SIGN_KEY = 'oaksodqweack123'

def md5(_str):
    return hashlib.new('md5', _str.decode('utf-8')).hexdigest()
def get_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

MSG_ADDRESS = 'http://server.fytxonline.com:11111/msg/post/'

def post_msg(to='qq',msg='',html='',auto_time=True):
        _d = {}
        _d['to'] = to
        _d['msg'] = msg.decode('utf-8').encode('utf-8')
        _d['html'] = html.decode('utf-8').encode('utf-8')
        if auto_time:
            _d['msg'] = '[%s]\n%s' % (get_now(),_d['msg'])
        _d['timestmap'] = int(time.time())
        sign_str = md5('%s%s%s' % (_d['msg'],_d['timestmap'],SIGN_KEY))
        _d['sign'] = sign_str
        try:
            _r = urllib2.urlopen(MSG_ADDRESS,urllib.urlencode(_d),timeout=10).read()
            
        except Exception,e:
            traceback.print_exc()
            _r = str(e)
        return _r 

if __name__ == '__main__':
    for i in xrange(1):
        print post_msg('qq,server','test%s' % i,'html132adasd')
    
    
    
        
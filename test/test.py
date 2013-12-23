#coding:utf-8

import os,sys,time,datetime
import MySQLdb
import functools

def runtime(f):
    @functools.wraps(f)
    def func(*args,**kwargv):
        st = time.time()
        f(*args,**kwargv)
        print ' run %s use time:%.2f' % (f.__name__,time.time() - st)
    return func

def connetmysql():
    import MySQLdb
    con = MySQLdb.connect(host='127.0.0.1',passwd='123456',db='aa')
    cur = con.cursor()
    cur.execute('select * from bb;')
    return cur.fetchall()

def baidu():
    import httplib
    print 'connect baidu'
    h=httplib.HTTPConnection('www.baidu.com:81')
    h.request('GET','/','')
    r=h.getresponse()
    r.read()
@runtime
def testcpm():
    d1 = dict(zip(range(130),[ str(i)*10 for i in range(100)]))
    d2 = dict(zip(range(100),[ str(i)*130 for i in range(100)]))
    for i in xrange(50000):
        cmp(d1,d2)
        _d = d2.copy()
    print cmp(d1,d2)

class a(object):
    val=None
    def __init__(self):
        print self.val
        if not self.__class__.val:
            self.__class__.val = 123
        self.val = 1111111111
if __name__=='__main__':
    aa=a()
    print aa.val
    cc=a()
    print cc.val
    print a.val
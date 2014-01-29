import gevent
from gevent.pool import Group
import time
import httplib
def baidu():
    print 'connect baidu'
    h=httplib.HTTPConnection('www.baidu.com:81')
    h.request('GET','/','')
    r=h.getresponse()
    r.read()

def talk(msg):
    baidu()
    print(msg)

g1 = gevent.spawn(talk, 'bar')
g2 = gevent.spawn(talk, 'foo')
g3 = gevent.spawn(talk, 'fizz')

group = Group()
group.add(g1)
group.add(g2)
group.join()

group.add(g3)
group.join()
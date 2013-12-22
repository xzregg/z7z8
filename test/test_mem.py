from mul_ping import ThreadPool,runtime
import multiprocessing


import sys
import memcache
import time

@runtime
def test_mem(mc=memcache.Client(['127.0.0.1:11211']),x=5000):
    mc=memcache.Client(['127.0.0.1:11211'])
    for i in xrange(x):
        mc.set('a','b'*200)
        mc.get('a')
    del mc
@runtime
def mul_test_mem():
    poll = multiprocessing.Pool(30)

    for i in xrange(2):
        poll.apply_async(test_mem,())
    poll.close()
    poll.join()
@runtime
def mult_test_mem():
    T = ThreadPool(30)
    for i in xrange(3):
        T.append(test_mem,())
    T.close()
class oo:pass

class b(dict):
    at = ''
    def __init__(self):

        self.at = b.at
        if not b.at:
            b.at = oo()
    @classmethod
    def a(self):
        print 'a'


if __name__ =='__main__':

    c=b()
    d=b()
    print c.at
    print d.at
    c.at = '5'

    g=b()
    print g.at
    bb=b()
    print bb.at
    #print sys.getrefcount(b)
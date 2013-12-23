from mul_ping import ThreadPool,runtime
import multiprocessing


import sys
import memcache
import time


def test_mem(x=2000,mc=memcache.Client(['127.0.0.1:11211'])):
    #mc=memcache.Client(['127.0.0.1:11211'])
    for i in xrange(x):
        mc.set('a','b'*200)
        mc.get('a')
    #del mc

@runtime
def mul_test_mem(b,x):
    poll = multiprocessing.Pool(b)

    for i in xrange(b):
        poll.apply_async(test_mem,(x,))
    poll.close()
    poll.join()

@runtime
def mult_test_mem(b,x):
    T = ThreadPool(b)
    for i in xrange(b):
        T.append(test_mem,(x,))
    T.close()


if __name__ =='__main__':
    mult_test_mem(5,10000)
    #mul_test_mem(10,5000)
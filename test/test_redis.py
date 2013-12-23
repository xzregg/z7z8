from mul_ping import ThreadPool,runtime
import multiprocessing


import sys
import redis
import time

rc=redis.Redis(host='127.0.0.1',port=6379,db=0)
def test_redis(x=2000):
    #rc=redis.Redis(host='127.0.0.1',port=6379,db=0)
    for i in xrange(x):
        rc.set('a','b'*200)
        rc.get('a')
    #del rc

@runtime
def mul_test_redis(b,x):
    poll = multiprocessing.Pool(b)
    for i in xrange(b):
        poll.apply_async(test_redis,(x,))
    poll.close()
    poll.join()

@runtime
def mult_test_redis(b,x):
    T = ThreadPool(b)
    for i in xrange(b):
        T.append(test_redis,(x,))
    T.close()


if __name__ =='__main__':
    mult_test_redis(5,10000)
    mul_test_redis(5,10000)
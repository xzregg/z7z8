# -*- coding:UTF-8 -*-
#线程池 by xzr

import threading
import time
import Queue

class ThreadWork(threading.Thread):
        def __init__(self,manager):
            super(ThreadWork,self).__init__()
            self.manager = manager
            self.setDaemon(True)
        def run(self,get_ret=True):
            while 1:
                try:
                    func_grgs = self.manager.jobQ.get_nowait()
                    if func_grgs:
                        res = apply(*func_grgs)
                        if get_ret:
                            self.manager.resultQ.put(res)
                    else:
                        break
                except Queue.Empty:
                    time.sleep(0.01)

class ThreadPool(object):
        def __init__(self,pool_size=0):
            self.Maxsize = pool_size or 100
            self.jobnums = 0
            self.jobQ = Queue.Queue(0)
            self.resultQ = Queue.Queue(0)
            self.threads = []

        def append(self,func,args=()):
            self.jobQ.put((func,args))
            self.jobnums += 1
            if len(self.threads) < self.Maxsize:
                t = ThreadWork(self)
                t.start()
                self.threads.append(t)

        def get_result(self):
                while 1:
                    try:
                        yield self.resultQ.get_nowait()
                    except Queue.Empty:
                        break

        def get_all_result(self):
            return [ r for r in self.get_result() ]

        def close(self):
            for _ in xrange(len(self.threads)):
                self.jobQ.put(None)
            for t in self.threads:
                t.join()


def test(x):
    time.sleep(1)
    #print x
    return x
import os,sys

def ping(ip):
    result = {}
    result['time'] = time.time()
    p = os.popen('ping -q -w 2 -i 0.2 %s'%ip)
    _packets,_rtt = p.read().split('\n')[-3:-1]
    assert  _packets,'ping error!'
    result['packetloss'] = _packets.split(',')[2].split()[0].rstrip('%')
    result['islive'] = True if int(result['packetloss']) <= 20 else False
    if  _rtt:
        _k,_v = _rtt.split()[1::2]
        for k,v in zip(_k.split('/'),_v.split('/')):
            result[k] = v
    return result


if __name__ == '__main__':
    iplist = './iplist'
    T = ThreadPool(3)
    for line in open(iplist,'rb'):
        T.append(ping,(line,))
    T.close()
    for r in T.get_all_result():
        print r

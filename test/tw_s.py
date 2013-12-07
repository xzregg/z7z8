# coding:utf-8
import sys,os,time
import twisted
import traceback
try:
    from twisted.internet import epollreactor
    epollreactor.install()
except Exception,e:
    print e

from twisted.internet import reactor

def hello():
    time.sleep(5)
    print '1'
    print '2'
    aise Exception('asd')
    reactor.stop()

def stack():
    print 'The python stack:'
    traceback.print_stack()

if __name__ == '__main__':

    reactor.callWhenRunning(hello)#异步
    print 'start'
    reactor.run()#阻塞
    print 'end'
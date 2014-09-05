# -*- coding:UTF-8 -*-

try:
    from twisted.internet import epollreactor
    epollreactor.install()
except:
    print 'the system not support epoll!'
    
import twisted
from twisted.internet import protocol,reactor

class PubPortocol(protocol.Protocol):
    '''协议对象
    '''
    def __init__(self,factory):
        self.factory = factory
    
    def connectionMade(self):
        '''连接开始
        '''
        self.factory.clients.add(self)
        
    def connectionLost(self,reason):
        self.factory.clients.remove(self)
        
    def dataReceived(self,data):
        '''数据到达
        '''
        self.transport.write(data)
        
class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

if __name__ == '__main__':
    reactor.listenTCP(1234,PubFactory())
    reactor.run()
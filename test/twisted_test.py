# coding=utf-8
from twisted.python import threadable
try:
    from twisted.internet import epollreactor
    epollreactor.install()
    
    threadable.init(1) 
except:
    pass

from twisted.internet import reactor,protocol
from twisted.internet import threads,defer 

from twisted.protocols import basic
from twisted.application import service
import struct,socket

import traceback,StringIO,threading,time,json

g_mutex = threading.Lock()
db_locker = threading.Lock()
sender_locker = threading.Lock()

_head_len = 2 #定义包头的长度
_player_len = 4 #定义角色ID的长度
if _head_len == 2:
    _head_char = 'H'
else:
    _head_char = 'I'
if _player_len == 8:
    _player_char = 'L'
else:
    _player_char = 'I'
            
class LoginService(basic.LineReceiver):
    def __init__(self,factory):
        self.server_id = 0
        self.factory = factory
        self._data = ''

    def dataReceived(self, data):

        self._data += data
        while len(self._data) > 3:
            try:
                
              print 'dataReceived'

                    
            except:
                print 'except'
                return
                
        if len(self._data)>0:
            print_file('login_service data has more:%d,%d'%(self.server_id,len(self._data)))
    

    
    
    def getId(self):
        return str(self.transport.getPeer())
    
    def connectionMade(self):
        print "New Client Login:", self.getId()
        self.factory.clients[self.getId()] = self

    def connectionLost(self, reason):
        print "Client Lost:", self.server_id,self.getId()
        try:
            self.factory.servers.pop(self.server_id)
            self.factory.clients.pop(self.getId())
        except:
            print_file(("remove error:", self.server_id,self.getId()))

class LoginServiceFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return LoginService(self)
    
    def __init__(self):
        self.clients = {}
        self.servers = {}
        self.login_list = {}
        self.deferRun()
        
    def checkUser(self,thread_id=0):

        pass

    

    def deferRun(self):
        deferlist=[]  
        #创建deferlist中的deferred  
        for i in range(10):  
            print('add to defer%d'%i)
            d = threads.deferToThread(self.checkUser,i)  
            deferlist.append(d)  

        #创建deferredlist  
        dl = defer.DeferredList(deferlist)  
        #给deferredlist添加回调函数  
        dl.addBoth(self.checkUserCallback) 

    def checkUserCallback(self):
        pass

def print_file(msg):
    print(msg)


def main():   
    print_file('login_service run..')  
    reactor.listenTCP(LOGIN_SERVICE_PORT, LoginServiceFactory())
    
    reactor.run()
    
if __name__=='__main__':  
    main()  
    
elif __name__=='__builtin__':  
    reactor.callLater(1,main)  
    application=service.Application('login_service') 


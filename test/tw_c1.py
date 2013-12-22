# coding:utf-8

from twisted.internet import reactor, protocol
from twisted.protocols import basic
import time
class PubProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print 'new'
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        print 'lost:%s' % self.transport.getHost()
        self.factory.clients.remove(self)

    def dataReceived(self,line):
        time.sleep(5)
        for c in self.factory.clients:
            c.sendLine("<{}> {}".format(self.transport.getHost(), line))

    #def lineReceived(self, line):
     #   print len(line)
     #   for c in self.factory.clients:
      #      c.sendLine("<{}> {}".format(self.transport.getHost(), line))

class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return PubProtocol(self)

reactor.listenTCP(8001, PubFactory())
reactor.run()
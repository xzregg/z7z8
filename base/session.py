#coding:utf-8
#定义session 类

import sys,os,time
import memcache
import redis
import cPickle



class SessionEngine(object):
    #session_data = {}
    def save_session(self):pass

class RedisSessionEngine(SessionEngine):
    def __init__(self,sid,address=('127.0.0.1',6379)):
        self.sid = sid
        print sid
        self.rc = redis.Redis(*address,db=0)
        _s = self.rc.get(sid)
        self.session_data = cPickle.loads(_s) if _s else {}

    def save_session(self):
        self.rc.set(self.sid,cPickle.dumps(self.session_data))

class MemcacheSessionEngine(SessionEngine):
    __mc = None
    def __init__(self,sid,address=['127.0.0.1:11211']):
        self.sid = sid
        if not MemcacheSessionEngine.__mc:
            MemcacheSessionEngine.__mc = memcache.Client(address)
        self.mc = MemcacheSessionEngine.__mc
        #print self.mc.get_stats()
        self.session_data = self.mc.get(sid) or {}
    def save_session(self):
        self.mc.set(self.sid,self.session_data)

class SessionEngineFactory(object):
    def __init__(self,sid,engine_type='redis'):
            if engine_type == 'memcache':
                self.se = MemcacheSessionEngine(sid)
            elif engine_type == 'redis':
                self.se = RedisSessionEngine(sid)

            #assert self.se,'Get Session Error'
    def get_session_engine(self):
        return self.se


class Session(dict):
    def __init__(self,sid):
        super(Session,self).__init__()
        self.se = SessionEngineFactory(sid).get_session_engine()
        self.update(self.se.session_data)
    def __getitem__(self, key):
        if not self.has_key(key):
            return None
        return super(Session,self).__getitem__(key)
    def save(self):
        if cmp(self,self.se.session_data):
            print 'is save'
            self.se.session_data = self.copy()
            self.se.save_session()

if __name__ == '__main__':
    d1 = dict(zip(range(130),[ str(i)*10 for i in range(100)]))
    d2 = dict(zip(range(150),[ str(i)*1440 for i in range(150)]))

    s = Session('asd')
    print type(s['bbb'])
    print s
    #s.clear()
    s.save()



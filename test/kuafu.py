# -*- coding:UTF-8 -*-
#线程池 by xzr

import threading
import time
import Queue
import MySQLdb
import os,sys,json

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

class Battle_net(object):
    def __init__(self):
        self.con = MySQLdb.connect(host='centerdb.fytxstatic.com',port=3307,passwd='mongo123123',db='sanguo',charset='utf8')
        self.servers_config = {}

    def get_server_mysql_config(self):
        sql = 'select id,name,log_db_config from servers;'
        cur = self.con.cursor()
        cur.execute(sql)
        for line in cur.fetchall():
            try:
                log_db_config = json.loads(line[2])
                _cf = {'host':log_db_config['host'],
                       'user':log_db_config['user'],
                       'port':int(log_db_config.get('port',3306)),
                       'db':log_db_config['db'],
                       'charset':'utf8',
                       'passwd':log_db_config['password']
                }
                self.servers_config[line[0]] = (line[1],_cf)
            except Exception,e:
                print '%s error!' % str(line[:2])
        return self.servers_config

def get_winner(sid,s_name,mysql_config):
        try:
            sql = 'select log_time,log_user,log_data,log_result,f1 from log_battle_net where log_data>=4 limit 1;'
            #sql = 'show databases;'
            conn =  MySQLdb.connect(**mysql_config)
            print 'connet %s ok' % sid
            cur = conn.cursor()
            cur.execute(sql)
            r = cur.fetchone()
        except:
            r = ()
            print 'connect %s error !' % sid
        finally:
            conn.close()
        return (sid,s_name,r)



if __name__ == '__main__':
    b = Battle_net()
    T = ThreadPool(50)
    i = 0
    for k,v in b.get_server_mysql_config().iteritems():
        i += 1
        T.append(get_winner,(k,v[0],v[1]))
        #print k,v
        #if i>3:break
    T.close()
    for r in T.get_result():
        print r


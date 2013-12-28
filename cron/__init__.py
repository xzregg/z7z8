#!/usr/bin/env python
#coding:utf-8
#定时任务
#http://pythonhosted.org/APScheduler/index.html#coalescing

import os
import sys
import datetime

from libs.apscheduler.scheduler import Scheduler
from libs.apscheduler.events import EVENT_JOB_EXECUTED,EVENT_JOB_ERROR
from libs.apscheduler.jobstores.shelve_store import ShelveJobStore
from libs.apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore
import shelve

from logging import getLogger

log = getLogger(__name__)

class ConJob(Scheduler):
    def __init__(self):
        super(ConJob,self).__init__()
        self._threadpool.max_threads=40
        self.add_listener(self.my_listener,EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        #self.store_alias  = 'mystore'
        self.store_alias  = 'default'
        #self.add_jobstore(ShelveJobStore('/tmp/dbfile'), 'mystore')#必须default不然他会自动创建default
        #self.add_jobstore(SQLAlchemyJobStore('mysql://root:123456@127.0.0.1:3306/apscheduler_jobs'),self.store_alias)
        #self.add_jobstore(SQLAlchemyJobStore('sqlite:///tmp/db'),self.store_alias)

    def add_cron_job(self,name,cron_str,sdate=None,func=None,args=None,**options):
        _c_s = cron_str.split()
        sdate = sdate or datetime.datetime.now()
        assert len(_c_s)==6,'format must match (分 时 日 月 星期 年) !'
        minute,hour,day,mouth,day_of_week,year= _c_s
        super(ConJob,self).add_cron_job(second='5',name=name,func=func,args=args,minute=minute,hour=hour,day=day,jobstore=self.store_alias,
                                        day_of_week=day_of_week,year=year,start_date=sdate,**options)


    def removejob(self,name):
        _j = None
        for j in self.get_jobs():
            if j.name == name:
                log.info('remove job [%s]!' % j.name)
                self.unschedule_job(j)

    def my_listener(self,event):
        if event.exception:
            log.warn('The job crashed :(')
        else:
            log.info( 'The job worked :)')

def test(c):
    for j in c.get_jobs():
        print j.name
        print j
    print '-' * 40

if __name__=='__main__':
    c= ConJob()
    #c.daemonic=False
    c.add_cron_job('asdasd','* * * * * *',func=test,args=(c,))
    c.start()
    print c._threadpool.max_threads
    c.print_jobs()
    print c.get_jobs()
    #c.removejob('asdasd')
    s = raw_input()

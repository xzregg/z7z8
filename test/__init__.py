import os,sys,time,datetime

import functools

def runtime(f):
    @functools.wraps(f)
    def func(*args,**kwargv):
        st = time.time()
        f(*args,**kwargv)
        print ' run %s use time:%.2f' % (f.__name__,time.time() - st)
    return func
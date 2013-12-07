#coding:utf-8

import threading
import time


class mulInstance(object):
    '''多例模式'''
    def __new__(cls):
        print '__new__'
        return cls
    def __init__(self,num):
        print '__init__'
        self.num = num
        self.instances = []
    def __call__(self,obj):
        print '1111111'
        if obj not in self.instances:
            print 'already has'
            self.instances.append(obj)
            return obj
        return self.instances[0]
def singleton(cls,*args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class o(object):
    def __init__(self,a):
        self.v = a


if __name__ == '__main__':
    print type(o)
    b = o('123')
    print b.v
    b.v = 2
    print b.v
    c = o()
    print c.v
    print type(b)
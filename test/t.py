
# -*- coding: utf-8 -*-
import logging
import os
import sys
import functools
import MySQLdb
import inspect
import time
PWD = os.path.dirname(os.path.realpath(__file__))

class  WarpClass(object):
    __sub_class = ['o'] #这些属性是类的话,方法也装饰
    def __new__(self,cls):
        def _warpClass(*args,**kvargs):
            _cls = cls(*args,**kvargs)
            self.__wraps_method(_cls)#包装类时将装饰所有类的方法
            return _cls
        return _warpClass

    @classmethod
    def __wraps_method(self,cls):
        for k,v in inspect.getmembers(cls):#包装类时将装饰所有类的方法
                if k != '__init__' :
                    _method = getattr(cls,k)
                    if inspect.ismethod(v):
                        setattr(cls,k,self.__new_method(_method))
                    elif k in self.__sub_class:
                        print _method
                        self.__wraps_method(v)
    @staticmethod
    def __new_method(method):
        @functools.wraps(method)#保存原来的函数名
        def _method(*args,**kvargs):
            _val_d = locals()
            _s = str(_val_d['kvargs']),str(_val_d['args']),_method.__name__
            print _s
            r = method(*args,**kvargs)
            return r+1
        return _method

class testB(object):
    def __init__(self):
        pass
    def Bmethod(self):
        return 1

#@WarpClass
class testA(object):
    b = 456
    def __init__(self):
        self.o = testB()
    def Amehtod(self,a=1,b=2):
        return a

class B(testA):
    def __init__(self):
        pass

import inspect
def  wrapfunc(obj,name,processor,avoid_doublewrap=True):
    call = getattr(obj,name)
    if avoid_doublewrap and getattr(call,'process',None):
        return
    original_callable = getattr(call,'im_func',all)
    def wrappedfunc(*args,**kwargs):
        return processer(original_callable,*args,**kwargs)
    wrappedfunc.original = call
    wrappedfucn.processor = processor
    if inspect.isclass(obj):
        if hasattr(call,'im_self'):
            if call.im_self:
                wrappedfunc = classmethod(wrappedfunc)
            else:
                wrappedfunc = staticmethod(wrappedfunc)
class A:
    def  __init__(self):
        pass
    @property
    def val(self):
        return 1

if __name__ == "__main__":
    a = A()
    a.val = 23
    print a.val

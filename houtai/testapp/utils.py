#coding:utf-8


import MySQLdb
import inspect,os
import time
import functools
PWD = os.path.dirname(os.path.realpath(__file__))

class  WarpClass(object):
    __sub_class = ['objects']
    def __new__(self,cls):
        self.__wraps_method(cls)
        return cls

    @classmethod
    def __wraps_method(self,cls):
        for k,v in inspect.getmembers(cls):#包装类时将装饰所有类的方法
                if k != '__init__' :
                    if inspect.ismethod(v):
                        #print v
                        setattr(cls,k,self.__new_method(v))
                    elif k in self.__sub_class:
                        print v
                        self.__wraps_method(v)
    @staticmethod
    def __new_method(method):
        @functools.wraps(method)#保存原来的函数名
        def _method(*args,**kvargs):
            _s = str(args),str(kvargs),_method.__name__
            print _s
            r = method(*args,**kvargs)
            return r
        return _method




if __name__ == "__main__":
    t = testA()
    print t.o.Bmethod()
    print t.Amehtod(123,b=2)
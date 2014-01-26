#coding:utf-8
#自动注册url


import inspect,os,sys
from tornado.web import url

Handlers = []
class route(object):
    def __init__(self,re_url,name=None,*args,**kwargs):
        self.re_url = re_url
        self.args = args
        self.kwargs = kwargs
        self.name = name
    def __call__(self,obj):
        Handlers.append(url(self.re_url,obj,
                            name = self.name or '%s.%s' % (obj.__module__,obj.__name__),
                            *self.args,**self.kwargs))
        return obj
        #if inspect.isclass(obj):
        #    print 'is class'
        #if inspect.isfunction(obj):
        #    print 'is function'
        #setattr(obj,'Handlers',Handlers)
        #return obj

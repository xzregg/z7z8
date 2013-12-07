#coding:utf-8

#单例模式
def  single(cls,*args,**kwargs):
    instances = {}
    def _single():
        if not instances.has_key(cls):
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return _single


@single
class A(object):
    def __init__(self):
        self.var = 1

if __name__ == '__main__':
    a = A()
    print a.var
    a.var=123456
    print 123123
    b = A()
    print b.var
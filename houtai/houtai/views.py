#coding:utf-8


from django.http import HttpResponse

def GetPost(request,keys=[],islist=[]):
    '''
    @keys
    @islist
    '''
    #get_list = lambda key:request.POST.getlist(key,request.GET.getlist(key,[]))
    #get = lambda key:request.POST.get(key,request.GET.get(key,''))
    #return [ get_list(k) if i in islist else get(k) for i,k in enumerate(keys)  ]
    R=dict(request.GET)
    R.update(dict(request.POST))

    #return map(lambda v:v[0] if  v.__len__()==1 else v,[ R.get(k,'') for k in keys])
    #return map(lambda i,v:v[0] if not i in islist and v.__len__()==1 else v,range(len(keys)),[ R.get(k,'') for k in keys])#单项不去列表
    l=[ v[0] if  not i in islist and v.__len__()==1 else v  for i,v in enumerate([ R.get(k,'') for k in keys]) ]
    return  l[0] if keys.__len__()==1 else l
import time
def home(request,name='home'):
    st = time.time()
    for i in xrange(10000):
        val1 = GetPost(request,['val1',],[])
    print val1
    return HttpResponse(str(time.time()-st))




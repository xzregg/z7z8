#coding:utf-8

def maopao(L):
    count = len(L)
    for i in xrange(count-1):
        for j in xrange(count-i-1):
            if L[j] > L[j+1]:
                L[j],L[j+1] = L[j+1],L[j]
    return L

def sushu(n):
    '''
    求n以内的素数
                                     忽略1和自身， 看有没能整除的数，没有则是素数
    '''
    return  filter(lambda x: not [ i for i in xrange(2,x) if x % i == 0],[ x for x in xrange(1,n+1) ])


def  BaoJianChui():
    import random
    d = {'b':0,'j':1,'c':2}
    while 1:
        out = random.choice(d.keys())
        print '系统出 %s' % out
        _in = raw_input('你输入：')
        if d[_in] > d[out] or ( d[_in] == 0 and d[out] == 2):
            print '你win'
        elif d[_in] == d[out]:
            print '平'
        else:
            print '你lost'

def fab(n):
    a,b=0,1
    for i in xrange(n):
        b,a = a or 1,a + b
        print a
        #print c



if __name__ == '__main__':
    print maopao([1,3,2,1,4,2,122,2,3])
    print sushu(100)
    #BaoJianChui()
    fab(100)
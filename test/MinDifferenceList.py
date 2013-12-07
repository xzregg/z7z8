

import random
import time
import sys


def MinDifferenceList(L):
    L1,L2,i= [],[],1
    L.sort()
    L_len=len(L)
    while i<=L_len:
        max = L[-i]
        smax = L[-(i+1)] if i<L_len else 0
        i+=2
        if sum(L1)>sum(L2):
            L1+=[smax]
            L2+=[max]
        else:
            L1+=[max]
            L2+=[smax]
    print 'Source List:',L
    print 'Result List:',L1,L2
    print 'Distance   :|%s - %s| = %s'%(sum(L1),sum(L2),abs(sum(L1)-sum(L2)))
    return L1,L2

def mean( sorted_list ):
    if not sorted_list:
        return (([],[]))

    big = sorted_list[-1]
    small = sorted_list[-2]
    big_list, small_list = mean(sorted_list[:-2])
    big_list.append(small)
    small_list.append(big)
    big_list_sum = sum(big_list)
    small_list_sum = sum(small_list)

    if big_list_sum > small_list_sum:
        return ( (big_list, small_list))
    else:
        return (( small_list, big_list))

if __name__=='__main__':
    #a=[random.choice(range(100)) for r in range(10)]
    #b=[random.choice(range(100)) for r in range(11)]
    import sys,os
    print os.path.dirname(__file__)
    sys.exit(1)
    a = [100,99,98,1,2, 3];
    b = [1, 2, 3, 4,5,40];
    c=a+b
    c=[1, 2, 3, 4, 5, 6, 700, 800]

    tests = [   [1,2,3,4,5,6,700,800],
                [10001,10000,100,90,50,1],
                range(1, 11),
                [12312, 12311, 232, 210, 30, 29, 3, 2, 1, 1]
                ]
    for L in tests:
        L.sort()
        MinDifferenceList(L)
        print "Source List:", L
        L1,L2 = mean(L)
        print "Result List:", L1, L2
        print 'Distance   :|%s - %s|= %s'%(sum(L1),sum(L2),abs(sum(L1)-sum(L2)))
        print '-*'*40

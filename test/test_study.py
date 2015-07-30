#coding:utf-8

import os,sys,time,datetime
import MySQLdb
import functools

def runtime(f):
    @functools.wraps(f)
    def func(*args,**kwargv):
        st = time.time()
        f(*args,**kwargv)
        print ' run %s use time:%.2f' % (f.__name__,time.time() - st)
    return func

#使用 for 循环、while 循环和递归写出 3 个函数来计算给定数列的总和。
def sum_list(number_list):
    sum_num = 0
    for i in number_list:
        sum_num += int(i)
    print 'for %s' % sum_num
    sum_num = 0
    i = 0
    while i<len(number_list) :
        sum_num += number_list[i]
        i += 1
    print 'while %s' % sum_num
    sum_num = 0
    
def recursive_sum_list(number_list):
    if not number_list:
        return 0
    sum_num = number_list.pop()
    
    return sum_num + recursive_sum_list(number_list)

#编写一个交错合并列表元素的函数。例如：给定的两个列表为[a，B，C]和[1，2，3]，函数返回[a，1，B，2，C，3]。
def merge_cross_list(lista,list_b):
    result_list = []
    for a,b in zip(lista,list_b):
        result_list.append(a)
        result_list.append(b)
    return result_list
    
#编写一个计算前 100 位斐波那契数的函数。根据定义，斐波那契序列的前两位数字是 0 和1，随后的每个数字是前两个数字的和。例如，前 10 位斐波那契数为：0，1，1，2，3，5，8，13，21，34。    
def fab(tol_num):
    fib_list = [0,1]
    while len(fib_list)<tol_num:
        fib_list.append(fib_list[-1] + fib_list[-2])
    return fib_list

def recursive_fib(num):
    pass


#编写一个能将给定非负整数列表中的数字排列成最大数字的函数。例如，给定[50，2，1,9]，最大数字为 95021。
def merge_number_form_list(num_list):
    return ''.join([str(x) for x in sorted(num_list,reverse=True,cmp=lambda x,y:cmp(int(str(x)[0]),y))])

#编写一个在1，2，…，9（顺序不能变）数字之间插入+或-或什么都不插入，使得计算结果总是 100 的程序，并输出所有的可能性。例如：1 + 2 + 34 – 5 + 67 – 8 + 9 = 100。

if __name__=='__main__':
    sum_list([1,2,3,45])
    print recursive_sum_list( [1,2,3,45] )
    print merge_cross_list(['a','b','c'],[1,2,3])
    
    print fab(10)
    print merge_number_form_list([50,2,1,9])
    the_number_list = range(1,10)
    import itertools
    print list(itertools.permutations(the_number_list,2)).__len__()
    
    
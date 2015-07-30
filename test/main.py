# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os

from ipip import IP
from ipip import IPX
from test import runtime

@runtime
def a():
    IP.load(os.path.abspath("17monipdb.dat"))
    for i in xrange(1,2):
        print IP.find("118.%s.8.%s" % (i+1,i))
    print IP.find('14.23.124.162')

if __name__ == '__main__':
    a()
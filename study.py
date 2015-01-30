#condig:utf-8

from __future__ import unicode_literals

from twisted.internet import reactor

from tornado.options import define, options
import os
import django
import twisted.test as ttest

import itertools
from itertools import count
import MySQLdb
import datetime
import urllib,urllib2
import random


def quick_sort(_list):
    pivot = random.choice(_list)
    print _list,pivot




if __name__ == '__main__':
    quick_sort(
               [3,2,1,55,12,31,2,3,4,51,3,2]
    )
    print random.random.
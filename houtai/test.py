# -*- coding:UTF-8 -*-

import sys
import time
import os
f=os.path.dirname

ProjectsDir=f(os.path.realpath(__file__))#项目路径
sys.path.insert(0,os.path.join(ProjectsDir,'houtai'))
os.environ['DJANGO_SETTINGS_MODULE'] ='houtai.settings'
from django.core.management import setup_environ
import houtai.settings
setup_environ(houtai.settings)
from django.db import connections,connection
from testapp.models import doc
from django.db.models import Q

b=doc()

b.name='123'
b.save()
b.name='123'
b.save()
print connection.queries

#coding:utf-8
#项目配置

import sys
import os

SESSION_ENGINE='memcache://127.0.0.1:11211'
#SESSION_ENGINE='redis://127.0.0.1:1111'

__od = os.path.dirname

#开启debug模式自动重启
DEBUG = True

PROJECT_ROOT = __od(os.path.abspath(__file__))

SETTINGS = {
    'debug': DEBUG,
    'template_path':os.path.join(__od(__file__), "templates"),
    'static_path':os.path.join(__od(__file__), "static"),
    'cookie_secret':'23123123',
    "gzip" : True,
}


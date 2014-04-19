#coding:utf-8
#项目配置
import sys
import os


import environment

SIGN_KEY = 'oaksodqweack123'

SETTINGS = {
    'debug': True,
    'template_path':os.path.join(os.path.dirname(__file__), "templates"),
    'static_path':os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret':'23123123',
    "gzip" : True,
}
#coding:utf-8
#项目配置
import sys
import os


import environment

SIGN_KEY = 'oaksodqweack123'

try:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.argv[0]))
    
PROJECT_ROOT = PROJECT_ROOT.replace('\\','/')

SETTINGS = {
    'debug': True,
    'template_path':os.path.join(PROJECT_ROOT, "templates"),
    'static_path':os.path.join(PROJECT_ROOT, "static"),
    'cookie_secret':'23123123',
    "gzip" : True,
}
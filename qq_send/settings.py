#coding:utf-8
#项目配置
import sys
import os

__od = os.path.dirname
SETTINGS = {
    'debug': True,
    'template_path':os.path.join(__od(__file__)),
    'static_path':os.path.join(__od(__file__), "static"),
    'cookie_secret':'23123123',
    "gzip" : True,
}#开启debug模式自动重启
#coding:utf-8


from tornado.web import url,StaticFileHandler
from settings import SETTINGS
import AutoUrl

import views
#print AutoUrl.Handlers
URLS = [(r"/static/(.*)", StaticFileHandler, {"path":SETTINGS['static_path']})] + AutoUrl.Handlers
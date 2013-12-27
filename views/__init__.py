#coding:utf-8

from base import BaseHandler

from base.log import LOGER

class test(BaseHandler):
    def get(self):
        L = LOGER('bb')
        L.info('asdasdasd')
        self.url = '----------'
        self.write('123')
        self.write('%f'%self.request.request_time())
        self.render('test.html',locals())
    def on_finish(self):
        print('<br>%f[%s]'%(self.request.request_time(),self._request_summary()))
        super(BaseHandler,self).on_finish()
        

class MainHandler(BaseHandler):
    #@tornado.gen.engine
    #@tornado.gen.coroutine
    #@tornado.web.asynchronous
    def get(self):
        #self.session['asd'] = dict(zip(range(100),[ str(i)*1440 for i in range(100)]))
        self.write('asd')
        #print self.cookies
        #self.set_cookie('asd','bbb')
        print self.session
        self.session['asad'] = {1:2}
        _k = self.get_argument('k','k')
        _v = self.get_argument('v','v')
        self.session[_k] = _v
        self.finish()
       # print testThread.num
        #self.render('test.html',locals())        #a = '--1'

    def callbacka(self,a='asd'):
        time.sleep(10)
        self.write('<html><body><form action="/" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
        self.finish()
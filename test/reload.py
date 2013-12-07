#coding:utf-8
#一个重载模块的线程
#by xzr


import threading
import sys
import os
import time

class CheckModules(threading.Thread):
    def __init__(self):
        super(CheckModules,self).__init__()
        self.setDaemon(True)
        self._d = {}

    def run(self):
        while 1:
            for k,m in sys.modules.iteritems():
                if hasattr(m,'__file__'):
                    _m_file = os.path.abspath(m.__file__)
                    _m_mtime = os.stat(_m_file).st_mtime
                    self._d.setdefault(k,[_m_file,_m_mtime])
                    if self._d[k][1] != _m_mtime:
                        print 'reload'
                        reload(sys.modules[k])
                        self._d[k][1] = _m_mtime
            print len(self._d.keys())
            time.sleep(1)


if __name__ == '__main__':
    import testreload
    c = CheckModules()
    c.start()
    while 1:
        print testreload.test()
        time.sleep(1)
    c.join()
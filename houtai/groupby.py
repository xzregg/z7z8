#coding:utf-8

from itertools import groupby
from operator import itemgetter

class SummaryQuery(object):
    def __init__(self,tableFile,merges=[],keyfunc=lambda x:x[0]):
        self.tableFile = tableFile
        self._d = {}
        self._merges = merges
        self.keyfunc = keyfunc

    def _merge_items(self,sl,tl):
        for i in self._merges:
            if len(sl) > i and  len(tl) > i and sl[i].isdigit() and tl[i].isdigit():
                    sl[i] = int(sl[i]) + int(tl[i])

    def _summary_line(self,line):
            items = line.split()
            if items:
                if not self._merges:
                    self._merges = range(1,len(items))
                k = self.keyfunc(items)
                if self._d.has_key(k):
                    self._merge_items(self._d[k],items)
                else:
                    self._d[k] = items

    def get_result(self):
        f = open(self.tableFile,'rb')
        for line in  f:
            if line:self._summary_line(line)
        f.close()
        for k,v in self._d.iteritems():
            if v:print v[0],v[1:]

if __name__ == '__main__':
    o = SummaryQuery('test.txt')
    o.get_result()


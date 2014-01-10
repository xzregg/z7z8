#coding:utf8

from StringIO import StringIO
import traceback
import StringIO

def get_traceback():
    fp = StringIO.StringIO()
    traceback.print_exc(file=fp)
    message = fp.getvalue()
    del fp
    return message

try:
    raise IOError, "an i/o error occurred"
except:
    print get_traceback()
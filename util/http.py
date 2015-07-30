# -*- coding: utf-8 -*-

import httplib
import traceback
import socket
import urllib,urllib2

def urldecode(query_str):
    d = {}
    a = query_str.split('&')
    for s in a:
        if s.find('='):
            k,v = map(urllib.unquote, s.split('='))
            try:
                d[k].append(v)
            except KeyError:
                d[k] = [v]
    return d



class HttpTimeOut(Exception):pass

def http_post(url, data='', data_type = 'x-www-form-urlencoded',user_agent='', timeout_param=5,timeout=5,headers=[],cookie=''):
    res = None
    urlInfo = httplib.urlsplit(url)
    uri = ( '%s?%s' % (urlInfo.path,urlInfo.query) ) if urlInfo.query else urlInfo.path
    if url.find('https://')>-1:
        conn = httplib.HTTPSConnection(urlInfo.netloc,timeout=timeout or timeout_param)
    else:
        conn = httplib.HTTPConnection(urlInfo.netloc,timeout=timeout or timeout_param)
    try:
        conn.connect()
        
        if data:
            if isinstance(data,unicode):
                data = data.encode('utf-8')
            conn.putrequest("POST", uri)
        else:
            conn.putrequest("GET", uri)
            
        for k,v in headers:
            conn.putheader(k, v)
            
        if cookie :
            if isinstance(cookie,dict):
                cookie = ' '.join(['%s=%s;' % (urllib2.quote(str(k)),urllib2.quote(str(v))) for k,v in cookie.iteritems()])
            conn.putheader("Cookie", cookie)
            
        conn.putheader("Content-Length", len(data))
        conn.putheader("Content-Type", "application/%s" % data_type)
        if user_agent!='':
            conn.putheader("User-Agent",user_agent)
                
        conn.putheader("Connection", "close")
        conn.endheaders()

        if data:
            conn.send(data)

        response = conn.getresponse()
        if response:
            res = response.read()
            response.close()
        
        return res
    
    except socket.timeout:
        raise HttpTimeOut('Connect %s time out' % url)
    except Exception, ex:
        raise ex
    
    conn.close()
    
    
if __name__ == '__main__':
    http_post('http://10.20.201.103',timeout_param=2) 

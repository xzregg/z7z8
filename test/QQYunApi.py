#!/usr/bin/env python
#coding:utf-8


import urllib,urllib2
import base64,hmac,hashlib
import time
import random
import json
import traceback
import sys


class QQYunApi(object):
    """
    腾讯云api接口
    http://doc.yun.qq.com/api/v1/contents/1-overview/1.0-start.html
    example:
    api=QQYunApi(Sid,Skey,'debug')
    print api.querytoken()
    """
    _env = {'wai':'http://api.yun.qq.com',         #外网服务
            'nei':'http://gz-api.tencentyun.com',  #内网服务
            'debug':'http://sandbox.api.yun.qq.com'#调试环境
            }
    
    def __init__(self,Sid,Skey,env):
            self.Sid = Sid
            self.Skey = Skey
            self.address = QQYunApi._env[env]
            self.header = {'x-txc-cloud-secretid':Sid,  #申请的密钥ID
                           'x-txc-cloud-nonce':'',      #随机数，用于防止重放攻击，注意避免重复
                           'x-txc-cloud-timestamp':'',  #发起请求时的Unix时间戳，请校对您服务器的时间是否准确
                           'x-txc-cloud-signature':'',  #请求签名
                         }
            self.params={}
            
    def _makeSignature(self):
        """
        鉴权信息生成 
        """
        assert self.method in ('POST','GET'),'method must POST OR GET'
        self.body = ''
        self.uri = self.url
        if self.params.has_key('self'):self.params.pop('self')
        if self.method == 'POST':
            self.body = json.dumps(self.params)
        elif self.method == 'GET':
            if self.params:
                self.uri = '%s?%s'%(self.url,'&'.join([ '%s=%s'%(k,v) for k,v in self.params.iteritems() if v]))#
        self.header['x-txc-cloud-nonce'] = int(random.random()*10**7)
        self.header['x-txc-cloud-timestamp'] = int(time.time())
        _orignal = ['body=%s'%self.body,
                  'method=%s'%self.method,
                  'uri=%s'%self.uri,
                  'x-txc-cloud-secretid=%s'%self.Sid,
                  'x-txc-cloud-nonce=%s'%self.header['x-txc-cloud-nonce'],
                  'x-txc-cloud-timestamp=%s'%self.header['x-txc-cloud-timestamp'],
                  ]
        s = hmac.new(self.Skey,'&'.join(_orignal) ,hashlib.sha1).digest()
        signature = s.encode('base64').rstrip()
        self.header['x-txc-cloud-signature'] = signature

    def getResults(self):
        """
        获取结果
        """
        self._makeSignature()
        fullurl = self.address+self.uri
        request = urllib2.Request(fullurl,self.body,self.header)
        #for k,v in self.header.iteritems():
        #    request.add_header(k,v)
        request.get_method = lambda: self.method 
        try:    
            response = urllib2.urlopen(request)
            r = json.loads(response.read())
        except urllib2.HTTPError,e:
            r = json.loads(e.read())
            #print r['errorCode']
            #print r['errorMessage']
        except:
            traceback.print_exc()
            print fullurl
            print self.body
        finally:
            return r
                

#-------define api-----------------
    def QueryTaskStatus(self,requestId):
        """
        查询任务详细信息
        @requestId 前次请求响应包中返回的标识请求的ID，用于在此接口查询前次接口具体的执行结果
        """
        self.method = "GET"
        self.url = "/v1/requests/%s"%requestId
        self.params = {}
        return self
    
    def QueryCVMS(self,lanips,offset=0,limit=200):
        """
        查询云服务器实例列表
        @lanips 云服务器内网ip串，不同内网ip以逗号分隔，若ip串中存在格式非法的ip，将返回400错误
        @offset 指定第一个返回结果相对实际查询结果集的偏移量，须为大于等于0的整数，默认0
        @limit  指定返回结果的最大数目，须为大于0且不大于200之间的整数，默认200
        """
        self.method = 'GET'
        self.url = '/v1/cvms'
        self.params = locals()
        return self
    
    def QueryCVMDomains(self,lanip):
        """
        查询云服务器绑定的域名列表
        @lanip云服务器内网ip，要求传且只能传一个，不传不会返回信息，传多个只会默认返回第一个的信息
        """
        self.method = 'GET'
        self.url = '/v1/cvms/domains'
        self.params = locals()
        return self
    
    def Querytoken(self):
        """
        查询云服务器登录token
        """
        self.method = "GET"
        self.url = '/v1/cvms/token'
        return self.getResults()
    
    def QueryDomainId(self,domains):
        """
        根据域名查询资源ID
        @domains  按域名查询，支持输入多个域名（域名间使用逗号分隔）；不传默认返回空数组
        """
        self.method = 'GET'
        self.url = '/v1/domains/query_instance_id'
        self.params = locals()
        r = self.getResults()
        r['instanceIds']
        return r['instanceIds']
    
    def QueryDomainInfo(self,domain):
        """
        查询域名详情
        @domain 域名
        """
        instanceId = self.QueryDomainId(domain).values()[0]
        self.method = 'GET'
        self.url = '/v1/domains/%s'%instanceId
        self.params = {}
        return self
    
    def QueryDomainList(self,instanceids='',domains='',type=2,offset=0,limit=200):
        """
        查询域名列表
        @instanceids   'id1,di2'资源id串，通过调用根据域名查询资源ID接口获得。不同资源id以逗号分隔，若id串中存在格式非法的id，将返回400错误（id间使用逗号分隔，建议以instanceids进行批量精确查询）
        @domains       'x.com,x1.com' 按域名查询，支持输入多个域名（域名间使用逗号分隔，不建议以domains进行批量精确查询）
        @type          域名类型（1：常规域名；2：分区分服域名），默认查询常规域名，填1、2之外的数字默认查询常规域名
        @offset        指定第一个返回结果相对实际查询结果集的偏移量，须为大于等于0的整数，默认0
        @limit         指定返回结果的最大数目，须为大于0且不大于200之间的整数，默认200
        """
        self.method = 'GET'
        self.url = '/v1/domains'
        self.params = locals()
        return self
    
    def CVMBindDomain(self,domain,lanIps=[],port=0):
        """绑定云服务器域名
        @domain     绑定的域名
        @lanIps    [ip1,ip2]数组，要绑定的cvm内网ip列表
        @port     端口
        """
        instanceId = self.QueryDomainId(domain).values()[0]
        self.method = 'POST'
        self.url = '/v1/domains/%s/cvm_bind'%instanceId
        self.params = locals()
        return self
    
    def CVMUnbindDomain(self,domain,iportlist=[()]):
        """解绑云服务器域名
        @domain 需要解除绑定的域名
        @iportlist [(ip1,port1),(ip2,port2)]需要解除的地址
        """
        instanceId = self.QueryDomainId(domain).values()[0]
        self.method = "POST"
        self.url = '/v1/domains/%s/cvm_unbind'%instanceId
        self.params = {'devicesList':[{'lanIp':k,'port':v} for k,v in iportlist if k and v]}
        return self

class ShcsYunApi(QQYunApi):
    def __init__(self,*args,**kwargs):
        super(ShcsYunApi,self).__init__(*args,**kwargs)
        
    def WaitResults(self,action,requestId):
            i = 0
            while 1:
                #time.sleep(3)
                _status = self.QueryTaskStatus(requestId).getResults()
                if _status['httpCode'] == 200:
                    print '%s 成功!'%action
                    return True
                elif _status['httpCode'] == 202:
                    time.sleep(5)
                    i += 1
                    print '%s 查询  第%s次'%(action,i)
                    if i >= 60:
                        print '%s 超时！'%action,_status['errorMessage']
                        sys.exit(0) 
                else:
                    print '%s 失败！'%action,_status['errorMessage']
                    return False
        
        
    def UnbindGameDomain(self,domains):
        for _domain in domains:
            d = self.QueryDomainInfo(_domain).getResults()
            for _ip in d['instanceInfo']['devicesList']:
                #if _ip['port']!=80:
                    print _domain,(_ip['lanIp'],_ip['port']),'解除绑定中..'
                    _requestId = self.CVMUnbindDomain(_domain,[(_ip['lanIp'],_ip['port'])]).getResults()['requestId']['id']
                    _action = '%s %s 解除绑定'%(_domain,str((_ip['lanIp'],_ip['port'])))
                    self.WaitResults(_action,_requestId)

    def BinGameDomain(self,domains,ip,port):
        for _domain in domains:
            print _domain,(ip,port),'绑定中...'
            _requestId = self.CVMBindDomain(_domain,[ip],port).getResults()['requestId']['id']
            _action = '%s %s 绑定'%(_domain,str((ip,port)))
            self.WaitResults(_action,_requestId)
            
if __name__ == "__main__":
    Sid = 'AKIDg2lJ88JReDkDYrdkFKjyKR3CcWvD8s49'
    Skey = 'LMwEk8lMSgKIvydok1TTu6AUGabWXj2b'
    api = ShcsYunApi(Sid,Skey,'debug')

    
    
    print api.Querytoken()
    #print api.QueryCVMS('10.190.235.12,10.190.141.7').getResults()
    #print api.QueryDomainId('win.app100655031.twsapp.com')
    #print api.QueryDomainInfo("s42.app100655031.qqopenapp.com").getResults()
    #print api.QueryDomainList('',"win.app100655031.twsapp.com").getResults()
    #print api.CVMBindDomain('win.app100655031.twsapp.com',['10.190.235.12'],8000).getResults()
    #print api.CVMUnbindDomain('win.app100655031.twsapp.com',[('10.190.235.12',8000)]).getResults()
   




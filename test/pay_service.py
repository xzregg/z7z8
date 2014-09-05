# coding=utf-8

try:
    from twisted.internet import epollreactor
    epollreactor.install()
except:
    pass
from twisted.internet import reactor,protocol
from twisted.application import service
from twisted.protocols import basic
import json,socket
import struct,datetime,time
import MySQLdb
import os,traceback,StringIO
from config import PAY_SERVICE_PORT,DB_CONFIG

_head_len = 2 #定义包头的长度
_player_len = 4 #定义角色ID的长度
if _head_len == 2:
    _head_char = 'H'
else:
    _head_char = 'I'
if _player_len == 8:
    _player_char = 'L'
else:
    _player_char = 'I'
    
class PayService(basic.LineReceiver):
    def __init__(self,factory):
        self.server_id = 0
        self.factory = factory
        self._data = ''
        self.last_time = 0
    def dataReceived(self, data):

        self._data += data
        while len(self._data)>3:
            try:
                if self.server_id == 0:
                
                    self.server_id, = struct.unpack('!I',self._data[:4])
                    self.server_id  = socket.htonl(self.server_id)
                    print_file('this server_id is %d'%self.server_id)
                    old_client_key = self.factory.servers.get(self.server_id,'')
                    if old_client_key!='':
                        old_client = self.factory.clients.get(old_client_key,None)
                        if old_client!=None:
                            print_file(('remove a old client',len(self.factory.clients),self.server_id,self.factory.servers,old_client.getId()))
                            self.factory.clients.pop(old_client_key)
                            old_client.transport.loseConnection()
                            
                    self.factory.servers[self.server_id]=self.getId()
                            
                    self.factory.send_list[self.server_id]=0
                    self._data = self._data[4:]
                
                else:
                    recv = self._data[:_head_len]
                    
                    _total_len, = struct.unpack('!%s'%_head_char,recv)
                    if _head_len==2:
                        _total_len = socket.htons(_total_len)
                    else:
                        _total_len = socket.htonl(_total_len)
                    if len(self._data) < _total_len:
                        return
                    
                    self._data = self._data[_head_len:]
                    recv = self._data[:_total_len-_head_len]
                    
                    self._data = self._data[_total_len-_head_len:]
                    
                    if len(recv)!=(_total_len-_head_len):
                        print_file('pay_server error recv length:%d,%d'%(len(recv),(_total_len-_head_len)))
                        
                    _msg_len = _total_len - (6 + _player_len +  _head_len)
            #        print('recv_len',_msg_len)
                    _type,_net_id,_player_id,msg, = struct.unpack('!HI%s%ds'%(_player_char,_msg_len),recv)
                    _type = socket.htons(_type)
                    #_net_id = socket.htonl(_net_id)
                    #_player_id = socket.htonl(_player_id)
                    
                    print_file(('pay_service %d,recv a reply:'%self.server_id,_type,_net_id,_player_id,msg))
                    msg = msg.replace('\0','')
                    if _type==115:
                        result = json.loads(msg)['msg']
                        result_code = result[0]
                        query_id = result[1]
    
                        #更新已发送的
                        record_count = self.factory.send_list.get(self.server_id,1)
#                        print('record_count:',record_count)
                        self.factory.send_list[self.server_id] = record_count-1
                        if result_code == 0:
                            pay_status = 4
                        else:
                            pay_status = -4
                        #更新充值
                        query_sql = 'update pay_action set pay_status=%d,last_time=now() where abs(pay_status)=3 and query_id=\'%s\''%(pay_status,query_id)
                        #print(query_sql)
                        cursor = self.factory.getConn().cursor()
                        cursor.execute(query_sql)
                        #写充值日志
                        log_sql = 'insert into log_pay(log_type,log_user,log_server,log_channel,log_data,log_result,log_time,f1,f2,f3,f4,f5,f6) select 21,pay_user,server_id,channel_id,pay_amount,pay_gold,last_time,query_id,pay_type,pay_status,card_no,pay_ip,remark from pay_action where query_id=\'%s\'' % query_id
#                         print(log_sql)
                        cursor.execute(log_sql)
                    
                    elif self.server_id==0 and _type==999:
                        recv_obj = json.loads(msg)
                        
                        list_server = recv_obj['msg']
                        
                        for item in list_server:
                            client_key = self.factory.servers.get(item,None)
                            client_item = self.factory.clients.get(client_key,None)
                            if client_item!=None:
                                print('admin remove a bad client [%d,%d,%s,%s]'%(len(self.factory.clients),item,self.factory.servers,client_item.getId()))
                                self.factory.servers.pop(item)
                                self.factory.clients.pop(client_key)
                                client_item.transport.loseConnection()
            except:
                fp = StringIO.StringIO()
                traceback.print_exc(file=fp)
                message = fp.getvalue()
                print_file('pay_service has an error1:%d,%s'%(self.server_id,message))
                self.factory.servers.pop(self.server_id)
                self.factory.clients.pop(self.getId())
                self.transport.loseConnection()
                return
            
        if len(self._data)>0:
            print_file('pay_service data has more:%d,%d'%(self.server_id,len(self._data)))
                
    def getId(self):
        return str(self.transport.getPeer())
    
    def connectionMade(self):
        print "New client Join:", self.getId()
        self.factory.clients[self.getId()] = self
        
    def connectionLost(self, reason):
        print "client Lost:", self.server_id,self.getId()
        try:
            self.factory.clients.pop(self.getId())
            self.factory.servers.pop(self.server_id)
        except:
            print_file(("remove error:", self.server_id,self.getId()))
            
class PayServiceFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return PayService(self)
        
    def __init__(self):
        self.clients = {}
        self.servers = {}
        self.pay_list = []
        self.pay_channels = {}
        self.send_list = {} #不给回就不发
        self.server_list = {}
        self.server_id_list = {} #服务器ID集合,包合服后的子服
        self.conn_list = {}
        self.conn_str = DB_CONFIG
        self.getServer()
        self.sendPayList()

    def getConn(self,server_id=0,is_reload=0):
        the_conn = self.conn_list.get(server_id,None)
        the_conn_str = ''
        if the_conn == None:
            if server_id==0:
                the_conn_str = self.conn_str
            else:
                if self.server_list.get(server_id,None)==None:
                    self.getServer()
                the_conn_str = self.server_list[server_id]['db_config']
                
            the_conn = MySQLdb.connect(host=the_conn_str['host'],user=the_conn_str['user'],passwd=the_conn_str['password'],port=the_conn_str.get('port',3306),db=the_conn_str['db'],charset='utf8')    
            self.conn_list[server_id]=the_conn
        else:
            try:
                the_conn.ping()
            except Exception,e:
                print_file('mysql has error:%s'%e)
                if is_reload==0:
                    self.conn_list[server_id] = None
                    return self.getConn(server_id,1)
        return the_conn
    
    def getServer(self):
        if len(self.server_list)==0 or int(time.time())%3600==0:
            query_sql = 'select id,game_addr,log_db_config,json_data from servers'
            cursor = self.getConn().cursor()
            cursor.execute(query_sql)
            list_server = cursor.fetchall()
            for item in list_server:
                try:
                    server_id = int(item[0])
                    master_server_id = 0
                    #print('server item',item)
                    if item[3]!='': #处理合服后的子服
                        json_data = json.loads('{%s}' % item[3])
                        master_server_id = int(json_data.get('master_server_id','0'))
                        
                    if master_server_id > 0:
                        server_ids = self.server_id_list.get(master_server_id,[])
                        server_ids.append(server_id)
                        self.server_id_list[master_server_id] = server_ids
                    else:    
                        server_ids = self.server_id_list.get(server_id,[])
                        server_ids.append(server_id)
                        self.server_id_list[master_server_id] = server_ids
                                    
                    self.server_list[server_id] = {'game_addr':item[1],'db_config':json.loads(item[2])}
                except:
                    print('load server db_confi has error %s'%item[0])
        print(self.server_id_list)
        
    def sendPayList(self):
            
        if self.pay_list.__len__() == 0:
            self.getPayActionList()
        
        if self.pay_channels.__len__() == 0:
            self.getPayChannel(0)

        #print('run....')
        if len(self.pay_list)>0:
            server_id = 0
            try:
                
                #    0=pay_user  1=query_id  2=pay_gold 3=pay_status  4=pay_type_name   5=pay_amount   6=remark   7=id   8=server_id    9=unit 
                #pay_user,query_id,pay_gold,pay_status,b.name pay_type_name,pay_amount,a.remark,a.id,a.server_id,b.unit
                
                #删除pay_channel 后
                # 0=pay_user  1=query_id 2=pay_gold 3=pay_status 4=pay_amount 5=remark 6=id 7=server_id 8=pay_type
                #pay_user,query_id,pay_gold,pay_status,pay_amount,remark,id,server_id
                the_action = self.pay_list[0]
                #print_file(the_action)
                pay_status = int(the_action[3])
                pay_code = 0
                the_action_id = int(the_action[6])
                server_id = int(the_action[7])
                
                server_id = self.getMasterServerId(server_id) #转换为主服ID
                
                if self.send_list.get(server_id,None)==None:
                    self.send_list[server_id]=0
                
                if self.send_list[server_id]>0 or self.servers.get(server_id,'')=='':
                    #add the action to last postion
                    print('has an no reply message %d,%d'%(server_id,self.send_list.get(server_id,0)))
                    self.pay_list.append(the_action)
                    self.pay_list.pop(0)
                    reactor.callLater(2, self.sendPayList)
                    return
                new_status = 3
                check_gold = 0
                remark = ''
                extra_gold = 0
                pay_gold = int(the_action[2])
                if pay_status <0:
                    pay_code = 1
                    new_status = -3
                    if the_action[5]!=None:#remark
                        remark = the_action[5].replace('"','')
                else:
                    extra_gold = int(the_action[9])
                    if float(the_action[4]) > 0:#pay_amount
                        check_gold = int(the_action[2])
#                    pay_gold += extra_gold
                    
                pay_type = the_action[8]
                pay_type = int(pay_type)
                pay_channel = self.pay_channels.get(pay_type, None)
                if pay_channel == None:
                    self.getPayChannel(1)
                    pay_channel = self.pay_channels.get(pay_type, {})

                pay_type_name = pay_channel.get('name','')
                pay_unit = pay_channel.get('unit',u'元')

                msg = u'{"msg":[%d,"%s",%d,%d,"%s",%.2f,"%s","%s",%d,%d]}'%(int(the_action[0]),the_action[1],pay_gold,pay_code,pay_type_name,float(the_action[4]),remark,pay_unit,check_gold,extra_gold)
                
                msg =  msg.encode('utf-8') +'\0'
                print_file('pay_server:%d,send  a msg:%s'%(server_id,msg))
                _msg_len = msg.__len__()
                _total_len = _msg_len + 6 + _player_len + _head_len
                #print_file('_total_len:%d,%d'%(_total_len,socket.ntohl(_total_len)))
                _type = 16
                _net_id = 0
                _player_id = the_action[0]
                
                if _head_len == 2:
                    _total_len = socket.ntohs(_total_len)
                else:
                    _total_len = socket.ntohl(_total_len)
                
                msg = struct.pack('!%sHI%s%ds'%(_head_char,_player_char,_msg_len),_total_len,socket.ntohs(_type),socket.ntohl(_net_id),socket.ntohl(_player_id),msg)
                
                self.clients[self.servers[server_id]].transport.write(msg)

                update_sql = 'update pay_action set pay_status=%d where id=%d'%(new_status,the_action_id)
                conn = self.getConn()
                cursor = conn.cursor()
                cursor.execute(update_sql)   
                conn.commit()
                self.send_list[server_id] += 1   
     
                self.pay_list.pop(0)
            except Exception,e:
                print_file('send pay message has error:%s'%e)
                
            reactor.callLater(1, self.sendPayList)
        else:
            reactor.callLater(6, self.sendPayList)
    
    
    def getMasterServerId(self,server_id):
        for item in self.server_id_list:
            ids = self.server_id_list[item]
            if server_id in ids:
                return item
        
        return item
        
    def getPayChannel(self,is_reload=0):
        if len(self.pay_channels)==0 or is_reload==1:
            query_sql = 'select id,`name`,`unit` from pay_channel'
            cursor = self.getConn().cursor()
            cursor.execute(query_sql)
            list_channel = cursor.fetchall()
            for item in list_channel:
                self.pay_channels[int(item[0])] = {'name':item[1],'unit':item[2]}
    
    def getPayActionList(self):
        #print_file('load date....')
        if self.clients.__len__()>0:
            try:
                server_list = set()
                for server_id in self.servers:
                    if self.send_list.get(server_id,0) > 0:
                        print_file('load data has no reply message:%d,%d'%(server_id,self.send_list.get(server_id,0)))
                    else:
                        for sid in self.server_id_list.get(server_id,[]):
                            server_list.add(str(sid))
                        
                if len(server_list)==0:
                    return        
                sql = 'select pay_user,query_id,pay_gold,pay_status,pay_amount,remark,id,server_id, pay_type,extra from pay_action where pay_status in (2,-2) and server_id in(%s) order by id limit 20'%(','.join(server_list))
                #print(sql)
                
                cursor = self.getConn().cursor()
                cursor.execute(sql)
                list_record = cursor.fetchall()
                for item in list_record:
                    self.pay_list.append(item)
            except Exception,e:
                print('get list error:%s'%e)
            
        #reactor.callLater(10,self.getPayActionList())

def print_file(msg):
    print(msg)
#    try:
#        module_path = os.path.dirname(__file__)
#        file_path = os.path.abspath(os.path.join(module_path, 'pay_service_%s.log'%datetime.datetime.now().strftime('%Y%m%d')))
#        #print(file_path,msg)
#        log_file = open(file_path,'a') 
#        log_file.write('[%s] %s \n'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),str(msg)))
#        log_file.close()
#    except:
#        print('error write file')

def main():  
    print_file('pay_service run..')  
    reactor.listenTCP(PAY_SERVICE_PORT, PayServiceFactory())
    reactor.run()
    
if __name__=='__main__':  
    main()  
    
elif __name__=='__builtin__':  
    reactor.callLater(1,main)  
    application=service.Application('pay_service') 

#coding:utf-8

import urllib,urllib2
import traceback
import json
import logging
import os,sys
import datetime,time

gm_address = 'http://113.106.25.165:56789/player_service'
gm_address = 'http://10.21.210.105:56789/player_service'

_append_item = 'silver'
_append_item = 'gold'

gold_done_file = './gold_done_file'
silver_done_file = './silver_done_file'

gold_log_file = './append_gold_log'
silver_log_file = './append_silver_log'

gold_done_player=[]
silver_done_player=[]
_sleep_time = 0
DATETIMEFORMAT = '%Y-%m-%d %H:%M:%S'
def get_now_str():
    return datetime.datetime.now().strftime(DATETIMEFORMAT)

def get_gm_result(data):
    _st = time.time()
    try:
        r = urllib2.urlopen(gm_address,data,timeout=20)
        r_json = json.loads(r.read())
        _r = (r_json['code'],r_json['content'][0])
    except Exception,e:
        traceback.print_exc()
        _r = (1,{})
    finally:
        _et =  int(time.time() - _st)
        global _sleep_time
        if _et > 0:
            _sleep_time += _et
        else:
            _sleep_time = 0
        return _r
def set_done_player():
    global gold_done_player
    global silver_done_player
    if os.path.exists(gold_done_file) and _append_item=='gold':
        gold_done_player = [ int(line) for line in open(gold_done_file,'rb')]
        print '已对%s个用户增加金币' % len(gold_done_player)
    if os.path.exists(silver_done_file) and _append_item=='silver':
        silver_done_player = [int(line) for line in open(silver_done_file,'rb')]
        print '已对%s个用户增加银币' % len(silver_done_player)

def append_to_file(_file,msg):
    with open(_file,'ab') as f:
        f.write(msg+'\n')

class Player(object):
    player_info_format = 'req_type=1&server_id={sid}&player_id={pid}'
    change_gold_and_silver_format = 'req_type=105&player_id={pid}&server_id={sid}&edited_player_info={{"gl": {gold}, "sl": {silver}}}'
    def __init__(self,sid,pid):
        self.sid = int(sid)
        self.pid = int(pid)
        self.info_data = self.player_info_format.format(sid=self.sid,pid=self.pid)

    def get_gole_and_silver(self):
        c,_d = get_gm_result(self.info_data)
        return (int(_d['gl']), int(_d['sl']))


    def append_gold(self,gold=0):
        gold = int(gold)
        now_gold,_ = self.get_gole_and_silver()
        _data = self.change_gold_and_silver_format.format(pid=self.pid,sid=self.sid,gold=gold,silver=0)
        c,_ = get_gm_result(_data)
        agold,_ = self.get_gole_and_silver()
        if agold>now_gold:
            msg = '成功'
            code = 0
        else:
            msg = '失败'
            code = 1
        append_to_file(gold_done_file,str(self.pid))
        _r =  '[%s] %s %s - 改前金币:%s 增加的金币:%s 修改后的金币:%s %s' % (get_now_str(),self.sid,self.pid,now_gold,gold,agold,msg)
        print _r
        append_to_file(gold_log_file,_r)
        return _r

    def append_silver(self,silver=0):
        silver = int(silver)
        _,now_silver = self.get_gole_and_silver()
        _data = self.change_gold_and_silver_format.format(pid=self.pid,sid=self.sid,gold=0,silver=silver)
        c,_ = get_gm_result(_data)
        _,asilver = self.get_gole_and_silver()
        if asilver>now_silver:
            msg = '成功'
        else:
            msg = '失败'
        _r =  '[%s] %s %s - 改前银币:%s 增加的银币:%s 修改后的银币:%s %s' % (get_now_str(),self.sid,self.pid,now_silver,silver,asilver,msg)
        append_to_file(silver_done_file,str(self.pid))
        print _r
        append_to_file(silver_log_file,_r)
        return _r

class Action(object):
    def __init__(self,input_file):
        self.fp = open(input_file,'rb')

    def do(self):
        for line in self.fp:
            if _sleep_time:
                print 'gm工具太忙了,我也休息下'
                time.sleep(_sleep_time)
            if line:
                try:
                    spl = line.split()
                    assert  len(spl) == 4,'必须4列，符合sid sname pid gold_or_silver'
                    sid,sname,pid,num = spl
                    pid = int(pid)
                    sid = int(sid)
                    p = Player(int(sid),int(pid))
                    assert int(num)>0,'%s确定增加的数目大于0！' % pid
                    if _append_item == 'gold':
                        if pid not in gold_done_player:
                            p.append_gold(int(num))
                            gold_done_player.append(pid)
                        else:
                            print '%s 已经增加过金币了' % pid
                    elif _append_item == 'silver':
                        if pid not in silver_done_player:
                            p.append_silver(int(num))
                            silver_done_player.append(pid)
                        else:
                            print '%s 已经增加过银币了' % pid
                    else:
                        print '什么都不做'
                except Exception,e:
                    traceback.print_exc()
                    print '[%s] %s 增加%s 发生错误!' % (get_now_str(),line.strip(),_append_item,)
def main():
    set_done_player()
    input_file_name = sys.argv[1]
    a = Action(input_file_name)
    a.do()

#文件格式必须是 server_id 服务器名 plarer_id gold_or_silver
if __name__=='__main__':
    main()

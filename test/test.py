#coding:utf-8

import threading
import time
import datetime

def a():
    ios_pay_type = [2,3,4,5,6,7,8,39]
    android_pay_pype = [1,34,35,36,37,38,40]
    sql_format = '''SELECT pa.last_time,s.name,order_id,query_id ,pay_gold,pc.unit,pay_amount,IF(pa.pay_type in ({androids}),'android','ios'),pc.func_name, pc.name AS p
ay_channel_name,c.name AS  channel_name,pa.pay_type FROM pay_action pa LEFT JOIN pay_channel pc ON pa.pay_type = pc.id LEFT JOIN channel c ON pa.channel_id = c.id LEFT
JOIN servers as s on pa.server_id=s.id WHERE pay_amount>0 AND  pay_status=4 AND pa.last_time BETWEEN 'sdate' AND 'edate' and (pa.open_id not in (1,435654,314475
2) or pa.open_id is NULL) AND pa.pay_type IN ({pay_types});'''
    file_format = 'efun_{sdate}'
    print sql_format.format(pay_types=','.join([str(x) for x in ios_pay_type+android_pay_pype]),androids=','.join([ str(x) for x in android_pay_pype]))




def get_dates(sdate,edate):
    edate = edate or datetime.datetime.now()
    print edate
    for i in xrange((edate - sdate).days + 1):
        print '相差天数:%s天' % i
        print sdate
        sdate = sdate + datetime.timedelta(days=1)


if __name__ == '__main__':
    _now  = datetime.datetime.now()
    print _now + datetime.timedelta(days=-1)
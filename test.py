#coding:utf-8


import datetime,time
import calendar
import random
# 生成新手卡号
letter = 'abcdefghjkmnpqrstuvwxyz'
digit = '23456789' 
char = '%s%s'%(letter,digit)

def get_verifCode(card_part):
    sum_value = 0
    for i in range(card_part.__len__()):
        if (i+1) % 2 == 0:
            if i < 9:
                sum_value += int(card_part[i]) * 2 % 10
            else:
                sum_value += ord(card_part[i]) * 2 % 23
        else:
            if i < 9:
                sum_value += int(card_part[i])
            else:
                sum_value += ord(card_part[i]) % 23
    chars = 'abcdefghjkmnpqrstuvwxyz'
    result_char = chars[sum_value % 23]
    return result_char

def add_months(dt,months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day,calendar.monthrange(year,month)[1])
    return dt.replace(year=year, month=month, day=day)


def get_date_list_from_month(sdate,edate):
    date_list = []
    if (edate-sdate).days>28:
        while sdate<edate:
            tmp_edate = add_months(sdate,1)
            if tmp_edate > edate:
                tmp_edate = edate
            date_list.append((sdate,tmp_edate + datetime.timedelta(seconds=-1)))
            sdate = tmp_edate
    else:
        date_list.append((sdate,edate))
        
    return date_list
if __name__ == '__main__':

    
    
    

#coding:utf-8

import json
import time
import datetime
import re
import types


class FormatCheck(object):
    
    tips = ''
    
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    @classmethod
    def isDatetime(cls,v):
        cls.tips = '不是日期格式!'
        try:return datetime.datetime.strptime(v,cls.DATE_FORMAT) 
        except:return False
        
    TIME_FORMAT = '%H:%M:%S'
    @classmethod
    def isTime(cls,v):
        cls.tips = '时间错误'  
        try:return  datetime.datetime.strptime(v,cls.TIME_FORMAT) 
        except:return False
    
    EMAIL_REGEX = r'[^@]+@[^@]+\.[^@]+'
    @classmethod
    def isEmail(cls,v):
        return 'email错误'  if not re.match(cls.EMAIL_REGEX,v) else Flase
    
    #判断是否为中文字符串
    @classmethod
    def isChineseCharString(cls,v):
        cls.tips = '不是中文字符串'
        if isinstace(v,unicode):
            v = v.encode('utf-8')
        for x in v:
            if (x >= u"\u4e00" and x<=u"\u9fa5") or (x >= u'\u0041' and x<=u'\u005a') or (x >= u'\u0061' and x<=u'\u007a'):
               continue
            else:
               return False
        return True
    
     
    #判断是否为中文字符
    @classmethod
    def IsChineseChar(cls,v):
        cls.tips = '不是中文字符'
        if v[0] > chr(127):
           return True
        return False
    
    
    #判断是否为整数
    @classmethod
    def isNumber(cls,v):
        cls.tips = '不是整数'
        if isinstance(v,basestring):
            return str(int(v)) == v
        return type(varObj) is types.IntType
     
    @classmethod
    def isNotEmptyString(cls,v):
        cls.tips = '不能为空'
        return len(v) != 0
    
    #判断是否为浮点数 1.324
    @classmethod
    def isFloat(cls,v):
        cls.tips = '不是整数'
        if isinstance(v,basestring):
            return str(float(v)) == v
        return type(v) is types.FloatType
    
    @classmethod
    def isCurrency(cls,v):
        cls.tips = '不是货币格式 '
        if cls.isFloat(v) and cls.isNumber(v):
            if v >0:
                return cls.isNumber(v)
                return False
        return True
 

    #匹配IP地址
    @classmethod
    def isIpAddr(cls,v):
        cls.tips = '不是ip地址格式'
        rule = '\d+\.\d+\.\d+\.\d+'
        match = re.match( rule , varObj )
        if match:
            return True
        return False
 

    @classmethod
    def isCreditCare(cls,card_number):
        """ checks to make sure that the card passes a luhn mod-10 checksum """  
        cls.tips = '不是行用卡'
        sum = 0  
        num_digits = len(card_number)  
        oddeven = num_digits & 1  
        for count in range(num_digits):  
            digit = int(card_number[count])  
            if not (( count & 1 ) ^ oddeven):  
                digit = digit * 2  
            if digit > 9:  
                digit = digit - 9  
            sum = sum + digit  
        return (sum % 10) == 0  

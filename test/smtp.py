# -*- coding: utf-8 -*-
import os,sys
import smtplib
import email.MIMEMultipart# import MIMEMultipart
import email.MIMEText# import MIMEText
import email.MIMEBase# import MIMEBase
import os.path

import mimetypes
import email.MIMEImage# import MIMEImage

From = "124465200@qq.com"
To = "2025096180@qq.com"
file_name = r"C:\Users\Administrator\Desktop\memcached_en32or64.zip"#附件名

server = smtplib.SMTP("smtp.qq.com")
server.login("124465200@qq.com","") #仅smtp服务器需要验证时

# 构造MIMEMultipart对象做为根容器
main_msg = email.MIMEMultipart.MIMEMultipart()

# 构造MIMEText对象做为邮件显示内容并附加到根容器
text_msg = email.MIMEText.MIMEText("我this is a test text to text mime",_charset="utf-8")
main_msg.attach(text_msg)

# 构造MIMEBase对象做为文件附件内容并附加到根容器
ctype,encoding = mimetypes.guess_type(file_name)
if ctype is None or encoding is not None:
    ctype='application/octet-stream'
maintype,subtype = ctype.split('/',1)
_size = os.path.getsize(file_name)

print _size
#sys.exit(1)
file_msg=email.MIMEImage.MIMEImage(open(file_name,'rb').read(),subtype)
print ctype,encoding

## 设置附件头
basename = os.path.basename(file_name)
file_msg.add_header('Content-Disposition','attachment', filename = basename)#修改邮件头
main_msg.attach(file_msg)

# 设置根容器属性
main_msg['From'] = From
main_msg['To'] = To
main_msg['Subject'] = "attach test "
main_msg['Date'] = email.Utils.formatdate( )

# 得到格式化后的完整文本
fullText = main_msg.as_string( )

# 用smtp发送邮件
try:
    server.sendmail(From, To, fullText)
finally:
    server.quit()



class SendMail(object):
    def __init__(self,myemail,mypassword,address):
        self.from = myemail


    def appendFile(self,filename):
        pass

    def
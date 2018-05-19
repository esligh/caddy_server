'''
Created on 

@author: ThinkPad
'''
import smtplib  
import email.mime.multipart  
import email.mime.text
from email.utils import formatdate;

SMTP_MAIL_SERVER_ADDRESS = 'smtp.163.com'; 
SMTP_SERVER_PORT ='25';
CADDY_MAIL_SERVER_ADDRESS ='caddy_mail_server@163.com';
CADDY_MAIL_SERVER_PWD = 'ndnumrhmyscnixth';  

def smpt_send(user_name,password,fro,to,subject,content):    
    msg=email.mime.multipart.MIMEMultipart();  
    msg['from']=fro;  
    msg['to']=to ;
    msg['subject']=subject;     
    msg['Date'] = formatdate(localtime=True)   
    txt=email.mime.text.MIMEText(content,'html','utf-8');  
    msg.attach(txt);
          
    smtp=smtplib.SMTP();  
    smtp.connect(SMTP_MAIL_SERVER_ADDRESS,SMTP_SERVER_PORT);
    smtp.login(user_name,password);  
    smtp.sendmail(fro,to,str(msg));
    smtp.quit();  
    
if __name__ == '__main__':
    pass
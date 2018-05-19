#coding:utf-8
'''
Created on 
@author: ThinkPad
'''

import logging 
from ser_main import app ;
from flask import request;
from flask import jsonify ;
from ser_model.db import Session; 
from ser_model.base_model import User ;
from ser_util.mail_util import smpt_send
from ser_util.mail_util import CADDY_MAIL_SERVER_ADDRESS,CADDY_MAIL_SERVER_PWD;
import re,uuid ;     
from ser_method.constants import OPER_INVALID, OPER_EXCEPTION, REG_SENDEMAIL, REG_SUCCESS,\
    REG_SAMENAME, REG_SAMEEMAIL
from ser_main.server_config import ACCOUNT_ACTIVE_URL ; 
from sqlalchemy.sql.expression import or_

@app.route('/caddy/api/v1.0/user_register',methods=['POST'])
def do_register():
    
    '''
        this method register an item of user info .
        
        To complete this operation need to do some things as follow:
        <1>parse user's info from json data 
        <2>verify the primary info.
        <3>update database.
        <4>send email and wait active account.   
    '''
    
    reg_state = OPER_INVALID;
    if(request.method == 'POST'):       
        jdata = request.get_json();
        #verify the email 
        email = jdata['email'].strip();
        uname = jdata['name'].strip();            
        url=ACCOUNT_ACTIVE_URL;
        active_code = uuid.uuid1();#base timestamp
       
        session = Session();        
        uid = '';       
        try:
            print uname,email ; 
            
            items = session.query(User).filter(or_(User.name == uname 
                        ,User.email == email)).all();
            print items ;             
            if len(items) > 0:
                if items[0].name == uname:
                    reg_state = REG_SAMENAME ; 
                    print "same name"; 
                if items[0].email == email:
                    reg_state = REG_SAMEEMAIL;
                    print "same email"; 
            else:
                print "same nothing";
                user = User(name=uname,sex=jdata['sex'],dev_id=jdata['dev_id'],\
                        email=email,signature=jdata['signature'],acti_code=active_code);
                user.hash_password(jdata['pwd']);                
                session.add(user);
                session.commit(); 
                uid = user.id;               
                reg_state = REG_SENDEMAIL;
        except Exception,e:
            print e;
            logger = logging.getLogger('watch_dog');
            logger.error(e);
            reg_state=OPER_EXCEPTION;
        finally:
            session.close();
        
        if reg_state == REG_SENDEMAIL:
            url+='?id='+str(uid)+'&acti_code='+str(active_code);
            subject = '欢迎注册跬步'
            content = '''<html><body>
                       <p>亲爱的跬步用户：</p>
                        <p>&nbsp;&nbsp;&nbsp;感谢您加入跬步,请点击下面的链接激活账号完成注册:</p>
                        <p>&nbsp;&nbsp;&nbsp;<a href="'''+str(url)+'''">'''+str(url)+'''</a></p>
                        <p>&nbsp;&nbsp;&nbsp;如果点击上面的链接无效，请直接拷贝到浏览器的地址栏点击访问。</p>
                        <body></html>''';
            smpt_send(CADDY_MAIL_SERVER_ADDRESS,CADDY_MAIL_SERVER_PWD,CADDY_MAIL_SERVER_ADDRESS,
                                      email,subject,content);
                                  
    elif request.method == 'GET':
#       id = request.args['id'];
        #update user's state field 
        reg_state = REG_SUCCESS;
    print reg_state ; 
    return jsonify({'reg_state':reg_state,'uid':uid}),200


@app.route('/active',methods=['GET'])
def do_active():
    uid = request.args.get('id');
    acti_code= request.args.get('acti_code');
    session =Session();
    try:
        entry = session.query(User).get(uid);
    except:
        result = "server exception.";
    if entry.acti_code==acti_code:
        try:        
            session.query(User).filter(User.id == uid).update({User.reg_state: 1});
            session.commit();     
            result = "账号已经激活，欢迎使用跬步。";
        except Exception,e:
            logger = logging.getLogger('watch_dog');
            logger.error(e);
            result = "server exception.";
        finally:
            session.close(); 
    else:
        result ='账号激活失败。'; 
    return result; 

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0;
    
if __name__ == '__main__':
    pass

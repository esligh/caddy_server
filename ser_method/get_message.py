'''
Created on 

@author: ThinkPad
'''
from ser_main.server_config import NGINX_USERPHOTO_URL_BASE
if __name__ == '__main__':
    pass

import logging ; 
from ser_main import app,auth;
from ser_model.db import Session;
from flask import json ,request;
from ser_model.base_model import AlchemyEncoder, Message,User
from ser_method.constants import OPER_SUCCESS, OPER_INVALID, OPER_EXCEPTION,PAGE_SIZE
from ser_util.auth_verify import verify_password ; 

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/get_messages',methods=['POST'])
@auth.login_required
def get_message():
    jdata = request.get_json();
    sender_id = jdata['sender_id'];
    requestor_id = jdata['requestor_id'];
    off =jdata['off'];
    session = Session();
    items = [];
    state = OPER_INVALID ; 
    try:
        sql = " select a.id,a.content, b.name ,b.photo_url,a.create_time ";
        sql += " from message a,user b where a.sender_id = b.id and ((a.sender_id =%s and a.receiver_id=%s)" % (requestor_id,sender_id);
        sql += " or (a.sender_id=%s and a.receiver_id = %s))  " %(sender_id,requestor_id);
        sql += " order by a.create_time limit %s,%s " %(int(off),PAGE_SIZE);
        relist = session.query(Message.id,Message.content,User.name,User.photo_url,Message.create_time).from_statement(sql).all();
        for e in relist:
            d={
               'id':e.id,
               'message':e.content,
               'creator_name':e.name,
               'create_time':e.create_time.strftime('%Y-%m-%d')
            };
            if e.photo_url is not None :
                d['creator_pic'] = NGINX_USERPHOTO_URL_BASE+e.photo_url
            else:
                d['creator_pic'] = "";

            items.append(d);
        state = OPER_SUCCESS;
    except Exception,e :
        print e;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION; 
    finally:
        session.close();
    return json.dumps({'state':state,'result':items},cls=AlchemyEncoder);

@app.route('/caddy/api/v1.0/get_msgusers',methods=['POST'])
@auth.login_required
def get_msgusers():
    jdata = request.get_json();
    uid = jdata['uid'];
    off = jdata['off'];
    session = Session();
    items = [] ;
    state = OPER_INVALID; 
    try:
        sql = " select distinct a.sender_id,b.name,b.sex,b.signature,b.photo_url,"
        sql += " (select count(*) from message c where a.sender_id = c.sender_id "  
        sql += " and c.receiver_id = a.receiver_id and c.is_read=false ) msg_count "  
        sql += " from message a, user b " 
        sql += " where a.sender_id = b.id and a.receiver_id = %s" % uid 
        sql += " limit %s,%s" %(int(off),PAGE_SIZE);
        
        relist = session.query(Message.sender_id,User.name,User.sex,User.signature,
            User.photo_url,'msg_count').\
            from_statement(sql).all();
            
        for e in relist:
            d={
               'sender_id':e.sender_id,
               'name':e.name,
               'sex':e.sex,
               'signature':e.signature,
               'msg_count':e.msg_count
            };            
            if e.photo_url is not None :
                d['photo_url'] = NGINX_USERPHOTO_URL_BASE+e.photo_url
            else:
                d['photo_url'] = "";
            items.append(d);
        state = OPER_SUCCESS;
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        session.close();
    return json.dumps({'state':state,'result':items},cls=AlchemyEncoder);
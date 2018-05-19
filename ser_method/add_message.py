'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_method.constants import OPER_INVALID, OPER_EXCEPTION, OPER_SUCCESS
from ser_main import app,auth ;
from flask import request,json;
from ser_model.db import Session;
from ser_model.base_model import Message
from ser_util.auth_verify import verify_password ; 
from ser_main import clients;

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/send_message',methods=['POST'])
@auth.login_required
def add_message():
    jdata = request.get_json();
    sender_id = jdata['sender_id'];
    receiver_id = jdata['receiver_id'];
    message = jdata['message'];
    session = Session();
    state = OPER_INVALID;
    msg_id = '';
    create_time = '';
    try:
        item = Message(content=message,sender_id = sender_id,receiver_id =receiver_id);
        session.add(item);
        session.commit();
        msg_id = item.id ; 
        create_time =item.create_time.strftime('%Y-%m-%d');
        state = OPER_SUCCESS ; 
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        session.close();
        
    #if receiver is online we need to notify him the coming message  .
    if receiver_id in clients.keys():
        data = {'event_type':'NEW_LETTER'}
        clients[receiver_id].socketio.emit('event',data);   

    return json.dumps({'state':state,'msg_id':msg_id,'create_time':create_time});

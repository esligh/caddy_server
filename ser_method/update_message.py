'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app,auth ;
from ser_model.db import Session;
from ser_model.base_model import Message;
from flask import json ;
from flask import request ; 
from ser_util.auth_verify import verify_password ; 
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 


@app.route('/caddy/api/v1.0/update_message',methods=['POST'])
@auth.login_required
def update_message():
    jdata = request.get_json();
    sender_id = jdata['sender_id'];
    receiver_id = jdata['receiver_id'];
    state = OPER_INVALID;
    try:       
        session = Session();
        session.query(Message).filter(Message.sender_id == sender_id,\
                Message.receiver_id == receiver_id).update({Message.is_read:True}); 
        session.commit();
        state = OPER_SUCCESS;
    except Exception ,e :
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        session.close();
    return json.dumps({'state':state});
if __name__ == '__main__':
    pass
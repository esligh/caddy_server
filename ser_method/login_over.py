'''
Created on 

@author: ThinkPad
'''

import logging ; 
from ser_main import app,auth ;
from ser_model.db import Session;
from ser_model.base_model import User,Message;
from flask import json ;
from flask import request ; 
from ser_util.auth_verify import verify_password ; 
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION
 
@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/login_over',methods=['POST'])
@auth.login_required
def login_over():
    jdata = request.get_json();
    uid = jdata['uid'];
    state = OPER_INVALID ; 
    result = {} ; 
    session = Session();
    try:
        #update state  first
        session.query(User).filter(User.id==uid).update({User.login_state:1});
        session.commit();                       
        #check message box
        relist = session.query(Message).filter(Message.receiver_id == uid, Message.is_read == 0).all();
        if len(relist)>0:
            result['have_message'] = True; 
        else:
            result['have_message'] = False;
        state = OPER_SUCCESS ; 
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog.'+__name__);
        logger.error(e);
        state =OPER_EXCEPTION ; 
    finally:
        session.close();        
    result['state']=state ; 
    print result ;
    return json.dumps(result);
 
if __name__ == '__main__':
    pass
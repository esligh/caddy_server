'''
Created on 

@author: ThinkPad
'''

import logging ; 
from ser_main import app,auth ;
from ser_model.db import Session;
from ser_model.base_model import User;
from flask import json ;
from flask import request ; 
from ser_util.auth_verify import verify_password ; 
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/user_logout',methods=['POST'])
@auth.login_required
def user_logout():
    jdata = request.get_json();
    uid = jdata['uid'];
    state = OPER_INVALID;
    try:       
        session = Session();
        session.query(User).filter(User.id == uid).update({User.login_state:False}); 
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
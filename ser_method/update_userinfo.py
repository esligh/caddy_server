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
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION
from ser_util.auth_verify import verify_password ; 

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/update_userinfo',methods=['POST'])
@auth.login_required
def update_userinfo():
    jdata = request.get_json();    
    fields={};
    if 'name' in jdata :
        fields['name'] = jdata['name'];
    if 'sex' in jdata:
        fields['sex'] = jdata['sex'];
    if 'signature' in jdata:
        fields['signature'] = jdata['signature'];
    if 'profession' in jdata:
        fields['profession'] = jdata['profession'];
    if 'residence' in jdata:
        fields['residence'] = jdata['residence'];
    if 'education' in jdata:
        fields['education'] = jdata['education'];    
    state = OPER_INVALID;
    session = Session();
    try:              
        session.query(User).filter(User.id == jdata['uid']).update(fields); 
        session.commit();
        state = OPER_SUCCESS; 
    except Exception ,e :
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally: 
        session.close();
    return json.dumps({'state':state}) ;

if __name__ == '__main__':
    pass
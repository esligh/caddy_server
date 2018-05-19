'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app,auth ;
from ser_model.db import Session;
from ser_model.base_model import CollectPack;
from flask import json ;
from flask import request ; 
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION
from ser_util.auth_verify import verify_password ; 

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/update_collectpack',methods=['POST'])
@auth.login_required
def update_collectpack():
    jdata = request.get_json();
    print jdata['pack_id'];
    fields={
        'pack_name':jdata['pack_name'],
        'pack_desc':jdata['pack_desc'],
        'is_private':bool(jdata['is_private']),
        'topic_id':jdata['topic_id']
    };
    state = OPER_INVALID;
    session = Session();
    try:              
        session.query(CollectPack).filter(CollectPack.id == jdata['pack_id']).update(fields); 
        session.commit();
        state = OPER_SUCCESS ; 
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
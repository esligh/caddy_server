'''
Created on 

@author: ThinkPad
'''
import logging 
from ser_main import app ,auth;
from flask import request ;
from ser_model.db import Session;
from flask.json import jsonify;
from ser_model.base_model import UserAction,ACTION_VOTE_COLLECTION, Collection,\
    ACTION_OPPOSE_COLLECTION;
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION;
from ser_util.auth_verify import verify_password ; 
@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/del_useraction',methods=['POST'])
@auth.login_required
def del_useraction():
    jdata = request.get_json();
    uid = jdata['uid'];
    obj_id = jdata['obj_id'];
    action_type = jdata['action_type'];
    state = OPER_INVALID;
    session = Session();
    try:
        session.query(UserAction).filter(UserAction.uid == uid , \
            UserAction.action_type == action_type , UserAction.obj_id == obj_id ).delete();
        if action_type == ACTION_VOTE_COLLECTION:
            session.query(Collection).filter(Collection.id == obj_id).update({
                                Collection.vote_count: Collection.vote_count - 1}); 
        if action_type == ACTION_OPPOSE_COLLECTION:
            session.query(Collection).filter(Collection.id == obj_id).update({
                                Collection.bro_count: Collection.bro_count - 1});     
        session.commit();
        state = OPER_SUCCESS;
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION ; 
    finally:
        session.close(); 
    return jsonify({'state':state});

if __name__ == '__main__':
    pass
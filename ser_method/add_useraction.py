'''
Created on 

@author: ThinkPad
'''
'''
Created on 
@author: ThinkPad
'''
import logging ; 
from ser_main import app,auth ;
from flask import request ;
from ser_model.db import Session;
from flask.json import jsonify
from ser_method import constants
from ser_model.base_model import  UserAction, ACTION_VOTE_COLLECTION, Collection,\
    ACTION_OPPOSE_COLLECTION

from ser_util.auth_verify import verify_password ; 
@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/add_useraction',methods=['POST'])
@auth.login_required
def add_useraction():
    jdata = request.get_json();
    state = constants.OPER_INVALID;
    uid = jdata['uid'];
    atype = jdata['action_type']; 
    obj_id = jdata['obj_id'];
    try:
        session = Session();
        item = UserAction(uid = uid,action_type = atype,
                        obj_id = obj_id);
        if atype == ACTION_VOTE_COLLECTION:
            session.query(Collection).filter(Collection.id == obj_id).update({
                                Collection.vote_count: Collection.vote_count + 1}); 
        if atype == ACTION_OPPOSE_COLLECTION:
            session.query(Collection).filter(Collection.id == obj_id).update({
                                Collection.bro_count: Collection.bro_count + 1});
        
        session.add(item);    
        session.commit();
        state = constants.OPER_SUCCESS;
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = constants.OPER_EXCEPTION;
    finally:
        session.close();
    return jsonify({'state':state});

if __name__ == '__main__':
    pass
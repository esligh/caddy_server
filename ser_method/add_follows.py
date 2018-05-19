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
from ser_model.base_model import Userfocus, Topic,CollectPack,User,\
    FOLLOW_TYPE_TOPIC,FOLLOW_TYPE_COLLECTOR,FOLLOW_TYPE_COLLECTPACK

from ser_util.auth_verify import verify_password ; 
@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/add_follows',methods=['POST'])
@auth.login_required
def add_follows():
    jdata = request.get_json();
    state = constants.OPER_INVALID;
    ftype = jdata['type']; 
    obj_id = jdata['obj_id'];
    try:
        session = Session();
        
        item = Userfocus(user_id = jdata['follower_id'],focus_type = ftype,
                        obj_id = obj_id);    
        session.add(item);
        if ftype == FOLLOW_TYPE_TOPIC:
            session.query(Topic).filter(Topic.id == obj_id).update({
                                Topic.focus_count: Topic.focus_count + 1});
            pass ;
        elif ftype == FOLLOW_TYPE_COLLECTPACK:
            session.query(CollectPack).filter(CollectPack.id == obj_id).update({
                                CollectPack.focus_count: CollectPack.focus_count + 1}); 
        elif ftype == FOLLOW_TYPE_COLLECTOR:
            session.query(User).filter(User.id == obj_id) .update({
                                User.focus_count:User.focus_count + 1});    
        session.commit();
        state = constants.OPER_SUCCESS;
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = constants.OPER_EXCEPTION;
    finally:
        session.close();
    result = {
            'state':state,
    };
    return jsonify(result),201;
if __name__ == '__main__':
    pass
'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app ,auth;
from flask import request ;
from ser_model.db import Session;
from flask.json import jsonify
from ser_model.base_model import Userfocus, Topic,CollectPack,\
FOLLOW_TYPE_COLLECTOR,FOLLOW_TYPE_COLLECTPACK,FOLLOW_TYPE_TOPIC
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION
from ser_util.auth_verify import verify_password ; 
@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/del_follows',methods=['POST'])
@auth.login_required
def del_follows():
    jdata = request.get_json();
    follower_id = jdata['follower_id'];
    obj_id = jdata['obj_id'];
    focus_type = jdata['type'];
    state = OPER_INVALID;
    session = Session();
    try:
        session.query(Userfocus).filter(Userfocus.user_id == follower_id and \
            Userfocus.focus_type == focus_type and Userfocus.obj_id == obj_id ).delete();
            
        if focus_type == FOLLOW_TYPE_TOPIC:
            session.query(Topic).filter(Topic.id == obj_id).update({
                                Topic.focus_count: Topic.focus_count - 1}); 
        elif focus_type == FOLLOW_TYPE_COLLECTPACK:
            session.query(CollectPack).filter(CollectPack.id == obj_id).update({
                                CollectPack.focus_count: CollectPack.focus_count -1});  
        elif focus_type == FOLLOW_TYPE_COLLECTOR:
            pass ; 
        state = OPER_SUCCESS;
        session.commit();
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
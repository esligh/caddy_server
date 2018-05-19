'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app,auth ;
from ser_model.db import Session;
from ser_model.base_model import User,Topic,Collection;
from flask import json,request;
from ser_model.base_model import Userfocus
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION

@app.route('/caddy/api/v1.0/user_fllow',methods=['POST'])
@auth.login_required
def user_follow():
    jdata = request.get_json();
    uid = jdata['user_id'];
    obj_id = jdata['obj_id'];
    target = jdata['target'];
    focus_type = '';
    state = OPER_INVALID;
    try:
        session= Session();
        if target == 'COLLECTOR':
            focus_type = '001';
            session.query(User).filter(User.id == obj_id).update({\
                                    User.focus_count: User.focus_count + 1});
        if target == 'COLLECTION':
            focus_type ='002';        
            session.query(Collection).filter(Collection.id == obj_id).update({\
                                    Collection.focus_count: Collection.focus_count + 1});
        if target == 'TOPIC':
            focus_type ='003';
            session.query(Topic).filter(Topic.id == obj_id).update({\
                                    Topic.focus_count: Topic.focus_count + 1});
        item = Userfocus(user_id=uid,focus_type=focus_type,obj_id=obj_id);
        session.add(item); 
        session.commit();
        state = OPER_SUCCESS;
    except Exception,e:
        print e ;      
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        session.close();
    return  json.dumps({'state':state});    
if __name__ == '__main__':
    pass
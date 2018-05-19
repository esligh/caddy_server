'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app,auth ;
from flask import request,json ;
from ser_model.db import Session;
from ser_method import constants
from ser_model.base_model import Report ,UserAction, ACTION_REPORT_COLLECTION

from ser_util.auth_verify import verify_password ; 
@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/add_report',methods=['POST'])
@auth.login_required
def add_report():
    jdata = request.get_json();
    state = constants.OPER_INVALID;
    try:
        session = Session();
        item = Report( obj_id = jdata['cid'],accuser_id= jdata['accuser_id'],defendant_id = jdata['defendant_id'],
                       reason = jdata['reason']);    
        session.add(item);
        action = UserAction(uid = jdata['accuser_id'],action_type = ACTION_REPORT_COLLECTION,
                        obj_id = jdata['cid']);    
        session.add(action);  
           
        session.commit();
        state = constants.OPER_SUCCESS;
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = constants.OPER_EXCEPTION;
    finally:
        session.close();
    return json.dumps({'state':state});

if __name__ == '__main__':
    pass
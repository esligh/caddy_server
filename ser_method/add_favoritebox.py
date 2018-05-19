'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app ,auth;
from flask import request ;
from ser_model.db import Session;
from flask.json import jsonify
from ser_method import constants
from ser_model.base_model import FavoriteBox
from ser_util.auth_verify import verify_password ; 

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/add_favoritebox',methods=['POST'])
@auth.login_required
def add_favoritebox():
    jdata = request.get_json();
    state = constants.OPER_INVALID;
    result = {}; 
    try:
        session = Session();
        item = FavoriteBox(type=jdata['box_type'],box_name = jdata['box_name'],box_desc = jdata['box_desc'],
                           is_private = bool(jdata['is_private']),create_by = jdata['create_by']);                         
        session.add(item);
        session.commit();
        state = constants.OPER_SUCCESS;
        result={
            'box_id':item.id
        }
    except Exception,e:
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = constants.OPER_EXCEPTION;
    finally:
        session.close();
    result['state'] = state ;
    print result ;  
    return jsonify(result),201;
if __name__ == '__main__':
    pass

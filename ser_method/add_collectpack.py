'''
Created on 

@author: ThinkPad
'''
import logging ; 

from ser_main import app,auth ;
from flask import request ;
from ser_model.db import Session;
from ser_model.base_model import CollectPack;
from flask.json import jsonify
from ser_method import constants
from ser_util.auth_verify import verify_password ; 

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/add_collectpack',methods=['POST'])
@auth.login_required
def add_collectpack():
    jdata = request.get_json();
    state = constants.OPER_INVALID;
    result = {};
    try:
        session = Session();
        item = CollectPack(pack_name = jdata['pack_name'],type=jdata['pack_type'],topic_id = jdata['topic_id'],is_private= bool(jdata['private']),
                csn= jdata['csn'],pack_desc = jdata['pack_desc'],create_by = jdata['create_by']);                         
        session.add(item);
        session.commit();
        result['pack_id'] = item.id ; 
        state = constants.OPER_SUCCESS;
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = constants.OPER_EXCEPTION;
    finally:
        session.close();
    result['state'] = state ; 
    return jsonify(result),201;
if __name__ == '__main__':
    pass
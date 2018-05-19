'''
Created on 

@author: ThinkPad
'''

if __name__ == '__main__':
    pass

import logging ; 
from ser_main import app,auth ;
from flask import request ;
from ser_model.db import Session;
from ser_model.base_model import Comment,Collection;
from flask.json import jsonify
from ser_method import constants

from ser_util.auth_verify import verify_password ; 
@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 
 
@app.route('/caddy/api/v1.0/del_comment',methods=['POST'])
@auth.login_required
def del_comment():
    jdata = request.get_json();
    state = constants.OPER_INVALID;
    session = Session();
    try:
        session.query(Comment).filter(Comment.id == jdata['comment_id']).delete();
        session.commit();
        session.query(Collection).filter(Collection.id == jdata['cid']).update({
                                Collection.comment_count: Collection.comment_count - 1});
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
            'state':state
    };
    return jsonify(result),201;

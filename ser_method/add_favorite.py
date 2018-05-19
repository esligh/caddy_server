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
from ser_model.base_model import Favorite, FavoriteBox, UserAction,\
    ACTION_COLLECT_COLLECTION
from ser_util.auth_verify import verify_password ; 

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/add_favorite', methods=['POST'])
@auth.login_required
def add_favorite():
    jdata = request.get_json();
    state = constants.OPER_INVALID;
    bids = jdata['bids'].strip();
    ids  = bids[1:-1].split(',');      
    try:
        session = Session();  
        for bid in ids:
            item = Favorite(collection_id=jdata['cid'], box_id=bid,
                        create_by=jdata['create_by']);                         
            session.add(item);       
        action = UserAction(uid = jdata['create_by'],action_type = ACTION_COLLECT_COLLECTION,
                        obj_id = jdata['cid']);    
        session.add(action);  
        session.query(FavoriteBox).filter(FavoriteBox.id.in_(tuple(ids))).update({
                                FavoriteBox.box_count: FavoriteBox.box_count + 1},synchronize_session=False);
               
        session.commit();            
        state = constants.OPER_SUCCESS;
    except Exception, e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = constants.OPER_EXCEPTION;
    finally:
        session.close();
    return jsonify({'state':state});

if __name__ == '__main__':
    pass

'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app ,auth;
from flask import request ;
from ser_model.db import Session;
from flask.json import jsonify;
from ser_model.base_model import  Favorite; 
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION;
from ser_util.auth_verify import verify_password ; 
from ser_model.base_model import UserAction, ACTION_COLLECT_COLLECTION,\
    FavoriteBox
@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/del_favorite',methods=['POST'])
@auth.login_required
def del_favorite():
    jdata = request.get_json();
    cid = jdata['cid'];
    uid = jdata['uid'];
    box_ids = jdata.get('box_ids');
    ids = tuple(box_ids.split(","));
    state = OPER_INVALID;
    session = Session();
    hasCollected = True; 
    try:
        session.query(Favorite).filter(Favorite.box_id.in_(ids),Favorite.collection_id==cid,\
            Favorite.create_by==uid).delete(synchronize_session=False);    
        session.query(FavoriteBox).filter(FavoriteBox.id.in_(ids),FavoriteBox.create_by == uid).\
            update({FavoriteBox.box_count: FavoriteBox.box_count -1},synchronize_session=False); 
                       
        relist = session.query(Favorite).filter(Favorite.create_by==uid,\
            Favorite.collection_id == cid).first();
        if relist is None:
            session.query(UserAction).filter(UserAction.uid == uid,UserAction.obj_id == cid ,\
                UserAction.action_type == ACTION_COLLECT_COLLECTION).delete();
            hasCollected = False ; 
        session.commit();
        state = OPER_SUCCESS; 
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION ; 
    finally:
        session.close(); 
    return jsonify({'state':state,'has_collected':hasCollected});

if __name__ == '__main__':
    pass
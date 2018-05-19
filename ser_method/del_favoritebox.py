'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app ,auth;
from flask import request ;
from ser_model.db import Session;
from flask.json import jsonify;
from ser_model.base_model import  FavoriteBox; 
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION;
from ser_util.auth_verify import verify_password ; 
from ser_model.base_model import Favorite
@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/clear_favoritebox',methods=['POST'])
@auth.login_required
def clear_favoritebox():
    jdata = request.get_json();
    uid = jdata['uid'];
    box_id = jdata['box_id'];
    state = OPER_INVALID;
    session = Session();
    try:    
        session.query(Favorite).filter(Favorite.box_id==box_id,Favorite.create_by==uid)\
            .delete(synchronize_session=False);
        session.query(FavoriteBox).filter(FavoriteBox.id == box_id,Favorite.create_by==uid)\
            .update({FavoriteBox.box_count:0});
        session.commit();
        state = OPER_SUCCESS; 
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION; 
    finally:
        session.close(); 
    return jsonify({'state':state});

@app.route('/caddy/api/v1.0/del_favoritebox',methods=['POST'])
@auth.login_required
def del_favoritebox():
    jdata = request.get_json();
    uid = jdata['uid'];
    box_id = jdata['box_id'];
    state = OPER_INVALID;
    session = Session();
    try:    
        session.query(Favorite).filter(Favorite.box_id==box_id,Favorite.create_by==uid)\
            .delete(synchronize_session=False);
        session.query(FavoriteBox).filter(FavoriteBox.id==box_id,FavoriteBox.create_by==uid)\
            .delete(synchronize_session=False);         
        session.commit();
        state = OPER_SUCCESS; 
    except Exception,e:
        print e ;
        state = OPER_EXCEPTION; 
    finally:
        session.close(); 
    return jsonify({'state':state});
if __name__ == '__main__':
    pass
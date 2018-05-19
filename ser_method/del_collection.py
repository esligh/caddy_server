'''
Created on 
@author: ThinkPad
'''

import logging; 
from collections import Counter ; 
from ser_main import app ,auth;
from flask import request ;
from ser_model.db import Session;
from ser_model.base_model import Collection;
from flask.json import jsonify;
from ser_model.base_model import Imagelib,CollectPack, Favorite,FavoriteBox,Comment,\
    UserAction
from ser_main.server_config import UPLOAD_IAMGE_ROOT_PATH ; 
from ser_method.constants import OPER_SUCCESS,\
    OPER_EXCEPTION, OPER_INVALID
from ser_util.auth_verify import verify_password ; 
from ser_main.server_config import UPLOAD_IMAGE_COVER_PATH,UPLOAD_IMAGE_THUMBNAIL_PATH

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/del_collection',methods=['POST'])
@auth.login_required
def del_collection():
    # uid = request.get_json().get('user_id');
    jdata = request.get_json();
    cids = jdata['collection_ids'];
    pid = jdata['pack_id'];
    del_state = OPER_INVALID;
    ids = tuple(cids.split(','));
    #use uid and cid verify 
    #pass then delete this collection 
    session = Session();
    try:
        #delete image file first 
        '''
        imgs =  session.query(Imagelib).filter(Imagelib.collection_id.in_(ids)).all();
        remove_files(imgs);
        
        sql = "update favorite_box set box_count=box_count-1 where id in " 
        sql += " (select box_id from collection where id in (:ids)) ";
        session.execute(sql,{'ids':cids.split(',')}) 
        
        #user_action 
        session.query(UserAction).filter(UserAction.action_type < '2000',
                UserAction.obj_id.in_(ids)).delete(synchronize_session=False);
             
        #delete favorite 
        session.query(Favorite).filter(Favorite.collection_id.in_(ids)).delete(synchronize_session=False);        
        #delete comment 
        session.query(Comment).filter(Comment.collection_id.in_(ids)).delete(synchronize_session=False);        
        #delete imagelib record 
        session.query(Imagelib).filter(Imagelib.collection_id.in_(ids)).delete(synchronize_session=False);
        #delete collection instance
        session.query(Collection).filter(Collection.id.in_(ids)).delete(synchronize_session=False);
        '''
        #update state 
        session.query(Collection).filter(Collection.id.in_(ids)).update({
                Collection.state:0},synchronize_session=False);    
        session.query(CollectPack).filter(CollectPack.id == pid).update({
                                CollectPack.collect_count: CollectPack.collect_count -int(jdata['size'])});
                                
        item = session.query(Favorite.box_id).filter(Favorite.collection_id.in_(ids)).all();        
        bids = [] ; 
        for e in item:
            bids.append(e.box_id);
        dd = Counter(bids);
        for key in dd.keys():
            n = dd[key];        
            session.query(FavoriteBox).filter(FavoriteBox.id == key).update({
                        FavoriteBox.box_count:FavoriteBox.box_count-n},synchronize_session=False); 
        session.commit();
        del_state = OPER_SUCCESS;            
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        del_state = OPER_EXCEPTION;
    finally:
        session.close();
    result = {
              'state':del_state,
    };
    return jsonify(result),201

'''
def remove_files(imgs): 
    for item in imgs:
        itype = item.type ; 
        if itype == 'COVER':
            cpath = UPLOAD_IMAGE_COVER_PATH+item.image_url ;
            os.remove(cpath);
            tpath = UPLOAD_IMAGE_THUMBNAIL_PATH+item.image_url ; 
            os.remove(tpath);
        elif itype == 'THUMBNAIL':
            path = UPLOAD_IAMGE_ROOT_PATH+item.image_url;
            os.remove(path);
            tpath = UPLOAD_IMAGE_THUMBNAIL_PATH+item.image_url.split(',')[-1]; 
            os.remove(tpath);
        else:
            path = UPLOAD_IAMGE_ROOT_PATH+item.image_url ;
            os.remove(path);
'''

if __name__ == '__main__':
    pass
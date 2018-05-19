'''
Created on 

@author: ThinkPad
'''
import os ,logging; 
from ser_main import app,auth ;
from flask import request ;
from ser_model.db import Session;
from ser_model.base_model import CollectPack,Collection;
from flask.json import jsonify
from ser_method import constants

from ser_util.auth_verify import verify_password ; 
from ser_model.base_model import Imagelib
from ser_main.server_config import UPLOAD_IMAGE_COVER_PATH,UPLOAD_IMAGE_THUMBNAIL_PATH
from ser_main.server_config import UPLOAD_IAMGE_ROOT_PATH ; 

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 
 
@app.route('/caddy/api/v1.0/del_collectpack',methods=['POST'])
@auth.login_required
def del_collectpack():
    jdata = request.get_json();
    state = constants.OPER_INVALID;
    session = Session();
    print jdata['pid'];
    try:
        '''
        sql = " select * from imagelib where collection_id in " ; 
        sql += " (select id from collection where pack_id = %s ) " % jdata['pid'];       
        imgs = session.query(Imagelib.id,Imagelib.type,Imagelib.image_name,Imagelib.image_url).\
                from_statement(sql).all();
        remove_files(imgs);        
        session.execute('delete from imagelib  where collection_id in(select id from collection  where pack_id = :id )',
                        {'id':jdata['pid']});
        session.query(Collection).filter(Collection.pack_id == jdata["pid"]).delete();        
        session.query(CollectPack).filter(CollectPack.id == jdata["pid"]).delete();    
        '''
        #update state 
        session.query(CollectPack).filter(CollectPack.id == jdata['pid']).update({
                CollectPack.state:0});
        session.commit();     
        state = constants.OPER_SUCCESS;
    except Exception,e:
        print e ; 
        state = constants.OPER_EXCEPTION;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
    finally:
        session.close();
    result = {
            'state':state
    };
    return jsonify(result),201;


def remove_files(imgs): 
    for item in imgs:
        itype = item.type ; 
        if itype == 'COVER':
            cpath = UPLOAD_IMAGE_COVER_PATH+item.image_url ;
            os.remove(cpath);
            tpath = UPLOAD_IMAGE_THUMBNAIL_PATH+item.image_url ; 
            os.remove(tpath);
        elif itype == 'THUMBNAIL':
            path = UPLOAD_IAMGE_ROOT_PATH+item.image_url ;
            os.remove(path);
            tpath = UPLOAD_IMAGE_THUMBNAIL_PATH+item.image_url ; 
            os.remove(tpath);
        else:
            path = UPLOAD_IAMGE_ROOT_PATH+item.image_url ;
            os.remove(path);
if __name__ == '__main__':
    pass
'''
Created on 
@author: ThinkPad
'''

import os ,logging; 
from ser_main import app ,auth;
from flask import request ;
from ser_model.db import Session;
from flask.json import jsonify;
from ser_method.constants import OPER_SUCCESS, \
    OPER_EXCEPTION, OPER_INVALID
from ser_model.base_model import Imagelib
from ser_util.auth_verify import verify_password ; 
from ser_main.server_config import UPLOAD_IMAGE_COVER_PATH,UPLOAD_IMAGE_THUMBNAIL_PATH
from ser_main.server_config import UPLOAD_IAMGE_ROOT_PATH ; 
from ser_tools.tools_util import make_thumbnail ; 

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/del_imgs',methods=['POST'])
@auth.login_required
def del_imgs():
    cid = request.get_json().get('cid');
    ids = request.get_json().get('ids');
    state = OPER_INVALID;   
    ids = tuple(ids.split(","));
    if ids is not None and ids != '':
        session = Session();
        try:
            #delete image file first 
            imgs =  session.query(Imagelib).filter(Imagelib.id.in_(ids)).all();
            hasthumbnail = remove_files(imgs);
                        
            print '#################',ids ; 
            #delete imagelib record 
            session.query(Imagelib).filter(Imagelib.id.in_(ids)).delete(synchronize_session=False); 
            
            if not hasthumbnail :
                relist = session.query(Imagelib).filter(Imagelib.collection_id == cid).all();
                if len(relist)>0:
                    session.query(Imagelib).filter(Imagelib.id == relist[0].id) \
                        .update({Imagelib.type:'THUMBNAIL'});
                    src_path = UPLOAD_IAMGE_ROOT_PATH+relist[0].image_url ; 
                    params = [
                      {'size':(200,150),'dst_path':UPLOAD_IMAGE_THUMBNAIL_PATH},
                    ]
                    make_thumbnail(src_path,params);
            session.commit();
                                   
            state = OPER_SUCCESS;           
        except Exception,e:
            print e ;
            logger = logging.getLogger('watch_dog');
            logger.error(e);
            state = OPER_EXCEPTION;
        finally:
            session.close();
    else:
        state = OPER_SUCCESS; 
                
    return jsonify({'state':state});


def remove_files(imgs): 
    hasthumbnail = True ; 
    for item in imgs:
        itype = item.type ; 
        cid = item.collection_id ; 
        if itype == 'COVER':
            hasthumbnail = False;             
            tpath = UPLOAD_IAMGE_ROOT_PATH+item.image_url ; 
            if os.path.exists(tpath):
                os.remove(tpath);
            cpath = UPLOAD_IMAGE_COVER_PATH+item.image_url ;
            if os.path.exists(cpath):
                os.remove(cpath);
        elif itype == 'THUMBNAIL':
            hasthumbnail = False; 
            path = UPLOAD_IAMGE_ROOT_PATH+item.image_url;
            if os.path.exists(path):
                os.remove(path);
            tpath = UPLOAD_IMAGE_THUMBNAIL_PATH+item.image_url.split('/')[-1];
            if os.path.exists(tpath): 
                os.remove(tpath);
        else:
            path = UPLOAD_IAMGE_ROOT_PATH+item.image_url ;
            if os.path.exists(path):
                os.remove(path);
    
    return hasthumbnail ;
        
'''
def remove_files(filenames): 
    for url in filenames:
        sl = url.split('/');
        path=sl[-2]+'/'+sl[-1];
        path = UPLOAD_IAMGE_ROOT_PATH+path ;
        if os.path.exists(path):
            os.remove(path);
'''
if __name__ == '__main__':
    pass
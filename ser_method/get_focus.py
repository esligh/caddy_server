'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app ;
from ser_main.server_config import NGINX_USERPHOTO_URL_BASE; 
from ser_model.db import Session;
from flask import json,request;
from ser_model.base_model import AlchemyEncoder, Userfocus,User,Topic,CollectPack ; 
from ser_method.constants import OPER_INVALID, OPER_EXCEPTION, OPER_SUCCESS ;
from ser_main.server_config import NGINX_TOPICIMAGE_URL_BASE
 
@app.route('/caddy/api/v1.0/get_focuslist',methods=['POST'])
def get_focuslist():
    jdata = request.get_json();
    uid = jdata['uid'];#user home id 
    off = jdata['off'];
    target = jdata['target'];
    items = [];
    state = OPER_INVALID;
    try:  
        session = Session();     
        if target == 'COLLECTOR':                    
            relist = None;  
            if jdata['follow_who'] == 'ME':
                relist = session.query(User).filter(Userfocus.obj_id==uid,
                        Userfocus.user_id==User.id,Userfocus.focus_type=='001').\
                        offset(int(off)).limit(10).all();
            else:#my follow    
                relist = session.query(User).filter(Userfocus.user_id==uid,\
                                    Userfocus.obj_id==User.id,Userfocus.focus_type=='001').\
                                    offset(int(off)).limit(10).all();
            for e in relist:
                d={
                   'id':e.id,
                   'sex':e.sex,
                   'name':e.name,
                   'signature':e.signature
                };                
                if e.photo_url is not None :
                    d['photo'] = NGINX_USERPHOTO_URL_BASE+e.photo_url
                else:
                    d['photo'] = "";
                items.append(d);
                                    
        if target == 'TOPIC':
            relist = session.query(Topic).filter(Userfocus.user_id==uid,\
                                    Topic.id==Userfocus.obj_id,Userfocus.focus_type=='002').\
                                    offset(int(off)).limit(10).all();
            for e in relist:
                d={
                   'tid':e.id,
                   'topic_name':e.topic_name,
                   'topic_desc':e.topic_desc,
                   'focus_count':e.focus_count,
                   'topic_pic':NGINX_TOPICIMAGE_URL_BASE+e.pic_url
                };
                items.append(d);               
        if target == 'COLLECTPACK':
            relist = session.query(CollectPack).filter(Userfocus.user_id==uid,\
                                    CollectPack.id==Userfocus.obj_id,Userfocus.focus_type=='003').\
                                    offset(int(off)).limit(10).all();
            for e in relist :
                d={
                   'pid':e.id,
                   'pack_name':e.pack_name,
                   'pack_type':e.type,
                   'pack_desc':e.pack_desc,
                   'follow_count':e.focus_count,
                   'collect_count':e.collect_count,
                   'create_by':e.create_by
                };
                items.append(d);                                 
        state = OPER_SUCCESS;        
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally: 
        session.close();
    result = json.dumps({'state':state,'result':items},cls=AlchemyEncoder);
    return result ;
 
if __name__ == '__main__':
    pass
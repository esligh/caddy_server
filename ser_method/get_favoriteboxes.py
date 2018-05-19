'''
Created on 

@author: ThinkPad
'''

import logging ; 
from ser_main import app ;
from ser_model.db import Session;
from flask import json ,request;
from ser_model.base_model import FavoriteBox,AlchemyEncoder, Favorite,\
    Collection,User;
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION,\
    PAGE_SIZE;
from ser_main.server_config import  NGINX_USERPHOTO_URL_BASE,NGINX_IMAGE_SERVER_URI; 


@app.route('/caddy/api/v1.0/get_favoriteboxes',methods=['POST'])
def get_boxes():
    jdata = request.get_json();
    uid = jdata['uid'];
    session = Session();
    state = OPER_INVALID;
    items = [] ; 
    try:
        relist = session.query(FavoriteBox).filter(FavoriteBox.create_by == uid).all();
        state = OPER_SUCCESS ; 
        for e in relist :
            d={
               'box_id':e.id,
               'box_type':e.type,
               'box_type':e.type,
               'box_name':e.box_name,
               'box_desc':e.box_desc,
               'focus_count':e.focus_count,
               'is_private':e.is_private,
               'create_by':e.create_by
            };
            items.append(d);            
    except Exception,e :
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION ;
    finally:
        session.close();    
    result = json.dumps({'state':state,'result':items},cls=AlchemyEncoder);  
    return result ; 

@app.route('/caddy/api/v1.0/get_collectedboxes',methods=['POST'])
def get_collectedbox():
    jdata = request.get_json();
    uid = jdata['uid'];
    cid = jdata['cid'];
    session = Session();
    state = OPER_INVALID;
    box_ids = '';
    try:
        relist = session.query(Favorite).filter(Favorite.create_by == uid,\
            Favorite.collection_id == cid).all();
        state = OPER_SUCCESS ; 
        for e in relist :
            box_ids += str(e.box_id) ;
            box_ids += ',';
    except Exception,e :
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION ;
    finally:
        session.close();    
    result = json.dumps({'state':state,'result':box_ids},cls=AlchemyEncoder);  
    return result ; 



@app.route('/caddy/api/v1.0/get_boxinfo',methods=['POST'])
def get_boxinfo():
    jdata = request.get_json();
    uid = jdata['uid'];    
    box_id = jdata['box_id'];
    state  = OPER_INVALID; 
    session = Session();
    result = {};
    try:
        sql = " select a.id,a.type,a.box_name,a.box_desc,a.focus_count,a.create_by,a.is_private,";
        if uid is None or uid == '' : #not login actually .
            sql += " (select false from dual ) is_focus " ; 
        else:
            sql += " (select b.id from userfocus b where a.id = b.obj_id and b.focus_type ='004' and b.user_id = %s limit 1 ) is_focus" % (uid); 
        sql += " from favorite_box a ,user b where a.create_by = b.id and a.id = %s " % (box_id);
        entry = session.query(FavoriteBox.id,FavoriteBox.box_name,FavoriteBox.box_desc,FavoriteBox.focus_count,
                              FavoriteBox.type,FavoriteBox.create_by,FavoriteBox.is_private,'is_focus').\
                              from_statement(sql).first();
        flag = True;
        if entry.is_focus is None or bool(entry.is_focus) is False:
            flag = False ; 
        print uid,entry.is_focus,flag 
        result = {
            'id' : entry.id,
            'box_type':entry.type,
            'box_name':entry.box_name,
            'box_desc':entry.box_desc,
            'focus_count':entry.focus_count,
            'create_by':entry.create_by,
            'is_focus': flag,
            'is_private':bool(entry.is_private)            
        };
        state = OPER_SUCCESS ; 
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state= OPER_EXCEPTION ; 
    finally:
        session.close();
        
    return json.dumps({'state':state,'result':result},ensure_ascii=False,cls=AlchemyEncoder);


@app.route('/caddy/api/v1.0/get_boxdetail',methods=['POST'])
def get_boxdetail():
    jdata = request.get_json();
    uid = jdata['uid'];
    off = jdata['off'];
    session = Session();
    items = [] ;
    state = OPER_INVALID; 
    try:
        sql = " select a.id,a.type,a.box_name,a.box_desc ,a.focus_count, a.box_count,";
        sql += " (select group_concat(b.title) from collection b ,favorite c where c.collection_id = b.id and c.box_id = a.id limit 3) titles"
        sql += " from favorite_box a where a.create_by = %s " % uid ;
        sql += " order by a.create_time desc limit %s,%s" %(int(off),PAGE_SIZE); 
        relist = session.query(FavoriteBox.id,FavoriteBox.type,FavoriteBox.box_name,FavoriteBox.box_desc,FavoriteBox.box_count
                         ,FavoriteBox.focus_count ,'titles').from_statement(sql).all();
        for e in relist:
            d={
               'box_id':e.id ,
               'box_type':e.type,
               'box_name':e.box_name,
               'box_desc':e.box_desc,
               'box_count':e.box_count,
               'focus_count':e.focus_count,
               'titles':e.titles
            };
            items.append(d);
        print items ; 
        state = OPER_SUCCESS;
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        session.close();
    return json.dumps({'state':state,'result':items}, ensure_ascii=False,cls=AlchemyEncoder); 


@app.route('/caddy/api/v1.0/get_boxlist',methods=['POST'])
def get_boxlist():
    jdata = request.get_json();
    off= jdata['off'];
    items = [] ;
    state = OPER_INVALID ; 
    try:
        session = Session();
        relist = session.query(Collection,User).filter(Favorite.collection_id == Collection.id,\
                    Collection.create_by == User.id , Collection.state ==1 , Favorite.box_id== jdata['box_id']).\
                    order_by(Favorite.create_time).offset(off).limit(PAGE_SIZE).all();
        
        for c in relist :
            d = {
                 'id':c[0].id,
                 'cisn':c[0].cisn,
                 'title':c[0].title,
                 'abstract':c[0].abstract,
                 'create_by':c[0].create_by,
                 'vote_count':c[0].vote_count,
                 'comment_count':c[0].comment_count,
                 'name':c[1].name,
                 'sex':c[1].sex,
                 'signature':c[1].signature
            }; 
            if c[1].photo_url is not None :
                d['photo'] = str(NGINX_USERPHOTO_URL_BASE+c[1].photo_url)
            else:
                d['photo'] = '';
            if c[0].cover is not None :
                d['cover'] = NGINX_IMAGE_SERVER_URI+c[0].cover 
            else :
                d['cover'] = '';   
            items.append(d);
            state =OPER_SUCCESS ; 
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION ; 
    finally:
        session.close();

    result = json.dumps({"state":state,"result":items},ensure_ascii=False,cls=AlchemyEncoder);    
    return result; 
if __name__ == '__main__':
    pass
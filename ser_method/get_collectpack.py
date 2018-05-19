'''
Created on 
@author: ThinkPad
'''
import logging ; 
from ser_main import app;
from ser_main.server_config import NGINX_USERPHOTO_BIG_URL_BASE,NGINX_IMAGE_SERVER_URI; 
from ser_model.db import Session;
from ser_model.base_model import CollectPack,Collection,User,Topic;
from flask import json ,request;
from ser_model.base_model import AlchemyEncoder, FavoriteBox
from ser_method.constants import OPER_SUCCESS,\
    PAGE_SIZE, OPER_INVALID, OPER_EXCEPTION

@app.route('/caddy/api/v1.0/get_collectpack',methods=['POST'])
def get_packinfo():
    jdata = request.get_json();
    uid = jdata['uid'];
    pack_id = jdata['pack_id'];
    state  = OPER_INVALID; 
    session = Session();
    result = {};
    try:
        sql = " select a.id,a.pack_name,a.type,a.pack_desc,a.focus_count,a.create_by,a.topic_id,a.is_private,";
        sql += " u.name,u.sex,u.photo_url,u.signature,"    
        if uid is None: #not login actually .
            sql += " (select false from dual ) is_focus " ; 
        else:     
            sql += " (select b.id from userfocus b where a.id = b.obj_id and b.focus_type ='003' and b.user_id = %s limit 1 ) is_focus" % (uid); 
        sql += " from collect_pack a ,user u where a.create_by = u.id and  a.id = %s " % (pack_id);
        entry = session.query(CollectPack.id,CollectPack.pack_name,CollectPack.type,CollectPack.pack_desc,CollectPack.focus_count,
                              CollectPack.create_by,CollectPack.topic_id,CollectPack.is_private,
                              User.name,User.photo_url,User.sex,User.signature,'is_focus',).\
                              from_statement(sql).first();  
        isFocus = True;
        if entry.is_focus is None or bool(entry.is_focus) is False:
            isFocus = False ; 
        result = {
            'id' : entry.id,
            'pack_name':entry.pack_name,
            'pack_type':entry.type,
            'pack_desc':entry.pack_desc,
            'focus_count':entry.focus_count,
            'create_by':entry.create_by,
            'is_focus': isFocus,
            'topic_id':entry.topic_id,
            'is_private':bool(entry.is_private),
            'name':entry.name,
            'sex':entry.sex,
            'signature':entry.signature            
        };
        
        if entry.topic_id is not None and entry.topic_id != '':
            tids = entry.topic_id.split(','); 
            names = '';
            item = session.query(Topic.topic_name).filter(Topic.id.in_(tuple(tids))).all();
            for e in item :
                names+=e.topic_name ; 
                names+=',';
            result['topic_names'] = names; 
        else :
            result['topic_names'] = '';
    
        if entry.photo_url is not None :
            result['photo'] = NGINX_USERPHOTO_BIG_URL_BASE+entry.photo_url
        else:
            result['photo'] = "";
        print result ;
        state = OPER_SUCCESS ; 
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state= OPER_EXCEPTION ; 
    finally:
        session.close();
        
    return json.dumps({'state':state,'result':result},ensure_ascii=False,cls=AlchemyEncoder);

@app.route('/caddy/api/v1.0/get_packlist',methods=['POST'])
def getpacklist():
    jdata = request.get_json();
    off= jdata['off'];
    items = [] ; 
    try:
        session = Session();
        relist = session.query(Collection,User).filter(Collection.create_by == User.id,
                                                Collection.pack_id == jdata['pack_id'],
                                                Collection.state == '1').\
        order_by(Collection.last_modify).offset(off).limit(PAGE_SIZE).all();
        for c in relist :
            d = {
                 'cid':c[0].id,
                 'cisn':c[0].cisn,
                 'title':c[0].title,
                 'abstract':c[0].abstract,
                 'create_by':c[0].create_by,
                 'vote_count':c[0].vote_count,
                 'name':c[1].name,
                 'sex':c[1].sex,
                 'signature':c[1].signature,
                 'comment_count':c[0].comment_count
            }; 
            if c[1].photo_url is not None :
                d['photo'] = NGINX_USERPHOTO_BIG_URL_BASE+c[1].photo_url
            else:
                d['photo'] = "";
            if c[0].cover is not None :
                d['cover'] = NGINX_IMAGE_SERVER_URI+c[0].cover 
            items.append(d); 
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
    finally:
        session.close();
    result = json.dumps({"state":OPER_SUCCESS,"result":items},ensure_ascii=False,cls=AlchemyEncoder);    
    return result; 

@app.route('/caddy/api/v1.0/get_hotpacks',methods=['POST'])
def gethotpacks():
    jdata = request.get_json();
    off = jdata['off'];
    action = jdata['action'];   
    state = OPER_INVALID;
    items = [] ; 
    try:
        session=Session();
        sql = ' select distinct a.id,a.type,a.box_name,a.box_desc,a.box_count , a.focus_count,b.id as uid ,b.name,b.sex, b.photo_url '; 
        sql +=' from favorite_box a, user b ';
        sql +=' where a.create_by = b.id and a.is_private = false  '
        if int(off) == 0 :
            sql += " order by a.focus_count desc   limit %s,%s " % (0,PAGE_SIZE);
        elif action == 'REQ_NEWDATA':
            sql += " and a.focus_count > %s order by a.focus_count desc  limit 0, 6" % (jdata['threshold']);
        elif action == 'REQ_HISTORY' :
            sql += " order by a.focus_count desc  limit %s, %s " % (int(off),PAGE_SIZE);    
        
        reslist = session.query(FavoriteBox.id,FavoriteBox.type,FavoriteBox.box_name,FavoriteBox.box_desc,FavoriteBox.focus_count,
            FavoriteBox.box_count,'uid',User.name,User.sex,User.photo_url).from_statement(sql).all();
        for e in reslist:
            d={
               'box_id':e.id,
               'box_type':e.type,
               'box_name':e.box_name,
               'box_desc':e.box_desc,
               'box_count':e.box_count,
               'focus_count':e.focus_count, 
               'uid':e.uid,
               'name':e.name,
               'sex' :e.sex,
            };            
            if e.photo_url is not None :
                d['photo'] = NGINX_USERPHOTO_BIG_URL_BASE+e.photo_url
            else:
                d['photo'] = "";
                
            items.append(d);
        state = OPER_SUCCESS;
    except Exception,e:
        print e; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        session.close();
    return json.dumps({'state':state,'result':items},cls=AlchemyEncoder);


@app.route('/caddy/api/v1.0/get_userpacks',methods=['POST'])
def get_userpacks():
    req_uid = request.get_json().get("req_uid");
    uid = request.get_json().get("uid");
    ismyself = False ; 
    if req_uid == uid : #myself 
        ismyself = True ; 
    off = request.get_json().get("off"); 
    state = OPER_INVALID;
    items = [] ;     
    session=Session();
    try:
        if ismyself:
            relist = session.query(CollectPack).filter(CollectPack.create_by == uid)\
                    .offset(int(off)).limit(10).all();
        else:
            relist = session.query(CollectPack).filter(CollectPack.create_by == uid,CollectPack.is_private == False)\
                        .offset(int(off)).limit(10).all();
        for e in relist :
            d={
               'id':e.id,
               'pack_name':e.pack_name,
               'pack_desc':e.pack_desc,
               'pack_type':e.type,
               'focus_count':e.focus_count,
               'collect_count':e.collect_count,
               'topic_ids':e.topic_id,
               'create_by':e.create_by
            };
            items.append(d);
        state = OPER_SUCCESS;
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION ; 
    finally:
        session.close();
    return json.dumps({'state':state,'result':items},cls=AlchemyEncoder);
            
if __name__ == '__main__':
    pass

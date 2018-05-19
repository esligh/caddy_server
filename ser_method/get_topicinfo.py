'''
Created on 

@author: ThinkPad
'''

import logging ; 
from ser_main import app ;
from ser_model.db import Session;
from ser_model.base_model import Topic;
from flask import json,request ;
from ser_model.base_model import AlchemyEncoder;
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION
from ser_main.server_config import NGINX_TOPICIMAGE_URL_BASE

@app.route('/caddy/api/v1.0/get_topicinfo',methods=['POST'])
def get_topic():
    jdata = request.get_json();
    uid = jdata['uid'];
    obj_id = jdata['obj_id'];
    state = OPER_INVALID;
    info={};
    session = Session();
    try:
        sql = " select a.id,a.topic_name,a.topic_desc,a.focus_count ,";
        if uid is None :
            sql += " ( select false from dual ) is_focus "
        else:
            sql += " (select b.id from userfocus b where a.id = b.obj_id and b.focus_type ='002' and b.user_id = %s limit 1 ) is_focus " % (uid);
        sql += " from topic a where a.id = %s " % (obj_id);
        entry = session.query(Topic.id,Topic.topic_name,Topic.topic_desc,Topic.focus_count,'is_focus').from_statement(sql).one();
        flag = True ;
        if entry.is_focus is None or bool(entry.is_focus) is False:
            flag = False; 
        info={
              'topic_id':entry.id,
              'topic_name':entry.topic_name,
              'topic_desc':entry.topic_desc,
              'focus_count':entry.focus_count,
              'is_focus':flag
        };
        state = OPER_SUCCESS;  
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        session.close();
    result = json.dumps({'state':state,'result':info},cls=AlchemyEncoder);
    return result ,200 ;

@app.route('/caddy/api/v1.0/get_topiclist',methods=['POST'])
def get_topiclist():
    jdata = request.get_json();
    off = request.get_json().get("off");
    s = jdata['slice'];
    session = Session();
    items=[];
    state=OPER_INVALID;
    try:
        relist = None ; 
        if off is None:
            relist = session.query(Topic).filter(Topic.topic_name.like('%'+s+'%')).all();
        else:    
            relist = session.query(Topic).filter(Topic.topic_name.like('%'+s+'%')).\
                    offset(int(off)).limit(10).all();
        for e in relist:
            d={
               'tid':e.id,
               'topic_name':e.topic_name,
               'topic_desc':e.topic_desc,
               'topic_pic' :NGINX_TOPICIMAGE_URL_BASE+e.pic_url
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
    return json.dumps({'state':state,'result':items},cls=AlchemyEncoder);

@app.route('/caddy/api/v1.0/get_packtopics',methods=['POST'])
def get_packtopics():
    jdata = request.get_json();
    ids = tuple(jdata['topic_ids'].split(","));
    print ids ; 
    state = OPER_INVALID ; 
    session = Session();
    items = [];
    try:
        relist = session.query(Topic).filter(Topic.id.in_(ids)).all();
        for e in relist :
            d= {
                'id':e.id,
                'topic_name':e.topic_name,
                'topic_desc':e.topic_desc,
                'topic_pic':NGINX_TOPICIMAGE_URL_BASE+e.pic_url
            };
            items.append(d);
        state = OPER_SUCCESS ; 
    except Exception,e :
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION ; 
    finally: 
        session.close();
    return json.dumps({'state':state,'result':items},cls=AlchemyEncoder);
    
if __name__ == '__main__':
    pass;

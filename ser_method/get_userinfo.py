#coding:utf-8
'''
Created on 

@author: ThinkPad
'''

import logging ; 
from ser_main import app ;
from ser_model.db import Session;
from ser_model.base_model import User;
from flask import json ,request;
from ser_model.base_model import AlchemyEncoder
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION
from ser_main.server_config import NGINX_USERPHOTO_MEDIUM_URL_BASE,NGINX_USERPHOTO_BIG_URL_BASE

@app.route('/caddy/api/v1.0/get_userinfo',methods=['POST'])
def get_userinfo():    
    jdata = request.get_json();
    uid = jdata['uid'];
    obj_id = jdata['obj_id'];
    state = OPER_INVALID;
    info={};
    try:
        session = Session();
        sql = " select a.id,a.name,a.sex,a.email,a.photo_url,a.signature,a.login_state,a.reg_state,a.profession,a.residence,a.education,";
        if uid is None or uid == '':
            sql += " (select false from dual ) is_focus "
        else:
            sql += " (select b.id from userfocus b where a.id = b.obj_id and b.focus_type ='001' and b.user_id = %s limit 1 ) is_focus" % (uid);  
        sql += " from user a where a.id = %s " % (obj_id);
        #entry = session.query(User).filter(User.id==jdata['uid']).one();
        entry = session.query(User.id,User.name,User.sex,User.email,User.photo_url,User.signature,User.profession,User.residence,User.education,
            User.login_state,User.reg_state,'is_focus').from_statement(sql).one();
        state = OPER_SUCCESS;
        flag = True;     
        if entry.is_focus is None or bool(entry.is_focus) is False:
            flag = False ; 
        info={
          'id':entry.id,
          'name':entry.name,
          'sex':entry.sex,
          'email':entry.email,          
          'signature':entry.signature,
          'login_state':entry.login_state,
          'reg_state':entry.reg_state,
          'is_focus': flag,
          'profession':entry.profession,
          'residence':entry.residence,
          'education':entry.education    
        };
        
        if entry.photo_url is not None :
            info['photo'] = NGINX_USERPHOTO_BIG_URL_BASE+entry.photo_url
        else:
            info['photo'] = "";
    
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION; 
    #user base info
    result = json.dumps({'state':state,'result':info},cls=AlchemyEncoder);
    session.close();
    return result ,200 ; 

@app.route('/caddy/api/v1.0/get_bestauthor',methods=['POST'])
def get_bestauthor(): 
    #jdata = request.get_json();
    #tid = jdata['tid'];
    state = OPER_INVALID;     
    try:
        session = Session();
        sql = "select a.id,a.name,a.sex,a.signature,a.photo_url from user a limit 0,5 ";
        relist = session.query(User.id,User.name,User.sex,User.signature,User.photo_url).from_statement(sql).all(); 
        state = OPER_SUCCESS ; 
    except Exception,e:
        print e ;
        state = OPER_EXCEPTION ; 
    finally:
        session.close();
    items = [] ;
    for e in relist:
            d={
               'author_id':e.id,
               'author_sex':e.sex,
               'author_name':e.name,
               'author_signature':e.signature
            };
            
            if e.photo_url is not None :
                d['author_pic'] = NGINX_USERPHOTO_MEDIUM_URL_BASE+e.photo_url
            else:
                d['author_pic'] = "";
            items.append(d);   
            
    result = json.dumps({"state":state,"result":items},ensure_ascii=False,cls=AlchemyEncoder);    
    return result; 

@app.route('/caddy/api/v1.0/get_userdetail',methods=['POST'])
def get_userdetail():
    jdata = request.get_json();
    uid = jdata['uid'];
    requestor_id = jdata['requestor_id'];
    session =Session();
    state = OPER_INVALID;
    d={};
    flag = True;
    try:
        sql = "select a.*,(select count(*) from userfocus b where b.user_id=a.id and b.focus_type='002') topic_count,";
        sql += "(select count(*)from userfocus b where b.user_id = a.id and b.focus_type= '001') my_follow_count ,";
        sql += "(select count(*)from userfocus b where b.obj_id = a.id and b.focus_type ='001' ) follow_me_count ,";        
        if requestor_id == uid: #myself 
            sql += "(select count(*) from collect_pack b where b.create_by = a.id) pack_count,"
            sql +='(select false from dual ) is_focus';            
        else:     
            sql += "(select count(*) from collect_pack b where b.create_by = a.id and b.is_private = false) pack_count,"
            sql +="(select b.id from userfocus b where b.obj_id = a.id and b.user_id = %s and b.focus_type='001' limit 0,1 ) is_focus " % (requestor_id); 
        sql +=" from user a where a.id = %s" % uid ;        
        entry = session.query(User.email,User.profession,User.residence,User.education,
                              'topic_count','my_follow_count','follow_me_count','pack_count','is_focus').from_statement(sql).one();
        
        if entry.is_focus is None or bool(entry.is_focus) is False:
            flag = False ;
        d={
           'topic_count':entry.topic_count,
           'my_follow_count':entry.my_follow_count,
           'follow_me_count':entry.follow_me_count,
           'pack_count':entry.pack_count,
           'is_focus':flag,
           'email':entry.email,           
          'profession':entry.profession,
          'residence':entry.residence,
          'education':entry.education
        };
        state = OPER_SUCCESS;
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        session.close();
    return json.dumps({'state':state,'result':d},cls=AlchemyEncoder);

@app.route('/caddy/api/v1.0/get_userlist',methods=['POST'])
def get_userlist():
    jdata = request.get_json();
    s=jdata['slice'];
    off = jdata['off'];
    session=Session();
    items = [];
    state = OPER_INVALID;
    try:
        relist = session.query(User).filter(User.name.like('%'+s+'%')).\
                    offset(int(off)).limit(10).all();
        for e in relist:
            d={
                'id':e.id,
                'name':e.name,
                'sex':e.sex,
                'signature':e.signature
            };
            
            if e.photo_url is not None :
                d['photo'] = NGINX_USERPHOTO_MEDIUM_URL_BASE+e.photo_url
            else:
                d['photo'] = "";
            items.append(d);
            state = OPER_SUCCESS;
    except Exception ,e :
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        session.close();
    return json.dumps({'state':state,'result':items},cls=AlchemyEncoder);

if __name__ == '__main__':
    pass
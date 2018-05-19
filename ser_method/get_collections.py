#coding:utf-8
'''
Created on 
@author: ThinkPad
'''
import logging ;  
from ser_main import app ;
from ser_main.server_config import NGINX_IMAGE_SERVER_THUMBNAIL ,NGINX_IMAGE_SERVER_URI,\
        NGINX_USERPHOTO_MEDIUM_URL_BASE,NGINX_IMAGE_SERVER_COVER; 
from flask import request ;
from ser_model.db import Session;
from ser_model.base_model import Collection ,User;
from flask import json ;
from ser_model.base_model import AlchemyEncoder, Imagelib
from ser_method.constants import OPER_SUCCESS, PAGE_SIZE,\
    OPER_INVALID, OPER_EXCEPTION

@app.route('/caddy/api/v1.0/get_collections',methods=['POST'])
def get_collections():
    data_type = request.get_json().get('data_type');     
    items = [] ; 
    session = Session();
    if data_type == 'HOME_LIST':
        items = get_homelist(session,request); 
    elif data_type == 'HOT_RANK':
        items = get_ranklist(session,request);
    elif data_type == 'HOT_RECOMMEND':
        items = get_recommendlist(session,request);   
    elif data_type == 'PACK_LIST':
        items = get_packlist(session,request);
    result = json.dumps({"state":OPER_SUCCESS,"result":items},ensure_ascii=False,cls=AlchemyEncoder);
    session.close();
    return result,200,{'Cache-Control': 'max-age=50' }; 
    
#get the homepage collection list based on users' favor  
def get_homelist(session,request):
    items = [] ;   
    jdata = request.get_json();
    threshold = jdata['threshold'];
    action = jdata['action'];
    sql  = " select a.id as cid,a.title,a.content,a.abstract,a.type,a.cover,a.comment_count,a.last_modify,a.pack_id,a.create_by ,a.vote_count,";
    sql += " a.cisn,b.id as uid,b.name,b.photo_url ,b.sex,b.signature,";
    sql += " (select image_url from imagelib where collection_id = a.id and (type = 'THUMBNAIL' or type = 'COVER') limit 0,1) image_url ";
    sql += " from collection  a , user b,collect_pack c where a.create_by=b.id and a.state=1 and a.pack_id = c.id and c.is_private = false ";
    if action == 'INIT':
        sql += " and a.create_time <= now() order by a.id desc ";
        #sql +=" and YEARWEEK(date_format(a.last_modify,'%Y-%m-%d')) = YEARWEEK(now()) order by a.id desc ";
    elif action == 'UP':
        sql +=" and a.id < %s order by a.id desc " % threshold; 
    elif action == 'DOWN':
        sql += "and a.id > %s order by a.id  " % threshold; 
    sql += " limit %s,%s " % (0,PAGE_SIZE);
    try:
        relist = session.query('cid',Collection.title,Collection.content,Collection.cover,Collection.type,Collection.pack_id,Collection.cisn , 
                               Collection.abstract,Collection.create_by,Collection.last_modify,Collection.comment_count,
                               Collection.vote_count,User.name,User.sex,User.photo_url,User.signature,Imagelib.image_url).\
                        from_statement(sql).all();
        for e in relist :
            d = {
             'cid':e.cid,
             'title':e.title,
             'abstract':e.abstract,
             'type':e.type,
             'cisn':e.cisn,
             'pid':e.pack_id,
             'create_by':e.create_by,
             'vote_count':e.vote_count,
             'comment_count':e.comment_count,
             'name':e.name,
             'sex':e.sex,             
             'signature':e.signature,         
             'last_modify':e.last_modify.strftime("%Y-%m-%d %H:%M:%S")
            }; 
            if e.image_url is not None :
                d['image_url'] = str(NGINX_IMAGE_SERVER_THUMBNAIL+e.image_url.split('/')[-1])
            else :
                d['image_url'] = '';
                
            if e.photo_url is not None :
                d['photo'] = str(NGINX_USERPHOTO_MEDIUM_URL_BASE+e.photo_url)
            else:
                d['photo'] = ''; 
            if e.cover is not None:
                d['cover'] = str(NGINX_IMAGE_SERVER_URI+e.cover);
            else:
                d['cover'] = '' ; 
            items.append(d);
        #result = session.query(Collection,Topic).filter(Collection.topic_id == Topic.id).offset(off).limit(20).all();                                        
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
    #if dont want pass session ,we need to do this before session.close();
    #session.expunge_all();
    #@see detail http://stackoverflow.com/questions/8253978/sqlalchemy-get-object-not-bound-to-a-session?rq=1
    return items;

#get the hot rank collection list .
def get_ranklist(session,request):
    items = [];
    try:
        jdata = request.get_json();
        action = jdata['action'];
        off = jdata['off'];
                
        sql  = " select distinct a.id as cid,a.title,a.content,a.abstract,a.cover,a.type,a.cisn,"
        sql += " a.comment_count,a.last_modify,a.pack_id,a.create_by , a.vote_count, ";
        sql += " b.id as uid,b.name,b.photo_url ,b.sex,b.signature,";
        sql += " (select image_url from imagelib where collection_id = a.id and (type = 'THUMBNAIL' or type = 'COVER') limit 0,1) image_url ";
        sql += " from collection  a , user b ,collect_pack c where a.create_by=b.id and a.state=1 and a.pack_id = c.id and c.is_private = false ";
        sql += " and date_format(a.`last_modify`,'%Y-%m')=date_format(now(),'%Y-%m')  "        
        if int(off) == 0 :
            sql += " order by a.vote_count desc limit %s,%s " % (0,PAGE_SIZE);
        elif action == 'REQ_NEWDATA':
            sql += " and a.vote_count > %s order by a.vote_count desc limit 0, 5" %(jdata['threshold']);
        elif action == 'REQ_HISTORY' :
            sql += " order by a.vote_count desc limit %s, %s " % (int(off),PAGE_SIZE);    
        
        result = session.query('cid',Collection.title,Collection.abstract,Collection.cover,Collection.comment_count,Collection.cisn,
                Collection.content,Collection.type,Collection.pack_id,Collection.create_by,Collection.vote_count,
                User.name,User.sex,User.photo_url,User.signature,Imagelib.image_url).from_statement(sql).all();
            
        for e in result:
            d={
               'cid':e.cid,
               'title':e.title,
               'abstract':e.abstract,
               'type':e.type,
               'cisn':e.cisn,
               'pid':e.pack_id,
               'create_by':e.create_by,
               'vote_count':e.vote_count,
               'name':e.name,
               'sex':e.sex,             
               'signature':e.signature,
               'comment_count':e.comment_count
            };
             
            if e.image_url is not None :
                d['image_url'] = str(NGINX_IMAGE_SERVER_THUMBNAIL+e.image_url.split('/')[-1])
            else :
                d['image_url'] = '';
                
            if e.photo_url is not None :
                d['photo'] = str(NGINX_USERPHOTO_MEDIUM_URL_BASE+e.photo_url)
            else:
                d['photo'] = '';  
            
            if e.cover is not None:
                d['cover'] = str(NGINX_IMAGE_SERVER_URI+e.cover);
            else:
                d['cover'] = '' ; 
            items.append(d);
    except Exception ,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
    return items ;

#get the hot recommend collection list ,also based on user's favor .  
def get_recommendlist(session,off):    
    items = [];
    try:
        jdata = request.get_json();
        off = jdata['off'];
        action = jdata['action'];
        sql  = " select distinct a.id as cid,a.title,a.abstract,a.cover,a.content,a.cisn,";
        sql += " a.type,a.last_modify,a.pack_id,a.create_by , a.vote_count ,a.comment_count, ";
        sql += " b.id as uid,b.name,b.photo_url ,b.sex,b.signature,";
        sql += " (select image_url from imagelib where collection_id = a.id and (type = 'THUMBNAIL' or type = 'COVER') limit 0,1) image_url ";
        sql += " from collection  a , user b , collect_pack c where a.create_by = b.id and a.state=1 and a.pack_id = c.id and c.is_private = false";
        sql += " and date_format(a.`last_modify`,'%Y-%m')=date_format(now(),'%Y-%m') "
      
        if int(off) == 0 :
            sql += " order by a.share_count desc  limit %s,%s " % (0,PAGE_SIZE);
        elif action == 'REQ_NEWDATA':
            sql += " and a.share_count > %s order by a.share_count desc  limit 0, 5" %(jdata['threshold']);
        elif action == 'REQ_HISTORY' :
            sql += " order by a.share_count desc  limit %s, %s " % (int(off),PAGE_SIZE);    
        
        result = session.query('cid',Collection.title,Collection.abstract,Collection.cover,Collection.comment_count,Collection.cisn,
                Collection.content,Collection.type,Collection.pack_id,Collection.create_by,Collection.vote_count,
                User.name,User.sex,User.photo_url,User.signature,Imagelib.image_url).from_statement(sql).all();
        for e in result:
            d={
               'cid':e.cid,
               'title':e.title,
               'abstract':e.abstract,
               'type':e.type,
               'cisn':e.cisn,
               'pid':e.pack_id,
               'create_by':e.create_by,
               'vote_count':e.vote_count,
               'name':e.name,
               'sex':e.sex,             
               'signature':e.signature,
               'comment_count':e.comment_count
            };
            
            if e.image_url is not None :
                d['image_url'] = str(NGINX_IMAGE_SERVER_THUMBNAIL+e.image_url.split('/')[-1])
            else :
                d['image_url'] = '';
                
            if e.photo_url is not None :
                d['photo'] = str(NGINX_USERPHOTO_MEDIUM_URL_BASE+e.photo_url)
            else:
                d['photo'] = '';    
            
            if e.cover is not None:
                d['cover'] = str(NGINX_IMAGE_SERVER_URI+e.cover);
            else:
                d['cover'] = '' ; 
            items.append(d);
    except Exception ,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
    return items ;

def get_packlist(session,off):
    items = [];
    try:
        jdata = request.get_json();
        off = jdata['off'];
        pid = jdata['pid'];
        sql  = " select a.id as cid,a.title,a.abstract,a.content,a.type,a.cover,a.last_modify,"
        sql += " a.pack_id,a.create_by , a.vote_count , a.comment_count,a.cisn,";
        sql += " b.id as uid,b.name,b.photo_url ,b.sex,b.signature,";
        sql += " (select image_url from imagelib where collection_id = a.id and (type = 'THUMBNAIL' or type = 'COVER') limit 0,1) image_url ";
        sql += " from collection  a , user b where a.create_by=b.id and a.state=1  and a.pack_id = %s" % (pid);
        sql += " order by a.share_count desc  limit %s,%s " % (int(off),PAGE_SIZE);
                
        result = session.query('cid',Collection.title,Collection.abstract,Collection.cover,Collection.comment_count,Collection.cisn,
                Collection.content,Collection.type,Collection.pack_id,Collection.create_by,Collection.vote_count,
                 User.name,User.sex,User.photo_url,User.signature,Imagelib.image_url).from_statement(sql).all();
    
        print result ;
        for e in result:
            d={
               'cid':e.cid,
               'title':e.title,
               'abstract':e.abstract,
               'type':e.type,
               'cisn':e.cisn,
               'pid':e.pack_id,
               'create_by':e.create_by,
               'vote_count':e.vote_count,
               'name':e.name,
               'sex':e.sex,             
               'signature':e.signature,
               'comment_count':e.comment_count
            };
            
            if e.image_url is not None :
                d['image_url'] = str(NGINX_IMAGE_SERVER_THUMBNAIL+e.image_url.split('/')[-1])
            
            else :
                d['image_url'] = '';
            
            if e.photo_url is not None :
                d['photo'] = str(NGINX_USERPHOTO_MEDIUM_URL_BASE+e.photo_url)
            else:
                d['photo'] = '';  
                
            if e.cover is not None:
                d['cover'] = str(NGINX_IMAGE_SERVER_URI+e.cover);
            else:
                d['cover'] = '' ;             
            items.append(d);
    except Exception ,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
    return items ;

@app.route('/caddy/api/v1.0/get_collectiondetail',methods=['POST'])
def get_collectiondetail():
    jdata = request.get_json();
    cid = jdata['cid'];
    state = OPER_INVALID;
    result = {};
    session = Session();
    try:
        sql = " select a.id as cid, a.title,a.content,a.abstract,a.type,a.cover,a.pack_id,a.create_by,";
        sql +=" a.vote_count ,a.create_time,a.comment_count,a.cisn,"
        sql += " b.id as uid ,b.name,b.signature,b.sex,b.photo_url,";
        sql += " (select image_url from imagelib where collection_id = a.id and type = 'COVER' limit 0,1) image_url ";
        sql +=" from collection a ,user b where a.create_by = b.id and a.state=1 and a.id = %s" % (cid);
        entry = session.query('cid',Collection.title,Collection.content,Collection.abstract,Collection.cover,Collection.type,Collection.pack_id,Collection.create_time,
                              Collection.cisn,Collection.create_by,Collection.vote_count,'uid',User.name,User.signature,User.sex,User.photo_url,
                              Collection.comment_count,Imagelib.image_url).from_statement(sql).one();
        result={
            'uid':entry.uid,
            'name':entry.name,
            'signature':entry.signature,
            'sex':entry.sex,
            'cid':entry.cid,
            'cisn':entry.cisn,
            'title':entry.title,
            'abstract':entry.abstract,
            'content':entry.content,
            'type':entry.type,
            'pid':entry.pack_id,
            'create_by':entry.create_by,
            'vote_count':entry.vote_count,
            'comment_count':entry.comment_count,
            'create_time':entry.create_time.strftime('%Y-%m-%d')
        };       
        
        if entry.photo_url is not None :
            result['photo'] = str(NGINX_USERPHOTO_MEDIUM_URL_BASE+entry.photo_url)
        else:
            result['photo'] = "";    
        
        if entry.image_url is not None :
                result['cover_url'] = str(NGINX_IMAGE_SERVER_COVER+entry.image_url)
        else :
                result['cover_url'] = '';
        
        if entry.cover is not None:
            result['cover'] = str(NGINX_IMAGE_SERVER_URI+entry.cover);
        else:
            result['cover'] = '' ;         
        state = OPER_SUCCESS;
    except Exception ,e: 
        print e ;  
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION ; 
    finally:
        session.close();
    return json.dumps({'state':state,'result':result},cls = AlchemyEncoder);

if __name__ == '__main__':
    pass
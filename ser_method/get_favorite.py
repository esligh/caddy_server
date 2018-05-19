'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app ;
from ser_model.db import Session;
from flask import json ,request;
from ser_model.base_model import AlchemyEncoder,Collection,User
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION,\
    PAGE_SIZE
from ser_main.server_config import NGINX_USERPHOTO_URL_BASE

@app.route('/caddy/api/v1.0/get_favorite',methods=['POST'])
def get_favorite():
    jdata = request.get_json();
    session = Session();
    items = [] ;
    state = OPER_INVALID ;
    off = int(jdata['off']);
    try:
        sql  = " select a.id as cid,a.title,a.abstract,a.content,a.type,a.last_modify,a.pack_id,a.create_by , a.vote_count , ";
        sql += " a.cisn,b.name,b.sex,b.signature,b.photo_url ,";
        sql += " (select count(*) from comment c where c.collection_id = a.id ) comment_count "
        sql += " from collection  a , user b, favorite f  where a.create_by = b.id "
        sql += " and a.id = f.collection_id and a.state= 1 and  f.create_by = %s " % (jdata['uid']);
        sql += " and f.box_id = %s " % (jdata['box_id']);
        sql += " order by a.last_modify desc  limit %s,%s " % (off,PAGE_SIZE);
        relist = session.query('cid',Collection.title,Collection.abstract,Collection.cisn,
                Collection.content,Collection.type,Collection.pack_id,Collection.create_by,Collection.vote_count,
                User.name,User.sex,User.signature,User.photo_url,'comment_count').from_statement(sql).all();
        for e in relist:
            d={
               'id':e.cid,
               'title':e.title,
               'abstract':e.abstract,
               'cisn':e.cisn,
               'vote_count':e.vote_count,
               'create_by':e.create_by,
               'comment_count':e.comment_count,
               'name':e.name,
               'signature':e.signature,
               'sex':e.sex                
            }
            if e.photo_url is not None :
                d['photo'] = str(NGINX_USERPHOTO_URL_BASE+e.photo_url)
            else:
                d['photo'] = ''; 
            items.append(d);
        state = OPER_SUCCESS;
    except Exception,e :
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION ; 
    finally:
        session.close();        
    return json.dumps({'state':state,'result':items},cls=AlchemyEncoder);
if __name__ == '__main__':
    pass
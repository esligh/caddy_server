'''
Created on 

@author: ThinkPad
'''
import logging; 
from ser_main import app ;
from ser_main.server_config import NGINX_USERPHOTO_URL_BASE; 
from flask import request ,json;
from ser_model.db import Session; 
from ser_model.base_model import Comment,User,AlchemyEncoder;
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION
# from ser_main import clients;

@app.route('/caddy/api/v1.0/get_comments', methods=['POST'])
def get_comments():
    jdata = request.get_json();
    off = jdata['off'];
    cid = jdata['cid'];
    state = OPER_INVALID;
    items = [] ;
    try:
        session = Session();
        sql = "select a.id,a.collection_id,a.type,a.content,a.create_by,a.create_time,a.vote_count ,b.name,b.sex,b.photo_url,";
        sql +=  "(select name from user c where c.id = a.receiver_id ) receiver_name ";
        sql += " from comment a,user b where a.create_by = b.id and a.collection_id = %s " % cid;
        sql += " order by a.create_time "; 
        sql += " limit %s,%s " %(int(off),10);
        relist =  session.query(Comment.id,Comment.collection_id,Comment.type,Comment.content,Comment.create_by,Comment.create_time,
                        Comment.vote_count,User.name,User.sex,User.photo_url,'receiver_name').from_statement(sql).all();
        state = OPER_SUCCESS;
        for e in relist:
            d={
               'comment_id':e.id,
               'cid':e.collection_id,
               'type':e.type,
               'content':e.content,
               'create_by':e.create_by,
               'create_time':e.create_time.strftime('%Y-%m-%d'),
               'vote_count':e.vote_count,
               'user_name':e.name,
               'user_sex':e.sex,
               'receiver_name':e.receiver_name
            };
            
            if e.photo_url is not None :
                d['user_pic'] = NGINX_USERPHOTO_URL_BASE+e.photo_url
            else:
                d['user_pic'] = "";
            items.append(d);
    except Exception ,e :
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION; 
    finally:
        session.close();
    
#     uid = jdata['uid'];
#     if  uid != '' and clients[uid] is not None:    
#         print clients[uid];  
#         print clients[uid].socketio ; 
#         clients[uid].socketio.emit('ping event',{'data':42});   
#     #socketio.emit('ping event', {'data': 42});
    return json.dumps({'state':state,'result':items},cls=AlchemyEncoder);
       
@app.route('/caddy/api/v1.0/get_commentcollections', methods=['POST'])
def get_commentcollections():
    jdata = request.get_json();
    uid = jdata['uid'];
    session = Session();
    items=[];
    state = OPER_INVALID; 
    try:
        sql = " select a.id,a.title ";
        sql += " from collection a , comment b where a.id = b.collection_id and a.create_by = %s " % (uid);         
        
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
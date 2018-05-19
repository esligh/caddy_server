'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app ;
from ser_model.db import Session;
from flask import json,request;
from ser_model.base_model import AlchemyEncoder , Collection,User
from ser_method.constants import OPER_INVALID, OPER_EXCEPTION, OPER_SUCCESS ;
from ser_model.base_model import UserAction
from ser_method.constants import PAGE_SIZE
 
@app.route('/caddy/api/v1.0/get_useraction',methods=['POST'])
def get_useraction():
    jdata = request.get_json();
    uid = jdata['uid']; 
    obj_id = jdata['obj_id'];
    actions = '';
    state = OPER_INVALID;
    try:  
        session = Session();     
        relist = session.query(UserAction).filter(UserAction.uid==uid,
            UserAction.obj_id==obj_id).all();
        for e in relist:
                actions+=e.action_type;
                actions+=',';
        state = OPER_SUCCESS;        
    except Exception,e: 
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally: 
        session.close();
    result = json.dumps({'state':state,'actions':actions},cls=AlchemyEncoder);
    return result ;

@app.route('/caddy/api/v1.0/get_actionlist',methods=['POST'])
def get_actionlist():
    jdata = request.get_json();    
    uid = jdata['uid']; 
    off = jdata['off'];  
    state = OPER_INVALID;
    items = [] ; 
    try:
        sql =  " select a.action_type,b.id,b.title,b.content,b.type,b.abstract,c.name " ; 
        sql += " from user_action a, collection b ,user c " ;   
        sql += " where a.obj_id = b.id and a.uid = c.id and "  ;  
        sql += " a.action_type in ('1000','1100','1200') and b.create_by = %s " % uid ;        
        sql += " order by a.create_time desc limit %s,%s" % (int(off),PAGE_SIZE);  
         
        session = Session();   
        relist = session.query(UserAction.action_type,Collection.id,Collection.type,Collection.content,
                               Collection.abstract,User.name).from_statement(sql).all();
        for e in relist :
            d={
            'cid':e.id,
            'type':e.type,
            'name':e.name,
            'action_type':e.action_type,
            'abstract':e.abstract
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
    return json.dumps({'state':state,'result':items});    
if __name__ == '__main__':
    pass
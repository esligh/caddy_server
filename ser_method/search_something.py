'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app ;
from ser_model.db import Session;
from ser_model.base_model import Collection,CollectPack
from flask import json,request ;
from ser_model.base_model import AlchemyEncoder
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION

@app.route('/caddy/api/v1.0/get_contentlist',methods=['POST'])
def get_contentlist():
    jdata = request.get_json();
    s = jdata['slice'];
    off = jdata['off'];
    items = [];
    session = Session();
    state = OPER_INVALID;
    try:
        relist = session.query(CollectPack).filter(CollectPack.pack_name.like('%'+s+'%'))\
                    .offset(int(off)).limit(5).all();
        for e in relist:
            d={
               'tag':'collectpack',
               'id':e.id,
               'cisn':e.cisn,
               'pack_name':e.pack_name,
               'focus_count':e.focus_count,
               'collect_count':e.collect_count,
               'create_by':e.create_by
            }
            items.append(d);
        relist = session.query(Collection).filter(Collection.title.like('%'+s+'%')).\
                    offset(int(off)).limit(10-len(items)).all();
        for e in relist:
            d={
                'tag':'collection',
                'id':e.id,
                'cisn':e.cisn,
                'title':e.title,
                'vote_count':e.vote_count,
                'create_by':e.create_by
            };
            items.append(d);
        state = OPER_SUCCESS;
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state =OPER_EXCEPTION;
    finally:
        session.close();                   
    return json.dumps({'state':state,'result':items},cls = AlchemyEncoder);
     
if __name__ == '__main__':
    pass
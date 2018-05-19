'''
Created on

@author: ThinkPad
'''
import logging ; 
from ser_main import app; 
from ser_model.db import Session;
from flask import json ,request;
from ser_model.base_model import AlchemyEncoder,Imagelib
from ser_method.constants import OPER_SUCCESS,OPER_INVALID, OPER_EXCEPTION

@app.route('/caddy/api/v1.0/get_imageinfo',methods=['POST'])
def get_imageinfo():
    jdata = request.get_json();
    cid = jdata['cid'];    
    state = OPER_INVALID ; 
    items = [] ;
    session = Session(); 
    try:
        relist = session.query(Imagelib).filter(Imagelib.collection_id == cid).all();
        for e in relist :
            d = {
            'id':e.id ,
            'img_uri':e.image_name,
            'img_url':e.image_url
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
    return json.dumps({'state':state,'result':items},cls= AlchemyEncoder);
if __name__ == '__main__':
    pass
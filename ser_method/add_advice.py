'''
Created on 

@author: ThinkPad
'''

import logging ; 
from ser_main import app;
from flask import request,json ;
from ser_model.db import Session;
from ser_method import constants
from ser_model.base_model import Advice 

@app.route('/caddy/api/v1.0/add_advice',methods=['POST'])
def add_advice():
    jdata = request.get_json();
    state = constants.OPER_INVALID;
    try:
        session = Session();
        item = Advice( advice= jdata['advice'], contact = jdata['contact'],
                       adviser_id = jdata['adviser_id']);    
        session.add(item);   
        session.commit();
        state = constants.OPER_SUCCESS;
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog.'.join(__name__));
        logger.error(e);
        state = constants.OPER_EXCEPTION;
    finally:
        session.close();
    return json.dumps({'state':state});

if __name__ == '__main__':
    pass
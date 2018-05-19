'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app ; 
from flask import json;
from ser_model.base_model import ServerConfig ; 
from ser_model.db import Session; 
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION

@app.route('/caddy/api/v1.0/get_appinfo', methods=['GET'])
def get_appinfo():
    state = OPER_INVALID;
    values = [] ; 
    try:
        session = Session();
        relist = session.query(ServerConfig.cfg_type,ServerConfig.cfg_key,ServerConfig.cfg_name,
                               ServerConfig.field_a,ServerConfig.field_b).filter(ServerConfig.cfg_type == 'VERSION_INFO').all();
        for e in relist:
            d={
               'cfg_key' : e.cfg_key,             
               'cfg_name': e.cfg_name,
               'cfg_value_a': e.field_a,
               'cfg_value_b':e.field_b                
            };
            values.append(d);
    except Exception,e:
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        state = OPER_SUCCESS;
    return json.dumps({'state':state,'result':values}); 

if __name__ == '__main__':
    pass
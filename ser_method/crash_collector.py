'''
Created on 

@author: ThinkPad
'''
import logging ; 
from flask import request ;
from flask import json ; 
from ser_main import app ; 
from ser_method import constants
from ser_main.server_config import UPLOAD_LOG_PATH

@app.route('/caddy/api/v1.0/crash_collector',methods=['POST'])
def do_crash():
    state = constants.OPER_INVALID;
    try :
        filename = request.form['file_name'];
        f = request.files.get('data');
        data = f.read();
        path = UPLOAD_LOG_PATH+filename; 
        output = open(path ,'wb');
        output.write(data);
        output.close();
        state = constants.OPER_SUCCESS;
    except Exception ,e :
        state = constants.OPER_EXCEPTION; 
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
    return json.dumps({'state':state});

if __name__ == '__main__':
    pass
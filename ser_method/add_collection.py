'''
Created on 

@author: ThinkPad
'''

import re,logging ; 
from ser_main import app ,auth;
from flask import request ;
from ser_model.db import Session;
from ser_model.base_model import Collection;
from flask.json import jsonify
from ser_method import constants
from ser_model.base_model import CollectPack, CTYPE_TEXTIMG
from ser_util.auth_verify import verify_password ; 
from ser_main.server_config import NGINX_IMAGE_SERVER_URI
from datetime import datetime

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/add_collection',methods=['POST'])
@auth.login_required
def add_collection():
    jdata = request.get_json();
    uid = jdata['create_by'];
    pid = jdata['pack_id'];
    ctype = jdata['type'] ;  #collection type 
    content = jdata['content']; 
    abstract = jdata['abstract'];
    cover = jdata['cover'];
    state = constants.OPER_INVALID;
    result = {};
    if ctype == CTYPE_TEXTIMG :
        content = replace_url(content); 
    try:
        session = Session();
        item = Collection(type=ctype,title=jdata['title'],cover=cover,content=content,abstract = abstract,\
                          pack_id = pid,cisn = jdata['cisn'],create_by=uid);     
        session.query(CollectPack).filter(CollectPack.id == pid).update({
                                CollectPack.collect_count: CollectPack.collect_count + 1});                                      
        session.add(item);
        session.commit();
        result['cid'] = item.id ; 
        state = constants.OPER_SUCCESS;
    except Exception,e:
        print e ; 
        logger = logging.getLogger('watch_dog.'.join(__name__));
        logger.error(e);
        state = constants.OPER_EXCEPTION;
    finally:
        session.close();
    result['state'] = state ; 
    return jsonify(result),201;

def f(m):
    d = m.groupdict();
    return '![]('+NGINX_IMAGE_SERVER_URI+d['url']+')';

def replace_url(text):
    p = re.compile("!\[.*\]\((?P<url>.*)\)");
    return p.sub(f,text);    
            
if __name__ == '__main__':
    pass
'''
Created on 
@author: ThinkPad
'''
import logging ; 
from ser_main import app,auth ;
from ser_model.db import Session;
from ser_model.base_model import Collection;
from flask import json ;
from flask import request ; 
from ser_util.auth_verify import verify_password ; 
from ser_method.constants import OPER_INVALID, OPER_SUCCESS, OPER_EXCEPTION
from ser_main.server_config import NGINX_IMAGE_SERVER_URI
import re ; 

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 


@app.route('/caddy/api/v1.0/update_collection',methods=['POST'])
@auth.login_required
def update_collection():
    jdata = request.get_json();
    cid = jdata['cid'];
    fields={}
    if 'title' in jdata :
        fields['title'] = jdata['title'];
    if 'content' in jdata:
        content = jdata['content']
        content = replace_url(content);
        fields['content'] = content; 
    if 'type' in jdata :
        fields['type'] = jdata['type'];
    if 'vote_count' in jdata :
        fields['vote_count'] = jdata['vote_count'];
    if 'bro_count' in jdata :
        fields['bro_count'] =jdata['bro_count'];
    if 'share_count' in jdata:
        fields['share_count'] = jdata['share_count'];
    if 'visit_count' in jdata :
        fields['visit_count'] = jdata['visit_count'];
    if 'focus_count' in jdata:
        fields['focus_count']  = jdata['focus_count'];
    if 'cover' in jdata:
        fields['cover'] = jdata['cover'];   
    state = OPER_INVALID;
    try:       
        session = Session();
        session.query(Collection).filter(Collection.id == cid).update(fields); 
        session.commit();
        state = OPER_SUCCESS;
    except Exception ,e :
        print e ;
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = OPER_EXCEPTION;
    finally:
        session.close();
    return json.dumps({'state':state});

def f(m):
    d = m.groupdict();
    return '![]('+NGINX_IMAGE_SERVER_URI+d['url']+')';

def replace_url(text):
    p = re.compile("!\[.*\]\((?P<url>.*)\)");
    return p.sub(f,text);    

if __name__ == '__main__':
    pass
'''
Created on 

@author: ThinkPad
'''
import logging ; 
from ser_main import app,auth ;
from flask import request ;
from ser_model.db import Session;
from flask.json import jsonify ; 
from ser_method import constants ;
from ser_model.base_model import Comment,Collection;
from ser_method.constants import OPER_INVALID
from ser_util.auth_verify import verify_password ; 
from ser_main import clients;

@auth.verify_password
def verify_pwd(username_or_token, password):
    # firstly, try to authenticate by token
    return verify_password(username_or_token, password) ; 

@app.route('/caddy/api/v1.0/add_comment', methods=['POST'])
@auth.login_required
def add_comment():
    jdata = request.get_json();
    state = OPER_INVALID;
    cid = jdata['cid']; 
    receiver_id = jdata['receiver_id'];
    comment_type = jdata['type'];
    try:
        session = Session();  
        item = Comment(collection_id=cid, type=comment_type,content = jdata['content'],
                receiver_id = receiver_id,create_by=jdata['create_by']);
        session.add(item);
        session.commit();        
        #use trigger more flexible 
        session.query(Collection).filter(Collection.id == cid).update({
                                Collection.comment_count: Collection.comment_count + 1});                          
               
        session.commit();            
        state = constants.OPER_SUCCESS;
    except Exception, e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = constants.OPER_EXCEPTION;
    finally:
        session.close();
    
    if receiver_id in clients.keys():
        data = {'event_type':'NEW_COMMENT','comment_type':comment_type};
        clients[receiver_id].socketio.emit('event',data);   
    return jsonify({'state':state});

if __name__ == '__main__':
    pass
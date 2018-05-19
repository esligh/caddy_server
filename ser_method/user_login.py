'''
Created on 

@author: ThinkPad

this module deal the app login process .
'''
import datetime ;
from ser_main import app,auth ;
from flask import request;
from flask import jsonify,g ;
from ser_model.db import Session; 
from ser_model.base_model import User;
from ser_method.constants import LOGIN_NFUSER, LOGIN_SUCCESS, LOGIN_PWDWRONG
from ser_main.server_config import NGINX_USERPHOTO_BIG_URL_BASE
COOKIE_EXPIRES_TIME_DURARING = 7776000;#three months 3600*24*30*3

'''
@auth.verify_password
def verify_password(useremail_or_token, password):
    # first try to authenticate by token
    db_session = Session();
    user = User.verify_auth_token(useremail_or_token)
    if not user:
        # try to authenticate with email/password
        user = db_session.query(User).filter_by(email=useremail_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user;
    db_session.close();
    return True ; 
'''

@app.route('/caddy/api/v1.0/user_login', methods=['POST'])
def do_login():
    # data = get_json() supported by Flask v0.10
    u_email = request.get_json().get('email') ;    
    u_pwd = request.get_json().get('pwd');
    login_state = '-1';
    login_desc = '';     
    session = Session();
    
    entry = session.query(User).filter(User.email==u_email).first();
    print entry ; 
    if entry is None:
        login_state = LOGIN_NFUSER;  # not found user;
        login_desc = 'not found the user';
    elif entry.email == u_email and entry.verify_password(u_pwd):
        print entry.verify_password(u_pwd),u_pwd ; 
        login_state = LOGIN_SUCCESS;  # login success 
        login_desc = 'login success';
        #update state operation occurs  when clients login completely; 
#        session.query(User).filter(User.id==entry.id).update({User.login_state:1});       
        g.user = entry ;   
    elif entry.email ==u_email and not entry.verify_password(u_pwd):
        login_state = LOGIN_PWDWRONG;
        login_desc = 'user password is wrong.';    
    result = {
              'state':login_state,
              'desc' :login_desc 
    }        
    if login_state == LOGIN_SUCCESS:
        token = g.user.generate_auth_token(COOKIE_EXPIRES_TIME_DURARING);
        now =datetime.datetime.now();
        delta = datetime.timedelta(seconds=COOKIE_EXPIRES_TIME_DURARING);
        n_days = now+delta;   
        expirydate = n_days.strftime('%Y-%m-%d %H:%M:%S');
        result['token']=token.decode('ascii');
        print result['token'];
        result['expirydate']=expirydate;
        #can add more info to return  
        info = {'user_id':g.user.id,'user_name':g.user.name,'user_sex':g.user.sex,'signature':g.user.signature,
                'user_email':g.user.email,'login_state':1,'reg_state':g.user.reg_state};
        
        if g.user.photo_url is not None :
            info['user_photo'] = NGINX_USERPHOTO_BIG_URL_BASE+g.user.photo_url
        else:
            info['user_photo'] = "";
        
        result['user_info'] = info ; 
        
    session.close();  
    #return jsonify(result),201;
    return jsonify(result);
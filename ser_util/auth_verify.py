'''
Created on 

@author: ThinkPad
'''
from ser_main import auth ;
from ser_model.db import Session;
from ser_model.base_model import User;
from flask import g ; 

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

if __name__ == '__main__':
    pass
'''
Created on 

@author: ThinkPad
'''

from ser_main import app,auth;
from flask import jsonify ,g;
import datetime ; 
COOKIE_EXPIRES_TIME_DURARING = 15552000 ;
                        
@app.route('/caddy/api/v1.0/get_token',methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(COOKIE_EXPIRES_TIME_DURARING);
    now =datetime.datetime.now();
    delta = datetime.timedelta(seconds=COOKIE_EXPIRES_TIME_DURARING);
    n_days = now+delta;   
    expirydate = n_days.strftime('%Y-%m-%d %H:%M:%S');
    return jsonify({'token': token.decode('ascii'), 'expirydate': expirydate})

if __name__ == '__main__':
    pass
'''
the app falsk instance
@author:esli
@see:   
'''

from flask import Flask
from flask_httpauth import HTTPBasicAuth ;
import redis ; 
from flask_socketio import emit,send ;  
from flask_socketio import SocketIO;

rd = redis.StrictRedis(host='localhost', port=6379, db=0);
auth =HTTPBasicAuth();
#gen use os.urandom(24)
clients = {}; #client map 
app = Flask(__name__); #server instance
app.secret_key = '\xfe\xc67C\xee\xc9\x1f\xe0=L\x9a\xb2\xc6/Hp[\x0b\x93\x16^w\xf1'
socketio = SocketIO(app);#socketio instance ,wrapper of app .

from ser_method import get_auth_token ; 
from ser_method import user_login ;
from ser_method import user_reg ;
from ser_method import add_collection ;
from ser_method import del_collection ;
from ser_method import update_collection ; 
from ser_method import get_collections;
from ser_method import get_topicinfo
from ser_method import simple_upload ;
from ser_method import get_userinfo ; 
from ser_method import get_collectpack ;
from ser_method import add_collectpack ;
from ser_method import del_collectpack;
from ser_method import add_follows;
from ser_method import del_follows ;
from ser_method import add_favoritebox ;
from ser_method import add_favorite ; 
from ser_method import get_favoriteboxes ;
from ser_method import get_favorite ;
from ser_method import get_focus ;  
from ser_method import add_comment ;
from ser_method import get_comments ; 
from ser_method import search_something ;  
from ser_method import update_collectpack ;
from ser_method import del_comment ; 
from ser_method import update_userinfo ; 
from ser_method import get_message ; 
from ser_method import add_message ; 
from ser_method import get_images ;
from ser_method import del_imgs;
from ser_method import add_useraction;
from ser_method import del_useraction;
from ser_method import get_useraction;
from ser_method import del_favorite;
from ser_method import del_favoritebox ;
from ser_method import update_message ; 
from ser_method import get_appinfo ; 
from ser_method import add_report ; 
from ser_method import add_advice ; 
from ser_method import crash_collector ; 
from ser_method import login_over ; 

########################################
from ser_event import handler_events ; 
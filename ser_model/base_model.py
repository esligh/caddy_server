'''
file user_model.py
@author eslin
@copyright: v1.0
@see: http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
 
this file contains all of the app models ,maping the database
table .the method layout will use these models to create relative 
view for client. 
'''

from ser_main import app ; 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import VARCHAR, BIGINT,  DATETIME, INTEGER, \
    TEXT, CHAR, BOOLEAN
from datetime import datetime;
from db import engine
from flask import json ;
from sqlalchemy.ext.declarative import DeclarativeMeta
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context;
from ser_model.db import Session;
from sqlalchemy.sql.functions import func

Base = declarative_base();
    
#Table User
class User(Base):
    __tablename__='user';
    __table_args__={
        'mysql_charset':'utf8'
    };
    id=Column(BIGINT,primary_key=True);
    name=Column(VARCHAR(80),unique=True);
    pwd =Column(VARCHAR(100));
    sex=Column(VARCHAR(2));
    age=Column(INTEGER);
    photo_url = Column(VARCHAR(300));
    profession = Column(VARCHAR(100));
    residence = Column(VARCHAR(100));
    education = Column(VARCHAR(100));
    email=Column(VARCHAR(100),unique=True);
    signature=Column(VARCHAR(128));
    reg_state =Column(CHAR(1),default='0');
    login_state =Column(CHAR(1));
    acti_code=Column(VARCHAR(50),nullable=False); # active code 
    focus_count = Column(INTEGER,default=0);
    dev_id =  Column(VARCHAR(200));
    rp_weight = Column(INTEGER,default=100);
    reg_time=Column(DATETIME,default=func.now());
    comment=Column(VARCHAR(200),default='');   
    reserved=Column(VARCHAR(200));
    topics = relationship('Topic',backref='creator', lazy='dynamic');
    collectins = relationship('Collection',backref='collector',lazy='dynamic');
    userfoucs = relationship('Userfocus',backref='follower',lazy='dynamic');
    favoriteboxs = relationship('FavoriteBox',backref='creator',lazy='dynamic');
    favorites = relationship('Favorite',backref='creator',lazy='dynamic');
    useraction = relationship('UserAction',backref='creator',lazy='dynamic');       
    def hash_password(self, password):
        self.pwd = pwd_context.encrypt(password)
        
    def verify_password(self,password):
        return pwd_context.verify(password,self.pwd);
    
    def generate_auth_token(self,expiration = 600):
        s = Serializer(app.secret_key,expires_in=expiration);
        
        result= s.dumps({'id':self.id});
        return result; 
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.secret_key);
        try:
            data = s.loads(token);
        except SignatureExpired:
            return None ; 
        except BadSignature:
            return None ;
        db_session = Session();        
        user =  db_session.query(User).filter(User.id==data['id']);
        db_session.close();
        return user ; 
            
#static  details @see ser_staticmgr.topic_mgr.  
class Topic(Base):
    __tablename__='topic'
    __table_args__={
        'mysql_charset':'utf8'
    };
    id=Column(INTEGER,primary_key=True);
    level_code=Column(VARCHAR(5),nullable=False); #leve_code define the topic's level on the topic tree.
    level_path=Column(VARCHAR(50));
    topic_name=Column(VARCHAR(50),unique=True);
    pic_url = Column(VARCHAR(300));
    topic_desc=Column(VARCHAR(500));
    focus_count=Column(INTEGER,default=0);
    create_by=Column(BIGINT,ForeignKey(User.id));
    create_time=Column(DATETIME,server_default=func.now());

#collection catalog ,differ with FavoriteBox .    
class CollectPack(Base):
    __tablename__='collect_pack'
    __table_args__={
        'mysql_charset':'utf8'
    };
    id=Column(BIGINT,primary_key=True);
    type = Column(VARCHAR(3),nullable=False);
    pack_name=Column(VARCHAR(200),nullable=False);
    pack_desc=Column(VARCHAR(200));
    create_by=Column(BIGINT,ForeignKey('user.id'));
    topic_id = Column(VARCHAR(50));
    csn = Column(VARCHAR(200)) ; #CopyRight Serial Number 
    focus_count=Column(INTEGER,default=0);   
    collect_count=Column(INTEGER,default=0);
    state = Column(INTEGER,default=1);
    create_time=Column(DATETIME,server_default=func.now());
    is_private = Column(BOOLEAN,default=False);
    collections = relationship('Collection',backref='folder', lazy='dynamic');

#image instance  
class Imagelib(Base):
    __tablename__='imagelib'
    __table_args__={
        'mysql_charset':'utf8'
    };
    id=Column(BIGINT,primary_key = True);
    type = Column(VARCHAR(20)); 
    image_name = Column(VARCHAR(260));
    image_url = Column(VARCHAR(260));
    position = Column(VARCHAR(100));#GPS pos : unused 
    collection_id = Column(BIGINT,ForeignKey('collection.id'),nullable=False);
    create_time = Column(DATETIME,server_default=func.now())

#collection type 
CTYPE_TEXT = '0';
CTYPE_TEXTIMG='1';
CTYPE_IMG = '2';

class Collection(Base):
    __tablename__='collection'
    __table_args__={
        'mysql_charset':'utf8'
    };
    id=Column(BIGINT,primary_key=True);
    type=Column(VARCHAR(2),nullable=False); 
    title=Column(VARCHAR(100),nullable=False);
    cover = Column(VARCHAR(300)); 
    content=Column(TEXT);
    abstract = Column(VARCHAR(150));
    pack_id=Column(BIGINT,ForeignKey('collect_pack.id'));
    cisn = Column(VARCHAR(200)) ; #CopyRight Identify Serial Number(cisn) 
    create_by=Column(BIGINT,ForeignKey('user.id'));
    vote_count=Column(INTEGER,default=0);
    bro_count=Column(INTEGER,default=0);
    share_count=Column(INTEGER,default=0);
    visit_count=Column(INTEGER,default=0);
    focus_count=Column(INTEGER,default=0);
    comment_count = Column(INTEGER,default=0);
    state = Column(INTEGER,default=1);#1 valid 0 invalid 
    create_time=Column(DATETIME,server_default=func.now());
    last_modify=Column(DATETIME,server_default=func.now());
    reserved = Column(VARCHAR(100));
    images = relationship('Imagelib',backref='relevance', lazy='dynamic');
    favorites = relationship('Favorite',backref='son', lazy='dynamic');
    comments = relationship('Comment',backref='target',lazy='dynamic');
    
    #def __repr__(self):
    #    return "{'title':'%s','content':'%s'}" % (self.title,self.content);

FOLLOW_TYPE_COLLECTOR = '001';
FOLLOW_TYPE_TOPIC = '002';
FOLLOW_TYPE_COLLECTPACK = '003';

class Userfocus(Base):
    __tablename__ = 'userfocus'
    __table_args__={
        'mysql_charset':'utf8'
    };
    id = Column(INTEGER,primary_key=True);
    user_id =Column(BIGINT,ForeignKey('user.id'));
    focus_type = Column(VARCHAR(3),nullable=False);#001 Collector ;002 Topic; 003 Collection etc.
    obj_id = Column(BIGINT,nullable=False);
    create_time=Column(DATETIME,server_default=func.now());

class FavoriteBox(Base):
    __tablename__ = 'favorite_box'
    __table_args__={
        'mysql_charset':'utf8'
    };
    id= Column(INTEGER,primary_key = True);
    type = Column(VARCHAR(3),nullable=False);
    box_name = Column(VARCHAR(200),nullable=False);
    box_desc = Column(VARCHAR(200));
    focus_count = Column(INTEGER,default=0);
    box_count = Column(INTEGER,default=0);
    is_private = Column(BOOLEAN,default = False);
    create_by=Column(BIGINT,ForeignKey('user.id'));
    create_time = Column(DATETIME,server_default=func.now());
    favorites = relationship('Favorite',backref='myelement',lazy='dynamic');
      
class Favorite(Base):
    __tablename__='favorite' 
    __table_args__={
        'mysql_charset':'utf8'
    };
    id = Column(BIGINT,primary_key=True);
    collection_id = Column(BIGINT,ForeignKey('collection.id'));
    box_id = Column(INTEGER,ForeignKey('favorite_box.id'));
    create_by = Column(BIGINT,ForeignKey('user.id'));    
    create_time = Column(DATETIME,server_default=func.now());

class Comment(Base):
    __tablename__="comment"
    __table_args__ = {
        'mysql_charset':'utf8'
    };
    id = Column(BIGINT,primary_key=True);
    collection_id = Column(BIGINT,ForeignKey('collection.id'));
    receiver_id = Column(BIGINT,ForeignKey('user.id'));
    type = Column(VARCHAR(2)); #10 common #20 reply 
    content = Column(TEXT,nullable = False);
    report_count = Column(INTEGER,default=0);
    vote_count = Column(INTEGER,default=0);
    create_by = Column(BIGINT,ForeignKey('user.id')); 
    create_time = Column(DATETIME,server_default=func.now());
    comment_sender = relationship('User',foreign_keys=[create_by]);
    comment_receiver = relationship('User',foreign_keys=[receiver_id]);
    #@see detail:http://docs.sqlalchemy.org/en/rel_1_0/orm/join_conditions.html 
    #            about Handling Multiple Join Paths 
    #@ref error :Could not determine join condition between parent/child tables on relationship User.comments 
    #            -there are multiple foreign key paths linking the tables.  
    #            Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as 
    #            containing a foreign key reference to the parent table.
     
class Message(Base):
    __tablename__="message"
    __table_args__={
        'mysql_charset':'utf8'
    };
    id = Column(BIGINT,primary_key = True);
    type = Column(VARCHAR(3));
    content= Column(TEXT);
    is_read = Column(BOOLEAN,default=False);
    sender_id = Column(BIGINT,ForeignKey('user.id'));
    receiver_id = Column(BIGINT,ForeignKey('user.id'));
    accepted = Column(BOOLEAN,default = False);
    accept_time = Column(DATETIME);
    create_time = Column(DATETIME,server_default=func.now()); 
    msg_sender = relationship('User',foreign_keys=[sender_id]);
    msg_receiver = relationship('User',foreign_keys=[receiver_id]);


#this table will record the action of user ,eg vote ,collect, comment etc.
# -- user action type --
ACTION_VOTE_COLLECTION =  '1000';
ACTION_COLLECT_COLLECTION  = '1100';
ACTION_COMMENT_COLLECTION  = '1200'; 
ACTION_OPPOSE_COLLECTION = '1300';
ACTION_FOCUS_COLLECTION = '1400';
ACTION_FOCUS_TOPIC = '2000';
ACTION_FOCUS_COLLECTOR = '3000';

ACTION_REPORT_COLLECTION = "4000";

#record of user action 
class UserAction(Base):
    __tablename__="user_action"
    __table_args__={
        'mysql_charset':'utf8'         
    };
    id=Column(BIGINT,primary_key = True);
    action_type=Column(VARCHAR(4)); #@see detail up 
    uid = Column(BIGINT,ForeignKey('user.id')); # the user who produce this action
    obj_id = Column(BIGINT); # the object of action 
    create_time =  Column(DATETIME,server_default=func.now());

#static : server configuration see ser_staitcmgr.config_mgr  
class ServerConfig(Base):
    __tablename__="server_config";
    __table_args__={
        'mysql_charset':'utf8'
    };
    id=Column(INTEGER,primary_key = True);
    cfg_type = Column(VARCHAR(30),nullable=False); #configuration type 
    cfg_key = Column(VARCHAR(30),unique=True); #configuration key unique   
    cfg_name = Column(VARCHAR(50)); #configuration name 
    field_a = Column(VARCHAR(260)); #value 1
    field_b = Column(VARCHAR(260)); #value 2 
    field_c = Column(VARCHAR(260)); #value 3 
    comment = Column(VARCHAR(100)); 
    create_time = Column(DATETIME,server_default=func.now()); 

class Report(Base):
    __tablename__ = "report";
    __table_args__={
        'mysql_charset':'utf8'         
    };
    id = Column(INTEGER,primary_key = True);
    obj_id = Column(BIGINT,nullable=False);
    accuser_id = Column(BIGINT,ForeignKey('user.id'));
    defendant_id  =Column(BIGINT,ForeignKey('user.id'));
    reason  = Column(TEXT);
    create_time = Column(DATETIME,server_default = func.now());
    accuser = relationship('User',foreign_keys=[accuser_id]);
    defendant = relationship('User',foreign_keys=[defendant_id]);
      
class Advice(Base):
    __tablename__ = "advice";
    __table_args__={
        'mysql_charset':'utf8'         
    };
    id = Column(INTEGER,primary_key = True);
    advice = Column(TEXT);
    contact = Column(VARCHAR(30));
    adviser_id = Column(BIGINT);#maybe None
    create_time = Column(DATETIME,server_default=func.now());

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') \
                          and x != 'metadata']:
                data = obj.__getattribute__(field) 
                try:
                    if isinstance(data, datetime):
                        data = data.strftime('%Y-%m-%d %H:%M:%S');
                    json.dumps(data,ensure_ascii=False) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj);

def init_db():
    Base.metadata.create_all(engine);    
def drop_db():
    Base.metadata.drop_all(engine);

#init_db();
#drop_db();        
if __name__ == 'main':
    pass; 
'''
Created on 

@author: ThinkPad
'''
from db import Session; 
from base_model import User ,Topic,Collection,Imagelib;  
from ser_model.base_model import Favorite, FavoriteBox
from collections import Counter ; 

session = Session();
#id = '5'
#session.query(User).filter(User.id==5).update({User.state: 1});     
#session.commit();
#query = session.query(User)
#e=query.filter(User.name=='esli').first();
#print e.name,e.email,e.sex ,     

#print '********************************'
import MySQLdb ;
import sys ;

item = session.query(Favorite.box_id).filter(Favorite.collection_id.in_(106,107)).all();
ids = [];
for e in item:
    ids.append(e.box_id);
d = Counter(ids);

session.query(FavoriteBox).filter(FavoriteBox.id.in_(tuple(ids))).update({
                FavoriteBox.box_count:FavoriteBox.box_count-1},synchronize_session=False); 
session.commit(); 
#fp =open("ic_guide.png",'rb');
#img =fp.read();
#fp.close();
#user = User(name='jeckral',pwd='123',sex='M',acti_code=-1,photo=img,\
#            email='1157553170@qq.com');
#print user.name,user.pwd,user.sex,user.email ; 
#session.add(user);
#session.commit();

#user = session.query(User).get(9)
#print user.name 
#output = open('1.png', 'wb');
#output.write(user.photo);
#output.close();

#topic =Topic(level_code='1000',topic_name='plant',topic_desc='love plant,love health.'
#             ,focus_count='10',create_by='1');
#session.add(topic);

#profession = Profession(profession='lawyer',description='work with law');
#session.add(profession);
#session.commit();

#collection = Collection(type='10',title='this is a title',content='this is content',topic_id=1,create_by=5)
#session.add(collection);
#session.commit();

#print session.query(Collection).filter(Collection.create_by==5).\
#order_by(Collection.last_modify).offset(1).limit(2).all();

#s = (session.query(Collection, Imagelib).filter(Collection.id == Imagelib.collection_id,\
#                                                 Collection.id == 2).all());
#from base_model import AlchemyEncoder ;    
#result = (session.query(Collection, Imagelib).filter(Collection.id == Imagelib.collection_id,\
#                                                 Collection.id == 2).all());        
#print json.dumps(result, cls=AlchemyEncoder)
#p = 'nao'
#condstr = '%'+p+'%'
#s = session.query(User).filter(User.name.like(condstr)).all();
#for i in s:
#    print i.name ;  



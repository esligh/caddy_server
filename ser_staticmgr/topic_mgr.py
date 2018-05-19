'''
Created on 2015

@author: ThinkPad
'''
from ser_model.db import Session; 
from ser_model.base_model import Topic; 
from sqlalchemy.sql.elements import  Null

#read topic pic
def add_topic(name,desc,level,path,pic=None,fcount,owner=-1):   
    imgdata = Null;
    if pic is not None and  pic is '':
        fp =open(pic,'rb');
        imgdata =fp.read();
        fp.close();
    topic =Topic(level_code=level,level_path=path,topic_name=name,topic_desc=desc,\
             topic_pic=imgdata,focus_count=fcount,create_by=owner);             
    try:
        session = Session();
        session.add(topic);
        session.commit();
    except Exception,e:
        print e; 
        session.rollback();
    finally:
        session.close();
        
def del_topic(did):
    try:
        session= Session();
        session.query(Topic).filter(Topic.id==did).delete();
        session.commit();
    except Exception,e:
        print e; 
    finally:
        session.close();
if __name__ == '__main__':
    pass
'''
Created on 

@author: ThinkPad
'''

from ser_model.db import Session; 
from ser_model.base_model import ServerConfig;

def config(ctype,key,name,value1,value2,value3,comment):
    session = Session();
    try:
        c = ServerConfig(cfg_type=ctype,cfg_key=key,cfg_name=name,field_a = value1,\
                         field_b=value2,field= value3,comment=comment);
        session.add(c);
        session.commit();
    except Exception,e:
        print e ; 
    finally:
        session.close();
        
#simple_config 
def config_valuea(ctype,key,name,value1):
    config(ctype,key,name,value1,None,None,None);

#remove_key 
def config_removebykey(key):
    session = Session();
    try:
        session.query(ServerConfig).filter(ServerConfig.cfg_key == key).delete();
    except Exception,e:
        print e ; 
    finally:
        session.close();
        
#remove_type         
def config_removebytype(ctype):
    session = Session();
    try :
        session.query(ServerConfig).filter(ServerConfig.cfg_type == ctype).delete();
    except Exception,e:
        print e ; 
    finally:
        session.close();

if __name__ == '__main__':
    pass
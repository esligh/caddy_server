'''
Created on 

@author: ThinkPad
'''

from ser_model.db import Session; 
from ser_model.base_model import Profession;

name = "";
desc = "";


def add_profession(name,desc):  
    profession = Profession(profession=name,description=desc);
    try:
        session = Session();
        session.add(profession);
        session.commit();
    except Exception,e:
        print e ;
    finally:
        session.close();

def del_profession(pid):
    try:
        session= Session();
        session.query(Profession).filter(Profession.id==pid).delete();
        session.commit();
    except Exception,e:
        print e; 
    finally:
        session.close();



if __name__ == '__main__':
    pass
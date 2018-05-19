'''
Created on 

@author: ThinkPad
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from ser_main.server_config import MYSQL_DATABASE_CONN_URI, db_config

#define engine
engine = create_engine(MYSQL_DATABASE_CONN_URI % (\
                       db_config['user'],
                       db_config['passwd'],
                       db_config['host'],
                       db_config['db'],
                       db_config['charset']),         
                       echo=True); 
Session = sessionmaker(autocommit=False,bind=engine);

#if __name__ == '__main__':
#   print 'can\'t run '
    
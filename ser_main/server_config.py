#coding:utf-8
'''
Created on 2015/4/22

@author: ThinkPad
'''
#server-config.py
db_config={
           'host':'localhost',
           'user':'root',
           'passwd':'jiaquhuaide@6',
           'db':'caddy_v1',
           'charset':'utf8'
};

#server domain ip  ,can config in db . 
SERVER_BASE = r'http://169.254.62.66';
SERVER_BASE_URL = r'http://169.254.62.66:5000';

#db connection url 
MYSQL_DATABASE_CONN_URI='mysql+mysqldb://%s:%s@%s/%s?charset=%s' ;

#nginx image server url  
NGINX_BASE_URL = r'http://169.254.62.66';
NGINX_IMAGE_SERVER_URI=NGINX_BASE_URL+'/images/';
NGINX_IMAGE_SERVER_THUMBNAIL = NGINX_BASE_URL+'/images/thumbnail/'
NGINX_IMAGE_SERVER_COVER = NGINX_BASE_URL+'/images/cover/';

#upload  image directory 
UPLOAD_IAMGE_ROOT_PATH = r'F:/caddy/images/';
UPLOAD_IMAGE_THUMBNAIL_PATH = r'F:/caddy/images/thumbnail/'; 
UPLOAD_IMAGE_COVER_PATH = r'F:/caddy/images/cover/';
UPLOAD_LOG_PATH = r'F:/caddy/log/';
SERVER_LOG_FILE = r'F:/caddy/log/error.log';

#user photo base path 
UPLOAD_USERPHOTO_ROOT_PATH = UPLOAD_IAMGE_ROOT_PATH+r'user_photos/src/';
UPLOAD_USERPHOTO_SMALL_PATH = UPLOAD_IAMGE_ROOT_PATH+r'user_photos/25_25'; #unused 
UPLOAD_USERPHOTO_MEDIUM_PATH = UPLOAD_IAMGE_ROOT_PATH+r'user_photos/40_40';
UPLOAD_USERPHOTO_BIG_PATH = UPLOAD_IAMGE_ROOT_PATH+r'user_photos/100_100';

#nginx user photo url 
NGINX_USERPHOTO_URL_BASE = NGINX_IMAGE_SERVER_URI+r'user_photos/src/';
NGINX_USERPHOTO_MEDIUM_URL_BASE = NGINX_IMAGE_SERVER_URI+r'user_photos/40_40/';
NGINX_USERPHOTO_BIG_URL_BASE = NGINX_IMAGE_SERVER_URI+r'user_photos/100_100/';

#nginx topic photo url  
NGINX_TOPICIMAGE_URL_BASE = SERVER_BASE+r'/images/topic/';

#account active url 
ACCOUNT_ACTIVE_URL =SERVER_BASE_URL+r'/active'; 


if __name__ == '__main__':
    pass
'''
Created on 

simple_upload method just simply response user's image upload request . 
our images mainly save at another image server by proxy using nginx .
At here,we put it together with other methods.when have to separate the 
two server ,considering to move it to image server . 
@author: ThinkPad
'''
import logging ; 
import os ,hashlib; 
from flask import request ;
from flask import json ;
from ser_main import app ; 
from ser_model.db import Session;
from ser_tools.tools_util import make_thumbnail ; 
from ser_model.base_model import Imagelib,User;
from ser_main.server_config import UPLOAD_IAMGE_ROOT_PATH,UPLOAD_USERPHOTO_ROOT_PATH
from ser_main.server_config import UPLOAD_USERPHOTO_MEDIUM_PATH,UPLOAD_USERPHOTO_BIG_PATH
from ser_method.constants import UPLOAD_SUCCESS, UPLOAD_FAILD, OPER_INVALID
from ser_main.server_config import UPLOAD_IMAGE_THUMBNAIL_PATH,UPLOAD_IMAGE_COVER_PATH 

@app.route('/caddy/api/v1.0/simple_upload',methods=['POST'])
def do_upload():     
    infomap = {};      
    cid = request.form['cid'];
    cover_url = request.form['cover_url'];
    howmany = request.form['size'];         
    try: 
        ###thread task 
        for i in range(0,int(howmany)):
            url = request.form['url_'+str(i)];
            map_url = request.form['map_url_'+str(i)];
            slst = map_url.split('/');
            datestr = slst[-2];
            store_folder= UPLOAD_IAMGE_ROOT_PATH+datestr;
            if not os.path.exists(store_folder):
                os.makedirs(store_folder);    
            unique_name = slst[-1];
            f = request.files.get('data_'+str(i));
            data = f.read();
            path = store_folder+'/'+unique_name ; 
            output = open(path ,'wb');
            output.write(data);
            output.close();      
            infomap[url]= datestr+'/'+unique_name;
        ####
        session = Session();
        if cover_url.strip() != '': 
            cover_name = request.form['cover_name'];
            f = request.files.get('cover_data');
            data = f.read();
            path = UPLOAD_IMAGE_COVER_PATH +cover_url;
            output = open(path ,'wb');
            output.write(data);
            output.close();    
            params = [
                      {'size':(200,150),'dst_path':UPLOAD_IMAGE_THUMBNAIL_PATH},
            ]
            make_thumbnail(path,params);
            cover = Imagelib(image_name=cover_name,image_url=cover_url, type = 'COVER',collection_id=cid);
            session.add(cover);
        ids = [] ; 
        for key in infomap.keys():
            url = infomap[key];
            img = Imagelib(image_name=key,image_url=url,collection_id=cid);
            session.add(img);
            ids.append(img.id);
            
        if cover_url == '':               
            session.query(Imagelib).filter(Imagelib.collection_id == cid,
                        Imagelib.image_name == request.form['url_0']) \
                        .update({Imagelib.type:'THUMBNAIL'});            
            entry = session.query(Imagelib).filter(Imagelib.collection_id == cid,
                        Imagelib.image_name == request.form['url_0']).one();
            session.commit();
            #thread task ###          
            src_path = UPLOAD_IAMGE_ROOT_PATH+entry.image_url ; 
            print "gen path:",src_path ; 
            params = [
                      {'size':(200,150),'dst_path':UPLOAD_IMAGE_THUMBNAIL_PATH},
            ]
            make_thumbnail(src_path,params);
            ###            
        else :
            session.commit();
        state =UPLOAD_SUCCESS;
    except Exception,e:
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state =UPLOAD_FAILD;
    
    result ={
              'state':state,
              'dict':infomap
    };
            
    return json.dumps(result);

@app.route('/caddy/api/v1.0/upload_userpic',methods=['POST'])
def do_userpic():
    uid = request.form['uid'];         
    fmt = uid+':'+request.form['email'];
    hstr = hashlib.sha1(fmt).hexdigest();
    path = UPLOAD_USERPHOTO_ROOT_PATH+hstr+'.png';
    if os.path.exists(path):
        os.remove(path);
    url = hstr+'.png';
    state = OPER_INVALID;
    session = Session();
    try:  
        session.query(User).filter(User.id == uid).update({User.photo_url:url}); 
        session.commit();
        f = request.files.get('user_pic');
        data = f.read(); 
        output = open(path ,'wb');
        output.write(data);
        output.close();  
        
        #make user photo thumbnail  
        params = [
          {'size':(100,100),'dst_path':UPLOAD_USERPHOTO_BIG_PATH},
          {'size':(40,40),'dst_path':UPLOAD_USERPHOTO_MEDIUM_PATH}
        ]
        make_thumbnail(path,params);
        state = UPLOAD_SUCCESS ; 
    except Exception , e:
        print e ; 
        logger = logging.getLogger('watch_dog');
        logger.error(e);
        state = UPLOAD_FAILD;         
    finally:
        session.close();
    return json.dumps({'state':state});

if __name__ == '__main__':
    pass;
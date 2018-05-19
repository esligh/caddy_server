'''
Created on 

@author: ThinkPad
'''

from passlib.apps import custom_app_context as pwd_context;
from PIL import Image ; 
import os ; 
import logging ;
from ser_main.server_config import SERVER_LOG_FILE

#another high-performance image library 
#@see detail at http://docs.wand-py.org/en/0.4.1/#why-just-another-binding 
#have installed on local 

def hash_password(password):
        newpwd = pwd_context.encrypt(password)
        return newpwd; 
    
def verify_password(one,two):
        return pwd_context.verify(one,two);
    
def initlog():
        logger = logging.getLogger('watch_dog');
        fhandler =logging.FileHandler(SERVER_LOG_FILE);
        fhandler.setLevel(logging.DEBUG);
        shandler = logging.StreamHandler();
        shandler.setLevel(logging.DEBUG);
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fhandler.setFormatter(formatter)
        shandler.setFormatter(formatter)
        logger.addHandler(fhandler);
        logger.addHandler(shandler);
        
#make thumb 
def make_thumbnail(path, params=[],auto=True):
    '''
        path :image src path 
        params :list of thumb info     
    '''
    if not os.path.exists(path):
        return ;   
    base, ext = os.path.splitext(path)
    name = base.split('/')[-1];
    try:
        im = Image.open(path)
    except IOError,e:
        print e ; 
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            im.load()
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            im = im.convert('RGB')
            im.paste((255,255,255), None, bgmask)
        else:
            im = im.convert('RGB')

    width, height = im.size
    
    for info in params:
        save_path = info['dst_path'];
        if not os.path.exists(save_path):
            os.makedirs(save_path);
        size = info['size'];
        filename = save_path+'/'+name+ext; 
        if os.path.exists(filename):
            os.remove(filename);            
        if float(width) / float(height) == float(str(size[0])) / float(str(size[1])):#same scale
            im.thumbnail(size);
            im.save(filename);
        else:
            if auto :
                scale = float(width)/float(height);
                newheight = float(size[0])/scale;
                size=(size[0],int(newheight));
                im.thumbnail(size);
            else :
                im.thumbnail(size);
            
            im.save(filename);        
    return ;
       
#simple code  
#from ser_main.server_config import UPLOAD_USERPHOTO_MEDIUM_PATH,UPLOAD_USERPHOTO_BIG_PATH
#params = [
#          {'size':(100,100),'dst_path':UPLOAD_USERPHOTO_BIG_PATH},
#          {'size':(40,40),'dst_path':UPLOAD_USERPHOTO_MEDIUM_PATH}
#]
#make_thumbnail(r'F:\caddy\images\user_photos\src\f9c0cabb331beeea8d00b2197b4b06f3b776b360.png',params);

'''
from ser_main.server_config import UPLOAD_IMAGE_THUMBNAIL_PATH
params = [
    {'size':(200,150),'dst_path':UPLOAD_IMAGE_THUMBNAIL_PATH},
]
make_thumbnail(r'F:/caddy/images/2015-08-08/ea59b261-c9f3-4ee5-80af-08f53deb69ed.jpg',params);
'''
      
if __name__ == '__main__':
    pass
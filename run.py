'''
Created on 

@author: ThinkPad
'''

from ser_main import app ,socketio;
from ser_tools.tools_util import initlog 

initlog();
if __name__ == '__main__':
    app.debug = True;   
    socketio.run(app,host='192.168.1.103',port=80);

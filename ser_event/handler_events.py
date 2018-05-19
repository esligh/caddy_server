'''
Created on 
@author:esli
@see:flask-socketio detail 
'''

'''
server 'push' : 
kuibu uses socketio to make a persistent connection with client,it allows 
server side sending message to client actively . 
'''

from ser_main import  clients, socketio ; 
from flask_socketio import emit;
from flask import request ; 

@socketio.on('message')
def handler_message(message):    
    eve_type = message['event_type'];
    #accroding to message type ,handle the message coming from client .
    if eve_type == 'KEEP_ALIVE': #five minutes once .        
        emit('message', {'type':'KEEP_ALIVE'}); # KEEP_ALIVE message response .        

#client login make a connection .  
@socketio.on('login')
def handler_login(json):
    print('received json: ' + str(json));
    client = request.namespace;
    print client ; 
    client_id = json['uid'];
    append_client_dict(client_id,client);
    print clients ; 

@socketio.on('logout')
def handler_logout(json):
    print ' ##user (id='+json['uid']+') is leaving.'
    client_id=json['uid'];
    remove_client_dict(client_id);    
    return ; 

@socketio.on('connect')
def handler_connect():
    print 'client connected.';
    return ; 

@socketio.on('disconnect')
def handler_disconnect(): 
    print 'client disconnected.'
    return ;

#construct a map table of clients , as hash table, store connected socket .
def append_client_dict(client_id,client):
    if not client_id in clients: 
        clients[client_id] = client;
    return ;

def remove_client_dict(client_id):
    return  ; 

if __name__ == '__main__':
    pass
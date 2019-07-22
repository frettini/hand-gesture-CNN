# Socket I/O
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

import logging
import time 


# Socket I/O
#====================================================#
PORT            = 5050
HOST            = '127.0.0.1'
app             = Flask(__name__)
app.debug       = False
socketio        = SocketIO(app, async_mode='threading', logger=False)
socket_thread   = None
FLASK_DEBUG = 0
logging.getLogger('werkzeug').setLevel(logging.ERROR) # remove socket io logs

def sendMsg(namespace,obj):
    socketio.emit(namespace,obj)

@socketio.on('customEvent', namespace="/socket")
def customEvent(msg):
     print ('test')
     print('received : ', msg)
     sendMsg("responsepi", '{"data":"Greetings to you too!"}')


@socketio.on('ComputerMessage')
def customEvent(msg):
     print ('test')
     if msg == "TriggerGoogle":
          sendMsg("responsepi", '{"data":"Greetings to you too!"}')


@app.route('/')
def index():
    print('Someone Connected!')
    sendMsg('response', {'data':'Hello Index'})
    return render_template('index.html')

@socketio.on('connect')
def connect():
    print('Someone Connected!!!')
    socketio.emit("responsepi", '{"data": "Connected"}')

@socketio.on('disconnect')
def disconnect():
    print('byeeeeeeee')
    socketio.emit("responsepi", {"data": "disconnecting"})

socketio.run(app, host=HOST, port=PORT, debug=False, log_output=False)



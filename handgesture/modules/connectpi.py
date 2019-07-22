import socketio



sio = socketio.Client()


def sendMessage(event_name, data, namespaceSIO):
    #callback function 
    sio.emit(event_name, data, namespace=namespaceSIO)
    print("message emitted")

@sio.on('responsepi', namespace='/socket')
def responsepi(msg):
    print('I received a message!', msg['data'])

def connectToPi():
    sio.connect('http://raspberrypi.local:5050/', namespaces=['/socket'])
    print('my sid is', sio.sid)

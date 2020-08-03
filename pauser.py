#!/usr/bin/env python3

import sys
import socketio

got_first_response = False
sio = socketio.Client()

@sio.on('stream_status')
def stream_status_handler(msg):
    global got_first_response
    status = msg['status']['playback']
    print('Playback status: {}'.format(status))
    if not got_first_response:
        got_first_response = True
        if status == 'playing':
            print("Pausing...")
            sio.emit('pausestream', {})
        elif status == 'paused':
            print("Resuming...")
            sio.emit('pausestream', {})
        else:
            print("Doing nothing")
            sio.disconnect()
    else:
        sio.disconnect()

@sio.event
def connect_error():
    print("The connection failed!")
    sys.exit(1)

sio.connect('http://localhost:5000')
sio.wait()

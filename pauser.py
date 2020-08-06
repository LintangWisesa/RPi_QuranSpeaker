#!/usr/bin/env python3

import sys
import socketio

def get_action():
    action = sys.argv[1] if len(sys.argv) >= 2 else 'toggle'
    if not action in ('toggle', 'pause', 'resume'):
        raise ValueError('If specified, action should be either pause or resume')
    return action

action = get_action()
got_first_response = False
sio = socketio.Client()

@sio.on('stream_status')
def stream_status_handler(msg):
    global got_first_response
    status = msg['status']['playback']
    print('Playback status: {}'.format(status))
    if not got_first_response:
        got_first_response = True
        if status == 'playing' and action in ('toggle', 'pause'):
            print("Pausing...")
            sio.emit('pausestream', {})
        elif status == 'paused' and action in ('toggle', 'resume'):
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

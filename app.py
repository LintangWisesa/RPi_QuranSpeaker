#!/usr/bin/env python3

from os.path import dirname, abspath, join as pathjoin
import json

# pip install flask flask-socketio eventlet gevent gevent-websocket
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import vlc

app = Flask(__name__)
# use async_mode='threading' to work outside of an http context (vlc events)
socketio = SocketIO(app, async_mode='threading')
vlc_instance = vlc.Instance()
vlc_player = None
base_url = None
stream_status = {
    'playback': 'stopped',
    'sheikh': None,
    'surah': None
}
root_dir = dirname(abspath(__file__))
status_file = pathjoin(root_dir, '.stream_status.json')

def save_status():
    global status_file, stream_status
    # save to disk
    try:
        with open(status_file, 'wt') as f:
            json.dump(stream_status, f)
    except Exception as e:
        print("Warning: Could not save status, ignoring: {}".format(e))

def load_status():
    global status_file, stream_status
    # load from disk
    try:
        with open(status_file, 'rt') as f:
            stream_status = json.load(f)
        if stream_status['sheikh']:
            set_base_url(stream_status['sheikh'])
            playback = stream_status['playback']
            if playback == 'paused': # starting in paused mode is not implemented yet
                stream_status['playback'] = 'stopped'
            if playback == 'playing':
                generate_and_play_list(stream_status['surah'])
            broadcast_stream_status()
    except Exception as e:
        print("Warning: Could not load status, ignoring: {}".format(e))

def vlc_action_stopped(event):
    global stream_status
    if stream_status['playback'] != 'stopped':
        generate_and_play_list(1)

def vlc_action_media_changed(event):
    global stream_status
    stream_status['surah'] = stream_status['surah'] + 1
    broadcast_stream_status()
    save_status()

def add_media_to_list(url, media_list):
    media = vlc_instance.media_new(url)
    media_list.add_media(media)

def generate_and_play_list(from_surah, to_surah=114):
    global base_url, vlc_player, stream_status
    stream_status['surah'] = from_surah - 1
    vlc_player = vlc_instance.media_player_new()
    vlc_events = vlc_player.event_manager()
    vlc_events.event_attach(vlc.EventType.MediaPlayerStopped, vlc_action_stopped)
    vlc_events.event_attach(vlc.EventType.MediaPlayerMediaChanged, vlc_action_media_changed)
    list_player = vlc_instance.media_list_player_new()
    list_player.set_media_player(vlc_player)
    media_list = vlc_instance.media_list_new()
    list_player.set_media_list(media_list)
    # play taawudz if started from the middle, first surah usually includes it
    if from_surah > 1:
        stream_status['surah'] = stream_status['surah'] - 1
        url = pathjoin(root_dir, 'mp3_adab', 'taawudz.mp3')
        add_media_to_list(url, media_list)
    for surah in range(from_surah, to_surah + 1):
        url = base_url.format(str(surah).zfill(3))
        add_media_to_list(url, media_list)
    list_player.play()

def play_single(file_name):
    file_name = pathjoin(root_dir, 'mp3_adab', file_name)
    vlc.MediaPlayer(file_name).play()

def set_base_url(sheikh):
    global base_url
    mirror, sheikh = sheikh.split('|')
    subdomain = 'download' if mirror == 'quran' else 'mirrors'
    base_url = 'https://{}.quranicaudio.com/{}/{}/{{}}.mp3'.format(subdomain, mirror, sheikh)
    
def broadcast_stream_status():
    # use socketio.emit to work outside of an http context (vlc events)
    socketio.emit('stream_status',  {'status': stream_status}, broadcast=True)

@app.route('/')
def index():
    return render_template('app.html')

@socketio.on('connect')
def client_connected():
    broadcast_stream_status()

@socketio.on('playstream')
def stream_changed(message):
    global stream_status
    print("playstream message received: {}".format(message))
    set_base_url(message['sheikh'])
    stream_status['playback'] = 'playing'
    stream_status['sheikh'] = message['sheikh']
    generate_and_play_list(int(message['surah']))
    # the vlc event media changed will increment surah and broadcast status
    
@socketio.on('stop')
def stop(message):
    global stream_status, vlc_player
    stream_status['playback'] = 'stopped'
    broadcast_stream_status()
    save_status()
    vlc_player.stop()
    play_single('tashdiq.mp3')

@socketio.on('pausestream')
def pause_stream(message):
    global stream_status, vlc_player
    if (vlc_player.get_state() == vlc.State.Paused):
        stream_status['playback'] = 'playing'
    elif (vlc_player.get_state() == vlc.State.Playing):
        stream_status['playback'] = 'paused'

    broadcast_stream_status()
    vlc_player.pause()
    save_status()

if __name__ == '__main__':
    load_status()
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_output=True,
        debug=False,
        use_reloader=False # causes load_status to be called twice!
    )

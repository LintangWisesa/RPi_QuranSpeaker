from os.path import dirname, join as pathjoin

# pip install flask flask-socketio eventlet gevent gevent-websocket
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
import time as delay
from pygame import mixer, time
import vlc

mixer.init()
app = Flask(__name__)
socketio = SocketIO(app)
vlc_instance = vlc.Instance()
vlc_player = None
base_url = None
stream_stopped = True

def vlc_action_stopped(event):
    global stream_stopped
    if not stream_stopped:
        generate_and_play_list(1, 114)

def generate_and_play_list(from_surah, to_surah):
    global base_url, vlc_player
    vlc_player = vlc_instance.media_player_new()
    vlc_events = vlc_player.event_manager()
    vlc_events.event_attach(vlc.EventType.MediaPlayerStopped, vlc_action_stopped)
    list_player = vlc_instance.media_list_player_new()
    list_player.set_media_player(vlc_player)
    media_list = vlc_instance.media_list_new()
    list_player.set_media_list(media_list)
    for aya in range(from_surah, to_surah + 1):
        url = base_url.format(str(aya).zfill(3))
        media = vlc_instance.media_new(url)
        media_list.add_media(media)
    list_player.play()

value = {
    'text': 'Speaker Quran',
    'now': "I'm Ready ..."
}

root_dir = dirname(__file__)

@app.route('/')
def index():
    return render_template('app.html', **value)

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Connected!'})

@socketio.on('playsurah')
def surah_changed(message):
    emit('update surah', message, broadcast=True)
    value['text'] = message['surah']
    print(message)

    nosurat = message['surahval'].zfill(3)
    awalayat = int(message['awal'])
    akhirayat = int(message['akhir'])

    ayats = []
    ayats.append(nosurat + '000')
    for i in range(awalayat, akhirayat + 1):
        ayats.append(nosurat + f"{i:03}")

    # print(ayats)

    for i in ayats:
        file_name = pathjoin(root_dir, 'mp3', '{}.mp3'.format(i))
        mixer.music.load(file_name)
        mixer.music.play()
        while mixer.music.get_busy():
            time.Clock().tick(10)
            # delay.sleep(.5)

@socketio.on('playjuz')
def juz_changed(message):
    value['text'] = message['juz']
    emit('update juz', message, broadcast=True)
    print(message)

    file_name = pathjoin(root_dir, 'mp3', '{}.mp3'.format(message['juzval']))
    mixer.music.load(file_name)
    mixer.music.play()
    # while mixer.music.get_busy(): 
    #     time.Clock().tick(10)

@socketio.on('playstream')
def stream_changed(message):
    global base_url, stream_stopped
    emit('update stream', message, broadcast=True)
    value['text'] = message['surah']
    print("Message received: {}".format(message))

    mirror, sheikh = message['sheikhval'].split('|')
    subdomain = 'download' if mirror == 'quran' else 'mirrors'
    base_url = 'https://{}.quranicaudio.com/{}/{}/{{}}.mp3'.format(subdomain, mirror, sheikh)
    
    nosurat = int(message['surahval'])
    stream_stopped = False
    generate_and_play_list(nosurat, 114)
    
@socketio.on('stop')
def stop(message):
    global stream_stopped, vlc_player
    stream_stopped = True
    # while mixer.music.get_busy():
    mixer.music.stop()
    vlc_player.stop()
    file_name = pathjoin(root_dir, 'mp3_adab', 'tashdiq.mp3')
    mixer.music.load(file_name)
    mixer.music.play()
    while mixer.music.get_busy():
        time.Clock().tick(10)

if __name__ == '__main__':
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_output=True,
        debug=True,
        use_reloader=True
    )

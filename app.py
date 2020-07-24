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
vlc_player = vlc_instance.media_player_new()

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

def play_stream(url):
    media = vlc_instance.media_new(url)
    vlc_player.set_media(media)
    vlc_player.play()

@socketio.on('playstream')
def stream_changed(message):
    emit('update stream', message, broadcast=True)
    value['text'] = message['surah']
    print("Message received: {}".format(message))

    mirror, sheikh = message['sheikhval'].split('|')
    subdomain = 'download' if mirror == 'quran' else 'mirrors'
    base_url = 'https://{}.quranicaudio.com/{}/{}'.format(subdomain, mirror, sheikh)
    
    nosurat = message['surahval'].zfill(3)
    url = "{}/{}.mp3".format(base_url, nosurat) 
    print("Playing {}...".format(url), flush=True)
    play_stream(url)
    
@socketio.on('stop')
def stop(message):
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

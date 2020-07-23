from os.path import dirname, join as pathjoin

# pip install flask flask-socketio eventlet gevent gevent-websocket
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
import time as delay
from pygame import mixer, time

mixer.init()
app = Flask(__name__)
socketio = SocketIO(app)

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

    nosurat = int(message['surahval'])
    awalayat = int(message['awal'])
    akhirayat = int(message['akhir'])

    if nosurat < 10:
        nosurat = '00' + str(nosurat)
    elif nosurat >= 10 and nosurat < 100:
        nosurat = '0' + str(nosurat)
    else:
        nosurat = str(nosurat)

    ayats = []
    ayats.append(nosurat + '000')
    for i in range(awalayat, akhirayat + 1):
        if i < 10:
            i = nosurat + '00' + str(i)
        elif i >= 10 and i < 100:
            i = nosurat + '0' + str(i)
        else:
            i = nosurat + str(i)
        ayats.append(i)

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

@socketio.on('stop')
def stop(message):
    print(message)
    # while mixer.music.get_busy():
    mixer.music.stop()
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

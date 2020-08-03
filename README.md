![simplinnovation](https://4.bp.blogspot.com/-f7YxPyqHAzY/WJ6VnkvE0SI/AAAAAAAADTQ/0tDQPTrVrtMAFT-q-1-3ktUQT5Il9FGdQCLcB/s350/simpLINnovation1a.png)

# Raspberry Pi Quran Speaker

## 📋 Project Summary

Klik gambar berikut untuk melihat video demo:

[![Video](https://img.youtube.com/vi/D82XjlrCjbE/0.jpg)](https://youtu.be/D82XjlrCjbE)

Speaker Al-Qur'an dengan fitur melantunkan ayat suci Al-Qur'an per ayat/per juz serta dapat dikontrol secara wireless via WiFi. Dirancang dengan Raspberry Pi 3B+ & aplikasi Python-based: Flask, Eventlet, Gevent-websocket & Socket.io. File audio yang digunakan merupakan lantunan ayat suci Al-Qur'an oleh Syeikh Abdurrahmaan As-Sudais & Syeikh Mishary Rasyid.

- 📝 Source code & tutorial: 
[klik di sini](https://github.com/LintangWisesa/RPi_QuranSpeaker)

- 🎧 Audio Quran MP3 per ayat (Syeikh Abdurrahmaan As-Sudais):
[klik di sini](https://everyayah.com/data/Abdurrahmaan_As-Sudais_64kbps/)

- 🎧 Audio Quran MP3 per juz (Syeikh Mishary Rasyid):
[klik di sini](https://ia800402.us.archive.org/16/items/MisharyRasyidPerJuz/Mishary/)

<hr>

## 🐳 Docker Tutorial

If you prefer running the project using Docker for an isolated setup
and a rather simpler installation steps, please follow the Docker guide
[here](docker.md).

<hr>

## 📋 Project Tutorial

This project is built on __Raspberry Pi 3B+__ with __Raspbian OS__ and __Python 3.x__ (I'm using 3.4 & 3.8). So make sure you've installed Python 3.x also __git__ to clone this project from my github.

- ### 1. Connect to WiFi & Check its IP

    Connect your Raspberry Pi to a WiFi connection, then check its IP address. On terminal type:

    ```bash
    $ ifconfig
    ```

    Your Pi's IP address must be various, it consists of some numbers with some dots like ```123.456.78.910```. Note your IP address!

<hr>

- ### 2. Clone this project

    Clone this project from my github repo. [Download here](https://github.com/LintangWisesa/RPi_QuranSpeaker) or clone it from your terminal (make sure you've installed *__git__* on your Pi):

    ```bash
    $ git clone <repo_url>
    ```
    
<hr>

- ### 3. Install Python packages

    Install Python packages needed through __*pip*__:

    ```bash
    $ pip3 install flask flask-socketio eventlet gevent gevent-websocket python-vlc
    ```

<hr>

- ### 4. Run Flask application

    Go back to the project root, then run its server application (```app.py``` file).

    ```bash
    $ cd ..

    $ python3 app.py
    ```

    The application (server) will be listening on port ```5000```, so you can access it via your Pi's web browser (for example *__Chromium__*): http://123.456.78.910:5000.

<hr>

- ### 5. Control it from other devices

    You can control it via your laptop, tablet or even a smartphone. First connect your device to a WiFi which your Raspberry Pi is connected to. Open your browser & go to your Pi's IP address on port ```5000```, for example: http://123.456.78.910:5000. You'll see something similar with your Pi display & try to play with it. Enjoy!

<hr>

- ### 6. Control it from other scripts

    You can pause/resume playback from other scripts on the Pi by running the following:
    ```bash
    ./pauser.py
    ```
    This script will only pause if it is currently in playing mode, and will resume
    only if it is in paused mode. If it is in stopped mode, it will do nothing.

    This is beneficial if you want to pause/resume playback beofre/after playing
    [Adhan](https://github.com/achaudhry/adhan) for example.

<hr>

#### Lintang Wisesa :love_letter: _lintangwisesa@ymail.com_

[Facebook](https://www.facebook.com/lintangbagus) | 
[Twitter](https://twitter.com/Lintang_Wisesa) |
[Youtube](https://www.youtube.com/user/lintangbagus) |
[LinkedIn](https://www.linkedin.com/in/lintangwisesa/) | 
:octocat: [GitHub](https://github.com/LintangWisesa) |
[Hackster](https://www.hackster.io/lintangwisesa)

#### Hossam Hammady
[Twitter](https://twitter.com/hammady) |
[GitHub](https://github.com/hammady)


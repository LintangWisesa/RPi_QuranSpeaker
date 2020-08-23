![simplinnovation](https://4.bp.blogspot.com/-f7YxPyqHAzY/WJ6VnkvE0SI/AAAAAAAADTQ/0tDQPTrVrtMAFT-q-1-3ktUQT5Il9FGdQCLcB/s350/simpLINnovation1a.png)

# Raspberry Pi Quran Speaker

## 📋 Project Summary

Click the following picture to see the demo video:

[![Video](https://img.youtube.com/vi/D82XjlrCjbE/0.jpg)](https://youtu.be/D82XjlrCjbE)

Qur'anic speaker for the online streaming of the Holy Qur'an. It can be controlled wirelessly via WiFi. Designed with Raspberry Pi 3B+/4B & Python: Flask, Eventlet, Gevent-websocket & Socket.io.

- 📝 Source code & tutorial: 
[Click here](https://github.com/LintangWisesa/RPi_QuranSpeaker)

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

    Go to the project root, then run its server application (```app.py``` file).

    ```bash
    $ cd RPi_QuranSpekaer
    $ ./app.py
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
    This script toggles the playing/paused mode. It will pause if it is
    currently in playing mode, and will resume if it is in paused mode.
    If it is in stopped mode, it will do nothing.

    You can also be specific if you only want to either pause or resume:
    ```bash
    ./pauser.py pause # pauses only, skips if paused or stopped
    ./pauser.py resume # resumes only, skips if playing or stopped
    ./pauser.py toggle # toggles, skips if stopped, the default behavior
    ```

    This is beneficial if you want to pause/resume playback beofre/after playing
    [Adhan](https://github.com/achaudhry/adhan) for example.

    Another scenario is to pause playback every night and resume in the morning.
    To do this add 2 cronjobs (type `crontab -e` and insert the below):

    ```
    0 22 * * * /home/pi/RPi_QuranSpeaker/pauser.py pause
    0 6 * * * /home/pi/RPi_QuranSpeaker/pauser.py resume
    ```

<hr>

- ### 7. Auto-start Quran Speaker on system boot

    We are going to use [supervisord](http://supervisord.org/) for auto-starting
    Quran Speaker on system boot and to ensure it is automatically restarted if
    it was stopped for any reason.

    1. Install supervisord:
        ```bash
        sudo apt install -y supervisor
        ``` 
    2. Place the following inside `/etc/supervisor/conf.d`:
        ```ini
        # /etc/supervisor/conf.d/quran_speaker.conf
        [program:quran_speaker]
        command=/home/pi/RPi_QuranSpeaker/app.py
        user=pi
        ```
    3. Reload supervisord:
        ```bash
        sudo systemctl reload
        ```
    4. Monitor the status of the service and check logs if necessary:
        ```bash
        sudo supervisorctl status quran_speaker
        sudo tail -f /var/log/supervisor/quran_speaker-stderr*
        ```

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


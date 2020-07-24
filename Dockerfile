FROM python:3.8.5
LABEL maintainer="Hossam Hammady <github@hammady.net>"

WORKDIR /home

# install pygame system dependencies
RUN  apt-get update && \
     apt-get install -y \
       python3-dev \
       libsdl-image1.2-dev \
       libsdl-mixer1.2-dev \
       libsdl-ttf2.0-dev \
       libsdl1.2-dev \
       libsmpeg-dev \
       python3-numpy \
       subversion \
       libportmidi-dev \
       libfreetype6-dev \
       vlc && \
     rm -rf /var/lib/apt/lists/*

# upgrade pip itself
RUN pip3 install --upgrade pip
# copy requirements to cache the dependencies
COPY requirements.txt /home
RUN pip3 install -r requirements.txt

# copy rest of source code to the container
COPY / /home

EXPOSE 5000

CMD ["python3", "-u", "app.py"]


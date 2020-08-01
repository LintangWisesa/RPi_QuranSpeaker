FROM python:3.8.5
LABEL maintainer="Hossam Hammady <github@hammady.net>"

WORKDIR /home

# install vlc system dependencies
RUN  apt-get update && \
     apt-get install -y vlc && \
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

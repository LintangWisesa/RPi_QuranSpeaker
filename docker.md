## 🐳 Docker Tutorial

### 1. System requirements

Install Docker and Docker Compose using [this](https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl) guide.

### 2. Download mp3 files

Follow the same instructions in the original tutorial.

### 3. Build and run

Build for the first time only:

```bash
docker-compose build
```

Run:

```bash
docker-compose up
```

Then visit the page: `http://RPI_IP:5000/` where `RPI_IP` is your Raspberry Pi IP.


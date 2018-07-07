FROM python:3.6

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
      libopus-dev \
      libsodium-dev \
      wget \
      xz-utils
RUN wget http://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz \
      && tar Jxvf ./ffmpeg-release-64bit-static.tar.xz \
      && cp ./ffmpeg*64bit-static/ffmpeg /usr/local/bin/
RUN pip install -r requirements.txt
CMD ["python", "main.py"]

FROM ubuntu:focal

# Install essential software packages

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y wget 
RUN apt-get install -y curl
RUN apt-get install vim nano -y

# Install python

RUN apt-get install python3.7 -y
RUN apt-get install python3-pip -y

# Install dependencies for opencv and face-recognition

RUN apt-get update 
RUN apt install -y libprotobuf-dev protobuf-compiler
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install cmake 
RUN apt-get install -y libopenblas-dev 
RUN apt-get install -y liblapack-dev 
RUN apt-get install -y libjpeg-dev
RUN apt-get install ffmpeg -y
RUN apt-get install -y --fix-missing
RUN apt-get install -y build-essential
RUN apt-get install -y gfortran
RUN apt-get install -y graphicsmagick
RUN apt-get install -y libgraphicsmagick1-dev
RUN apt-get install -y libatlas-base-dev
RUN apt-get install -y libavcodec-dev
RUN apt-get install -y libavformat-dev
RUN apt-get update
RUN apt-get install -y --fix-missing
RUN apt-get autoremove -y
RUN apt-get clean 
RUN apt-get install -y libglib2.0-dev
RUN apt-get install -y libgtk2.0-dev
RUN apt-get install -y libswscale-dev
RUN apt-get install -y pkg-config
RUN apt-get install -y software-properties-common
RUN apt-get install -y zip

# Downloading and building dlib

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

# Install pip packages

RUN pip3 install --upgrade pip
RUN pip3 install flask
RUN pip3 install flask-restful
RUN pip3 install requests
RUN pip3 install Pillow
RUN pip3 install scipy>=0.17.0
RUN pip3 install Click>=6.0
RUN pip3 install flask-sqlalchemy
RUN pip3 install face_recognition
RUN pip3 install numpy
RUN pip3 install opencv-python

# remove unwanted packages

RUN apt-get install -y --fix-missing
RUN apt-get autoremove -y
RUN apt-get clean

# Change the directory to the project root

WORKDIR /home/face_recognition
# ADD FlaskApp FlaskApp/
# WORKDIR /home/face_recognition/FlaskApp
RUN git clone https://github.com/manand881/RPi-Face-Recognition.git
RUN git pull
WORKDIR /home/face_recognition/RPi-Face-Recognition/"Edge Unit"/FlaskApp

# run project

EXPOSE 5055
CMD ["python3", "app.py"]
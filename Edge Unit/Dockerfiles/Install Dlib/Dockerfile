FROM ubuntu:focal

# Install software packages

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y wget 
RUN apt-get install -y curl
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get update 
RUN apt install -y libprotobuf-dev protobuf-compiler
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install cmake 
RUN apt-get install -y libopenblas-dev 
RUN apt-get install -y liblapack-dev 
RUN apt-get install -y libjpeg-dev
RUN apt-get install vim nano -y

# Install pip packages

RUN pip3 install --upgrade pip
RUN pip3 install flask
RUN pip3 install flask-restful
RUN pip3 install requests
RUN pip3 install flask-sqlalchemy
RUN pip3 install face_recognition
RUN pip3 install numpy
RUN pip3 install opencv-python

# Handing opencv dependencies

RUN apt-get update
RUN apt-get install ffmpeg -y

# remove unwanted packages

RUN apt-get autoremove -y

# Change the directory to the project root

WORKDIR /home/face_recognition
ADD FlaskApp FlaskApp/
WORKDIR /home/face_recognition/FlaskApp

# run project

EXPOSE 5055
CMD ["python3", "app.py"]
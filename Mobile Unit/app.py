import os
import sys
import cv2
import time
import cv2
from multiprocessing import Process, Queue
from module import *


israspberrypi = False

# Checking if the device is a raspberry pi from module.py

if('RaspberryPi' in detect_device() and applyconfig('Use USB Cam') == False):
    israspberrypi = True
    print("[INFO]    Detected Raspberry Pi as device with instruction to use Pi Camera")
if(israspberrypi):
    from picamera.array import PiRGBArray
    from picamera import PiCamera


vid = None
width = None
height = None
fps = None
frame_queue = Queue()
post_queue = Queue()
grabframepid = None
showframepid = None
frame_queue_size_pid = None
edgeunit_ip = None
postframepid = None


if(israspberrypi == False):
    vid = cv2.VideoCapture(0)
    width = vid.get(3)
    height = vid.get(4)
    fps = vid.get(5)
    grabframepid = 0
    showframepid = 0
    frame_queue_size_pid = 0


def grabframefromusb(frame_queue, post_queue):
    print("[INFO]    Started frame grab process from the usb camera")
    face_cascade = cv2.CascadeClassifier(os.path.join(
        sys.path[0], 'haarcascade_frontalface_default.xml'))
    while True:
        # now = time.time()
        ret, frame = vid.read()
        if(ret):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, 1.1, 4, minSize=(70, 70))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                post_queue.put(cropimage(frame, x, y, w, h))
            frame_queue.put(frame)
        # print("[INFO]    FPS:".ljust(37), 1/(time.time()-now))


def grabframefrompicamera(frame_queue, post_queue):
    print("[INFO]    Started frame grab process from the picamera")

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)
    face_cascade = cv2.CascadeClassifier(os.path.join(
        sys.path[0], 'haarcascade_frontalface_default.xml'))
    run_haarcascade_this_frame = True
    faces = []
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # now = time.time()
        image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if(run_haarcascade_this_frame):
            faces = face_cascade.detectMultiScale(
                gray, 1.1, 4, minSize=(70, 70))
            run_haarcascade_this_frame = not run_haarcascade_this_frame
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            post_queue.put(cropimage(frame, x, y, w, h))
        frame_queue.put(image)
        rawCapture.truncate(0)
        # print("[INFO]    FPS:".ljust(37), 1/(time.time()-now))


def showframe(frame_queue, grabframepid, frame_queue_size_pid, postframepid):
    print("[INFO]    Started frame show process")
    while True:
        frame = frame_queue.get()
        cv2.imshow('Frame Queue', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            try:
                os.kill(grabframepid, 9)
                os.kill(frame_queue_size_pid, 9)
                os.kill(postframepid, 9)
            except:
                pass
            print("[INFO]    Program ended due to user input")
            return


def frame_queue_size(frame_queue):
    print("[INFO]    Started frame queue size process")
    while True:
        frames_in_queue = frame_queue.qsize()
        print("[INFO]    Frames in Queue:".ljust(
            37), frames_in_queue, end="\r")
        time.sleep(1)


def postframe(post_queue, edgeunit_ip):
    print("[INFO]    Started frame post process")
    while True:
        frame = post_queue.get()
        if(frame is not None):
            post_frame_to_edgeunit(encode_image(frame), edgeunit_ip)


if __name__ == "__main__":
    print("[INFO]    Starting Program")

    # Checking for edge unit ip to post

    print("[INFO]    Checking for Edge Unit")
    writeedgeunitip(findedgeunitip())
    edgeunit_ip = readedgeunitip()

    # Starting processes according to config file

    grab_process = None
    if(israspberrypi):
        print("[INFO]    Starting frame grab process from the picamera")

        grab_process = Process(
            target=grabframefrompicamera, args=(frame_queue, post_queue,))
    else:
        print("[INFO]    Starting frame grab process from the usb camera")

        grab_process = Process(target=grabframefromusb,
                               args=(frame_queue, post_queue,))

        print("[INFO]    Camera height is: " + str(height))
        print("[INFO]    Camera width is: " + str(width))
        print("[INFO]    Camera FPS is: " + str(fps))
    frame_queue_process = Process(target=frame_queue_size, args=(frame_queue,))
    post_frame_process = Process(
        target=postframe, args=(post_queue, edgeunit_ip,))
    # starting processes
    grab_process.start()
    frame_queue_process.start()
    post_frame_process.start()
    show_process = Process(target=showframe, args=(
        frame_queue, grab_process.pid, frame_queue_process.pid, post_frame_process.pid))
    show_process.start()
    # waiting to join all processes
    grab_process.join()
    show_process.join()
    frame_queue_process.join()
    post_frame_process.join()

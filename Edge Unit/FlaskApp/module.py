import os
import sys
import time
from multiprocessing import Process, Queue
from os import listdir
from os.path import isfile, join
from time import gmtime, strftime

import cv2
import face_recognition
import numpy as np

API_Call_queue = Queue()
Recognized_faces_queue = Queue()

# This module needs lots of work


def change_working_directory_to_file_directory():
    filedirectory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(filedirectory)


def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True


def check_user():
    iterator = 0
    while(True):
        temp = "user_"+str(iterator)
        if(create_directory_if_not_exists(temp)):
            return temp
        iterator += 1


def capture_image():
    checkedforuser = False
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Capture Image")
    img_counter = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Capture Image", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            if(checkedforuser == False):
                os.chdir("Faces")
                checkedforuser = True
            img_name = "frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
            return

    cam.release()
    cv2.destroyAllWindows()


def knownimagesandencoginds(known_face_encodings, known_face_names):

    mypath = sys.path[0]+"/Faces"
    print(mypath)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for files in onlyfiles:
        try:
            image_path = os.path.join(mypath, files)
            image_data = face_recognition.load_image_file(image_path)
            image_face_encoding = face_recognition.face_encodings(image_data)[0]
            known_face_encodings.append(image_face_encoding)
            known_face_names.append(files.split('.')[0])
        except:
            pass
    return known_face_encodings, known_face_names


def bytes_to_image(bytes):

    img = cv2.imdecode(np.frombuffer(bytes, np.uint8), 1)
    cv2.imwrite('API Image Recieved On'+str(time.time())+'.png', img)


def bytes_to_cv2image(bytes):

    img = cv2.imdecode(np.frombuffer(bytes, np.uint8), 1)
    # cv2.imshow('API Image Recieved On'+str(time.time()), img)
    return img


def face_recognition_from_queue(API_Call_queue, Recognized_faces_queue):
    # video_capture = cv2.VideoCapture(0)
    known_face_encodings = []
    known_face_names = []
    known_face_encodings, known_face_names = knownimagesandencoginds(
        known_face_encodings, known_face_names)

    # print("[INFO]    Starting face recognition...\n")
    # print("[INFO]    Persons for whom recognition data exists\n")
    # print(*known_face_names, sep='\n')

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
        if(API_Call_queue.qsize() > 0):
            # Grab a single frame of video
            frame = API_Call_queue.get()
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(
                    rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    tempjson = {"name": name, "time": strftime(
                        "%H:%M:%S", gmtime()), "Department": "Accounts", "Gate": 1, "date": strftime("%d-%m-%Y", gmtime())}
                    face_names.append(name)
                    Recognized_faces_queue.put(tempjson)
                    print("Detected Face : {}. There are {} frames in the queue".format(
                        name, API_Call_queue.qsize()))
            process_this_frame = not process_this_frame
        else:
            print("[INFO]    No frames in the queue. Sleeping for 1 second {}".format(
                strftime("%Y-%m-%d %H:%M:%S", gmtime())), end="\r")
            time.sleep(1)
        # cv2.destroyAllWindows()


def start_face_recognition_process():
    print("[INFO]    Starting face recognition process...")
    face_recognition_process = Process(
        target=face_recognition_from_queue, args=(API_Call_queue, Recognized_faces_queue))
    face_recognition_process.start()
    return face_recognition_process, face_recognition_process.pid


def put_in_queue(bytes):
    API_Call_queue.put(bytes_to_cv2image(bytes))


def get_from_queue():
    if(Recognized_faces_queue.qsize() > 0):
        return Recognized_faces_queue.get()
    else:
        return {"name": "Empty"}


def save_new_face(file):
    mypath = sys.path[0]+"/Faces"
    os.chdir(mypath)
    file.save(file.filename)
    os.chdir("..")

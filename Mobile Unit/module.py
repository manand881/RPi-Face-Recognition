import io
import json
import os
import platform
import sys
import requests
import cv2


def encode_image(image):
    ret, jpeg = cv2.imencode('.jpg', image)
    return jpeg.tobytes()


def draw_rectangle(image, x, y, w, h):
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return image


def cropimage(image, x, y, w, h):
    return image[y:y+h, x:x+w]


def applyconfig(CheckConfig):
    filepath = os.path.join(sys.path[0], 'config.json')
    with open(filepath, 'r') as f:
        config = json.load(f)
        if(CheckConfig == 'Use USB Cam'):
            return config["Use USB Cam"]


def detect_device():
    DeviceType = None
    if (platform.system() == 'Windows'):
        DeviceType = 'Windows'+' '+platform.release()
    else:
        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower():
                    DeviceType = 'RaspberryPi'
                    print("[INFO]    Detected Raspberry Pi as device")
        except Exception as e:
            print(
                "[+] Error occured while checking if the device is a raspberry pi: {}".format(e))

    return DeviceType


def ping(ip):
    try:
        print("[INFO] Trying to connect to {}".format(ip), end="\r")
        response = requests.get('http://'+ip+':5055/hello')
        if("Edge Unit" in response.text):
            print("\n[INFO]    Edge Unit found at {}".format(ip))
            return ip
    except:
        pass


def findedgeunitip():
    filepath = os.path.join(sys.path[0], 'config.json')
    with open(filepath, 'r') as f:
        config = json.load(f)
        if(config["Edge Unit IP"] == ''):
            print("[INFO]    No Edge Unit IP found in config.json")
            prefix = '192.168'
            for i in range(0, 255):
                for j in range(190, 255):
                    ip = prefix+'.'+str(i)+'.'+str(j)
                    if(ping(ip)):
                        return ip
        else:
            print("[INFO]    Edge Unit IP found in config.json")
            return config["Edge Unit IP"]


def writeedgeunitip(ip):
    filepath = os.path.join(sys.path[0], 'config.json')
    with open(filepath, 'r') as f:
        config = json.load(f)
    config["Edge Unit IP"] = ip
    print("[INFO]    Writing Edge Unit IP to config.json")
    with open(filepath, 'w') as f:
        json.dump(config, f)


def readedgeunitip():
    filepath = os.path.join(sys.path[0], 'config.json')
    with open(filepath, 'r') as f:
        config = json.load(f)
    return config["Edge Unit IP"]


def post_frame_to_edgeunit(frame, ip):
    url = 'http://'+ip+':5055/recognize'
    headers = {'Content-Type': 'application/octet-stream'}
    # print(type(frame),"framelen")
    # files = {'file': ('frame.jpg', frame)}
    # response = requests.post(url, data=files, headers=headers)
    # print(response.text)
    res = requests.post(url, data=frame, headers=headers)

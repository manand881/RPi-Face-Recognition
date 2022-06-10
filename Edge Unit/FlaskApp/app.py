# flask app to recieve api call
from email import message
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
# import face_recognition
from module import *

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'the random string'
# app.config["DEBUG"] = True
db = SQLAlchemy(app)
face_recognition_process = None
face_recognition_process_id = None


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route("/enroll")
def enroll():
    return render_template('enroll.html', message="")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/enroll_face", methods=['POST'])
def enroll_face():
    if request.method == 'POST':
        f = request.files['file']
        if(".png" not in f.filename):
            return render_template('enroll.html', message="Please Upload PNG File Only")
        else:
            # f.save(f.filename)
            save_new_face(f)
        return render_template('enroll.html', message="Successfully enrolled")


@app.route('/hello', methods=['GET'])
def home():
    return {'Device Type': 'Edge Unit',
            'Device ID': '123456789', }


@app.route('/recognize', methods=['POST'])
def recognize():
    # recieve bytedata
    # bytes_to_image(request.data)
    # bytes_to_cv2image(request.data)
    put_in_queue(request.data)
    return {'Recieved': 'OK'}


@app.route('/recognized', methods=['GET'])
def recognized():
    return jsonify(get_from_queue())


if __name__ == "__main__":
    print("[INFO]    Starting Flask Server...")
    print("[INFO]    Starting Face Recognition...")
    face_recognition_process, face_recognition_process_id = start_face_recognition_process()
    app.run(host='0.0.0.0', debug=True, port=5055)

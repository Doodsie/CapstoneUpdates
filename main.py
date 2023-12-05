import json
from flask import Flask, render_template, request, session, redirect, url_for, Response, jsonify, flash,  send_from_directory
from flask_socketio import SocketIO, emit
import mysql.connector
import cv2
from PIL import Image
import numpy as np
import os
import time
from datetime import date, datetime
import re
from werkzeug.utils import secure_filename
import io
import base64
from engineio.payload import Payload
from threading import Thread


app = Flask(__name__)
app.secret_key = 'pisatindipay'
cnt = 0
pause_cnt = 0
justscanned = False
img_id = 0
max_imgid = 1
socketio = SocketIO(app,cors_allowed_origins='*' )
Payload.max_decode_packets = 50

resized_image = cv2.resize(image, (width, height))
#socketio = SocketIO(async_mode='gevent', ping_timeout=cfg.service.PING_TIMEOUT, ping_interval=cfg.service.PING_INTERVAL)


config = {
    "host": "roundhouse.proxy.rlwy.net",
    "user": "root",
    "password": "f4C3ed4bcfAEfachEbC1dfDhBeFdfgA1",
    "database": "zagusopass",
    "port": "20449"
}
'''
config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "zagusopass"
}
'''
cnx = mysql.connector.connect(**config)
mycursor = cnx.cursor(buffered=True)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Generate dataset >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''
def generate_dataset(nbr):
    face_classifier = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")

    mycursor.execute("select * from img_dataset WHERE img_person='" + str(nbr) + "'")
    data1 = mycursor.fetchall()
    for item in data1:
        imagePath = "dataset/" + nbr + "." + str(item[0]) + ".jpg"
        # print(imagePath)
        try:
            os.remove(imagePath)
        except:
            pass
    mycursor.execute("delete from img_dataset WHERE img_person='" + str(nbr) + "'")
    cnx.commit()

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        # scaling factor=1.3
        # Minimum neighbor = 5

        if len(faces) == 0:
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        return cropped_face

    cap = cv2.VideoCapture(0)

    mycursor.execute("select ifnull(max(img_id), 0) from img_dataset")
    row = mycursor.fetchone()
    lastid = row[0]

    img_id = lastid
    max_imgid = img_id + 100
    count_img = 0

    while True:
        ret, img = cap.read()
        if face_cropped(img) is None:
            frame1 = cv2.resize(img, (200, 200))
            frame1 = cv2.imencode('.jpg', frame1)[1].tobytes()
            yield (b'--frame1\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')
        if face_cropped(img) is not None:
            count_img += 1
            img_id += 1
            face = cv2.resize(face_cropped(img), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            file_name_path = "dataset/" + nbr + "." + str(img_id) + ".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(count_img) + '%', (5, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

            mycursor.execute("""INSERT INTO `img_dataset` (`img_id`, `img_person`) VALUES
                                ('{}', '{}')""".format(img_id, nbr))
            cnx.commit()
            if int(img_id) == int(max_imgid):
                if int(img_id) == int(max_imgid):
                    cv2.putText(face, "Training Complete", (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(face, "Click Train Face.", (5, 45), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            frame = cv2.imencode('.jpg', face)[1].tobytes()
            yield (b'--frame1\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            if cv2.waitKey(1) == 13 or int(img_id) == int(max_imgid):
                break
                cap.release()
                cv2.destroyAllWindows()
'''
def global_decl():
    global img_id,count_img,max_imgid
    img_id = 0
    max_imgid = 1

global_decl()

####global img_id,count_img,max_imgid
count_img = 0
img_id = 0

def generate_dataset_socket(image):
    face_classifier = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
    '''
    mycursor.execute("select * from img_dataset WHERE img_person='" + str(nbr) + "'")
    data1 = mycursor.fetchall()
    for item in data1:
        imagePath = "dataset/" + str(nbr) + "." + str(item[0]) + ".jpg"
        # print(imagePath)
        try:
            os.remove(imagePath)
        except:
            pass
    mycursor.execute("delete from img_dataset WHERE img_person='" + str(nbr) + "'")
    cnx.commit()
    '''
    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        # scaling factor=1.3
        # Minimum neighbor = 5

        if len(faces) == 0:
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        return cropped_face


    '''
    mycursor.execute("select ifnull(max(img_id), 0) from img_dataset")
    row = mycursor.fetchone()
    lastid = row[0]
    '''
    global img_id, count_img, max_imgid
    #img_id = lastid
    #max_imgid = img_id + 100
    #count_img = 0

    
    img = image
    #if int(img_id) <= int(max_imgid) and face_cropped(img) is None:
            #frame = cv2.resize(img, (200, 200))
            #frame1 = cv2.imencode('.jpg', frame1)[1].tobytes()
            #yield (b'--frame1\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')
            #return frame1
    #img_id=0
    #max_imgid=1
    if int(img_id) < int(max_imgid) and face_cropped(img) is not None:
            #global img_id, count_img, max_imgid
            count_img += 1
            img_id += 1
            print("imgid:"+str(img_id))
            face = cv2.resize(face_cropped(img), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            file_name_path = "dataset/" + str(nbr) + "." + str(img_id) + ".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(count_img) + '%', (5, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

            mycursor.execute("""INSERT INTO `img_dataset` (`img_id`, `img_person`) VALUES
                                ('{}', '{}')""".format(img_id, nbr))
            cnx.commit()
            if int(img_id) == int(max_imgid):
                if int(img_id) == int(max_imgid):
                    cv2.putText(face, "Training Complete", (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(face, "Click Train Face.", (5, 45), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            #frame = cv2.imencode('.jpg', face)[1].tobytes()
            #yield (b'--frame1\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            frame = face
            #if int(img_id) == int(max_imgid):
                #break
    if int(img_id) <= int(max_imgid) and face_cropped(img) is None:
        frame = cv2.resize(img, (200, 200))
        if int(img_id) == int(max_imgid):
            cv2.putText(frame, "Training Complete", (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, "Click Train Face.", (5, 45), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    return frame


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Train Classifier >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/train_classifier/<nbr>')
def train_classifier(nbr):
    user_id = session.get('user_id')  # Get the user's ID from the session
    # dataset_dir = "C:/Users/jd/PycharmProjects/FlaskOpencv_FaceRecognition/dataset"
    if not has_completed_training(user_id):
        img_count = get_image_count(user_id)  # Get the image count for the user

        if img_count == 100:

            dataset_dir = "dataset"

            path = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)]
            faces = []
            ids = []

            for image in path:
                img = Image.open(image).convert('L');
                imageNp = np.array(img, 'uint8')
                id = int(os.path.split(image)[1].split(".")[1])

                faces.append(imageNp)
                ids.append(id)
            ids = np.array(ids)

            # Train the classifier and save
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)
            clf.write("classifier.xml")

            mycursor.execute("UPDATE users SET completed_training = 1 WHERE id = %s", (user_id,))
            cnx.commit()

            flash('TRAIN SUCCESSFUL.', 'success')
        else:
            flash('SORRY, TRAIN MUST BE 100%', 'danger')

    else:
        flash('YOU CAN ONLY TRAIN ONCE.', 'danger')

    return redirect('/vfdataset_page')


def get_image_count(user_id):
    # Assuming you have a database table named img_dataset with user_id field
    mycursor.execute("SELECT COUNT(*) FROM img_dataset WHERE img_person = %s", (user_id,))
    row = mycursor.fetchone()
    count = row[0] if row else 0
    return count


@app.route('/gendataset')
def gendataset():
    user_id = session['user_id']
    user_completed_process = has_completed_training(user_id)
    return render_template('gendataset.html', user_completed_process=user_completed_process)


def has_completed_training(user_id):
    # Implement your logic to check if the user has completed training
    # For example, you can check the value of the 'completed_training' field in the database
    mycursor.execute("SELECT completed_training FROM users WHERE id = %s", (user_id,))
    result = mycursor.fetchone()

    if result and result[0] == 1:
        return True
    else:
        return False


def face_show():
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        global justscanned
        global pause_cnt

        pause_cnt += 1

        coords = []

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            if confidence > 70 and not justscanned:
                global cnt
                cnt += 1

                n = (100 / 30) * cnt
                # w_filled = (n / 100) * w
                w_filled = (cnt / 30) * w

                # cv2.rectangle(img, (x, y + h + 40), (x + w, y + h + 50), color, 2)
                # cv2.rectangle(img, (x, y + h + 40), (x + int(w_filled), y + h + 50), (153, 255, 255), cv2.FILLED)

            else:
                if not justscanned:
                    cv2.putText(img, 'UNKNOWN', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img, ' ', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

                if pause_cnt > 80:
                    justscanned = False

            coords = [x, y, w, h]
        return coords

    def recognize(img, clf, faceCascade):
        coords = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 0), "Face", clf)
        return img

    faceCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    wCam, hCam = 400, 400

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while True:
        ret, img = cap.read()
        img = recognize(img, clf, faceCascade)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Face Recognition >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Global variables for liveness detection
# Global variables for liveness detection
last_face_detection_time = time.time()
face_detected = False

'''
def face_recognition(group_id, attendancetime, attendanceduration, random_attendance_id, user_id):
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        global justscanned
        global pause_cnt
        global last_face_detection_time
        global face_detected

        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        pause_cnt += 1

        for (x, y, w, h) in features:
            # Check liveness using HOG descriptor
            liveness = detect_liveness(img, x, y, w, h)
            if liveness:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                id, pred = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int(100 * (1 - pred / 300))

                if confidence > 80 and not justscanned:
                    cnt_increment()

                    if int(cnt) == 30:
                        cnt_reset()
                        atime = str(date.today()) + ' ' + str(attendancetime) + ':00'

                        mycursor.execute("select a.img_person, b.first_name, b.last_name "
                                         "  from img_dataset a "
                                         "  left join users b on a.img_person = b.id "
                                         " where a.img_id = " + str(id))
                        row = mycursor.fetchone()
                        if row:
                            pnbr = row[0]
                            pname = row[1]

                            mycursor.execute("select count(*) "
                                             "  from accs_hist "
                                             " where accs_date = curdate() AND group_id = '" + str(
                                group_id) + "' AND accs_prsn = '" + pnbr + "' AND random_attendance_id = '" + str(
                                random_attendance_id) + "'")
                            row = mycursor.fetchone()
                            rowcount = row[0]

                            if rowcount > 0:
                                cv2.putText(img, pname + ', Present', (x - 10, y - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
                                justscanned = True
                                pause_cnt = 0
                            else:
                                cv2.putText(img, pname, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                            (153, 255, 255), 2,
                                            cv2.LINE_AA)

                                mycursor.execute(
                                    "insert into accs_hist (accs_date, accs_prsn, group_id, accs_added, random_attendance_id) values('" + str(
                                        date.today()) + "', '" + pnbr + "', '" + str(group_id) + "', '" + str(
                                        atime) + "', '" + str(
                                        random_attendance_id) + "')")
                                cnx.commit()

                                time.sleep(1)

                                justscanned = True
                                pause_cnt = 0
                        else:
                            cv2.putText(img, 'UNKNOWN', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2,
                                        cv2.LINE_AA)
                    else:
                        justscanned = False
                else:
                    if not justscanned:
                        cv2.putText(img, 'Spoofing', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2,
                                    cv2.LINE_AA)
                    else:
                        cv2.putText(img, 'Present', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (0, 0, 255), 2, cv2.LINE_AA)

                    if pause_cnt > 80:
                        justscanned = False

            else:
                if not justscanned:
                    cv2.putText(img, 'Spoofing', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img, 'Present', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (0, 0, 255), 2, cv2.LINE_AA)

                if pause_cnt > 80:
                    justscanned = False

    def recognize(img, clf, faceCascade):
        draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 0), "Face", clf)
        return img

    def detect_liveness(img, x, y, w, h):
        global last_face_detection_time
        global face_detected

        roi = img[y:y + h, x:x + w]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Define a region of interest for the face
        roi_hsv = hsv[int(0.1 * h):int(0.9 * h), int(0.1 * w):int(0.9 * w)]
        roi_gray = gray[int(0.1 * h):int(0.9 * h), int(0.1 * w):int(0.9 * w)]

        # Calculate gradients
        gx = cv2.Sobel(roi_gray, cv2.CV_64F, 1, 0, ksize=5)
        gy = cv2.Sobel(roi_gray, cv2.CV_64F, 0, 1, ksize=5)

        # Combine gradients
        mag, ang = cv2.cartToPolar(gx, gy)
        gradient = np.mean(mag)

        # Check liveness
        if gradient > 20:
            # Face is detected
            last_face_detection_time = time.time()
            face_detected = True
            return True
        else:
            # Face is not detected or considered fake
            current_time = time.time()
            if current_time - last_face_detection_time > 1.0 and face_detected:
                face_detected = False
                return True  # Detected as a live face
            return False

    faceCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    wCam, hCam = 400, 400

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while True:
        ret, img = cap.read()
        img = recognize(img, clf, faceCascade)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
'''

def cnt_increment():
    global cnt
    cnt += 1


def cnt_reset():
    global cnt
    cnt = 0



def face_recognition_socket(image):
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        global justscanned
        global pause_cnt
        global last_face_detection_time
        global face_detected
        print("fr:"+str(fr_random_attendance_id))
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        pause_cnt += 1

        for (x, y, w, h) in features:
            # Check liveness using HOG descriptor
            liveness = detect_liveness(img, x, y, w, h)
            if liveness:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                id, pred = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int(100 * (1 - pred / 300))

                if confidence > 80 and not justscanned:
                    cnt_increment()

                    if int(cnt) == 30:
                        cnt_reset()
                        #atime = str(date.today()) + ' ' + str(attendancetime) + ':00'

                        mycursor.execute("select a.img_person, b.first_name, b.last_name "
                                         "  from img_dataset a "
                                         "  left join users b on a.img_person = b.id "
                                         " where a.img_id = " + str(id))
                        row = mycursor.fetchone()
                        if row:
                            pnbr = row[0]
                            pname = row[1]
                            ###############################################################################################
                            #random_attendance_id = session['random_attendance_id']
                            random_attendance_id = fr_random_attendance_id

                            mycursor.execute("select a.group_id, a.random_time, a.duration "
                                             "  from random_attendance a "
                                             " where a.id = " + str(random_attendance_id))
                            row = mycursor.fetchone()
                            print(row)
                            group_id = row[0]
                            attendancetime = row[1]
                            attendanceduration = row[2]
                            #user_id = session['user_id']
                            atime = str(date.today()) + ' ' + str(attendancetime) + ':00'

                            print("gid" + str(group_id))
                            ###############################################################################################
                            mycursor.execute("select count(*) "
                                             "  from accs_hist "
                                             " where accs_date = curdate() AND group_id = '" + str(
                                group_id) + "' AND accs_prsn = '" + str(pnbr) + "' AND random_attendance_id = '" + str(
                                random_attendance_id) + "'")
                            row = mycursor.fetchone()
                            rowcount = row[0]

                            if rowcount > 0:
                                cv2.putText(img, pname + ', Present', (x - 10, y - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
                                justscanned = True
                                pause_cnt = 0
                            else:
                                cv2.putText(img, pname, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                            (153, 255, 255), 2,
                                            cv2.LINE_AA)

                                mycursor.execute(
                                    "insert into accs_hist (accs_date, accs_prsn, group_id, accs_added, random_attendance_id) values('" + str(
                                        date.today()) + "', '" + pnbr + "', '" + str(group_id) + "', '" + str(
                                        atime) + "', '" + str(
                                        random_attendance_id) + "')")
                                cnx.commit()

                                time.sleep(1)

                                justscanned = True
                                pause_cnt = 0
                        else:
                            cv2.putText(img, 'UNKNOWN', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2,
                                        cv2.LINE_AA)
                    else:
                        justscanned = False
                else:
                    if not justscanned:
                        cv2.putText(img, 'Spoofing', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2,
                                    cv2.LINE_AA)
                    else:
                        cv2.putText(img, 'Present', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (0, 0, 255), 2, cv2.LINE_AA)

                    if pause_cnt > 80:
                        justscanned = False

            else:
                if not justscanned:
                    cv2.putText(img, 'Spoofing', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img, 'Present', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (0, 0, 255), 2, cv2.LINE_AA)

                if pause_cnt > 80:
                    justscanned = False

    def recognize(img, clf, faceCascade):
        draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 0), "Face", clf)
        return img

    def detect_liveness(img, x, y, w, h):
        global last_face_detection_time
        global face_detected

        roi = img[y:y + h, x:x + w]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Define a region of interest for the face
        roi_hsv = hsv[int(0.1 * h):int(0.9 * h), int(0.1 * w):int(0.9 * w)]
        roi_gray = gray[int(0.1 * h):int(0.9 * h), int(0.1 * w):int(0.9 * w)]

        # Calculate gradients
        gx = cv2.Sobel(roi_gray, cv2.CV_64F, 1, 0, ksize=5)
        gy = cv2.Sobel(roi_gray, cv2.CV_64F, 0, 1, ksize=5)

        # Combine gradients
        mag, ang = cv2.cartToPolar(gx, gy)
        gradient = np.mean(mag)

        # Check liveness
        if gradient > 20:
            # Face is detected
            last_face_detection_time = time.time()
            face_detected = True
            return True
        else:
            # Face is not detected or considered fake
            current_time = time.time()
            if current_time - last_face_detection_time > 1.0 and face_detected:
                face_detected = False
                return True  # Detected as a live face
            return False

    faceCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    wCam, hCam = 400, 400


    img = recognize(image, clf, faceCascade)

        #frame = cv2.imencode('.jpg', img)[1].tobytes()
        #yield (b'--frame\r\n'
               #b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return img




# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< END Face Recognition >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Optimization >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< END  Optimization >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/vfdataset_page')
def vfdataset_page():
    global nbr
    nbr = session['user_id']
    global img_id, count_img, max_imgid
    img_id = 0
    return render_template('gendataset.html', prs=session['user_id'])


@app.route('/vidfeed_dataset/<nbr>')
def vidfeed_dataset(nbr):
    mycursor.execute("select * from img_dataset WHERE img_person='" + str(nbr) + "'")
    data1 = mycursor.fetchall()
    for item in data1:
        imagePath = "dataset/" + str(nbr) + "." + str(item[0]) + ".jpg"
        # print(imagePath)
        try:
            os.remove(imagePath)
        except:
            pass
    mycursor.execute("delete from img_dataset WHERE img_person='" + str(nbr) + "'")
    cnx.commit()

    mycursor.execute("select ifnull(max(img_id), 0) from img_dataset")
    row = mycursor.fetchone()
    global lastid
    lastid = row[0]
    global count_img
    count_img = 0
    print("generate")
    global img_id
    img_id = lastid
    global max_imgid
    max_imgid = img_id + 100

    # Video streaming route. Put this in the src attribute of an img tag
    return Response(nbr, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    random_attendance_id = session['random_attendance_id']
    mycursor.execute("select a.group_id, a.random_time, a.duration "
                     "  from random_attendance a "
                     " where a.id = " + str(random_attendance_id))
    row = mycursor.fetchone()

    group_id = row[0]
    attendancetime = row[1]
    attendanceduration = row[2]
    user_id = session['user_id']

    # attendancetime = session['attendancetime']
    # attendanceduration = session['attendanceduration']

    # Video streaming route. Put this in the src attribute of an img tag
    #return Response(face_recognition(group_id, attendancetime, attendanceduration, random_attendance_id, user_id),
                    #mimetype='multipart/x-mixed-replace; boundary=frame')
    return user_id


@app.route('/video_show')
def video_show():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(face_show(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/fr_page', methods=['GET', 'POST'])
def fr_page():
    """Video streaming home page."""
    user_id = session['user_id']
    data = ""

    mycursor.execute("select a.accs_id, a.accs_prsn, b.first_name, b.last_name, a.accs_added "
                     "  from accs_hist a "
                     "  left join users b on a.accs_prsn = b.id "
                     " where a.accs_prsn = '" + str(user_id) + "' AND a.accs_date = curdate() "
                                                               " order by 1 desc")
    data = mycursor.fetchall()

    atdone = "no"
    random_attendance_id = session['random_attendance_id']
    mycursor.execute("select count(*) "
                     "  from accs_hist "
                     " where accs_date = curdate() AND  accs_prsn = '" + str(
        user_id) + "' AND random_attendance_id = '" + str(random_attendance_id) + "'")
    row = mycursor.fetchone()
    rowcount = row[0]
    if rowcount > 0:
        atdone = "yes"
    else:
        atdone = "no"
    '''
    attendancetime = str(date.today())
    if request.args.get('time') != "" and request.args.get('time') != None and request.args.get('time') != "auto":
        session['attendancetime'] = request.args.get('time')
        attendancetime = session['attendancetime']
        #attendancetime = request.args.get('time')

    session['attendanceduration'] = 0
    if request.args.get('duration') != "" and request.args.get('duration') != None and request.args.get('duration') != "auto":
        session['attendanceduration'] = request.args.get('duration')
    '''

    random_attendance_id = session['random_attendance_id']
    mycursor.execute("select a.group_id, a.random_time, a.duration "
                     "  from random_attendance a "
                     " where a.id = " + str(random_attendance_id))
    row = mycursor.fetchone()
    # group_id = row[0]
    # session['attendancetime'] = row[1]
    #print(row)
    session['attendanceduration'] = row[2]

    # session['random_attendance_id']="6"
    #####################################################################################################
    random_attendance_id = session['random_attendance_id']
    global fr_random_attendance_id
    fr_random_attendance_id = random_attendance_id
    print("frc:"+str(fr_random_attendance_id))

    #######################################################################################################################


    return render_template('fr_page.html', data=data, data1=atdone)


@app.route('/countTodayScan')
def countTodayScan():
    cnx = mysql.connector.connect(**config)
    mycursor = cnx.cursor()

    mycursor.execute("select count(*) "
                     "  from accs_hist "
                     " where accs_date = curdate() ")
    row = mycursor.fetchone()
    rowcount = row[0]
    print(rowcount)
    return jsonify({'rowcount': rowcount})


@app.route('/loadData', methods=['GET', 'POST'])
def loadData():
    cnx = mysql.connector.connect(**config)
    mycursor = cnx.cursor()
    user_id = session['user_id']

    mycursor.execute("select a.accs_id, a.accs_prsn, b.first_name, b.last_name, date_format(a.accs_added, '%H:%i:%s') "
                     "  from accs_hist a "
                     "  left join users b on a.accs_prsn = b.id "
                     " where a.accs_date = curdate() and b.id = " + str(user_id) +
                     " order by 1 desc")

    '''
      mycursor.execute("select a.accs_id, a.accs_prsn, b.first_name, b.last_name, date_format(a.accs_added, '%H:%i:%s') "
                       "  from accs_hist a "
                       "  left join users b on a.accs_prsn = b.id "
                       " where a.accs_date = curdate() "
                       " order by 1 desc")
    '''
    data = mycursor.fetchall()

    return jsonify(response=data)


@app.route('/')
def add_login_view():
    msg = ""
    return render_template('login.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login_submit():
    msg = ""
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # mycursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password,))
        mycursor.execute("SELECT * FROM users WHERE email ='%s' AND password ='%s'" % (email, password))
        account = mycursor.fetchone()
        if account:
            if account[7] != 'teacher':
                # if account[14] == 1:
                session['loggedin'] = True
                session['user_id'] = account[0]
                session['user_name'] = account[1] + ' ' + account[2]
                session['user_email'] = account[3]
                session['user_role'] = account[7]
                session['user_photo'] = account[13]
                session['random_attendance_id'] = '0'
                msg = "<div class='alert alert-success'>Successfully LogIn</div>"
                # return render_template('updateownprofile.html', msg=msg)
                return redirect(url_for('updateownprofile'))
            # else:
            # msg = " Your account is not approved!"
            elif account[7] != 'admin':
                # if account[14] == 1:
                session['loggedin'] = True
                session['user_id'] = account[0]
                session['user_name'] = account[1] + ' ' + account[2]
                session['user_email'] = account[3]
                session['user_role'] = account[7]
                session['user_photo'] = account[13]
                session['random_attendance_id'] = '0'
                msg = "<div class='alert alert-success'>Successfully LogIn</div>"
                # return render_template('updateownprofile.html', msg=msg)
                return redirect(url_for('updateownprofile'))
            # else:
            # msg = " Your account is not approved!"
            else:
                session['loggedin'] = True
                session['user_id'] = account[0]
                session['user_name'] = account[1] + ' ' + account[2]
                session['user_email'] = account[3]
                session['user_role'] = account[7]
                session['user_photo'] = account[13]
                msg = "Successfully LogIn"
                # return render_template('updateownprofile.html', msg=msg)
                return redirect(url_for('updateownprofile'))
        else:
            flash('Email or password Incorrect', 'danger')
    return render_template('login.html', msg=msg)


@app.route('/signup')
def signup():
    msg = ""
    return render_template('signup.html', msg=msg)


@app.route('/signup', methods=['POST'])
def signup_submit():
    msg = ""
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'password' in request.form and 'email' in request.form:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        re_password = request.form['re_password']
        email = request.form['email']
        user_role = "student"
        phone = ""

        password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$'

        if password == re_password:
            mycursor.execute("SELECT * FROM users WHERE email = '%s'" % (email))
            account = mycursor.fetchone()
            if account:
                flash('Email already exists !', 'danger')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid Email Address', 'danger')
            elif not re.match(r'[A-Za-z0-9]+', first_name):
                flash('First Name must contain only characters and numbers !', 'danger')
            elif not re.match(password_pattern, password):
                flash(
                    'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character (@, #, $, %, ^, &, +, =, !).',
                    'danger')
            elif not first_name or not password or not email:
                flash('Please Fill out the form', 'danger')
            else:
                mycursor.execute(
                    "insert into users ( first_name, last_name, email, password, user_role, phone) values('" + str(
                        first_name) + "', '" + str(last_name) + "', '" + str(email) + "', '" + str(
                        password) + "', '" + str(user_role) + "', '" + str(phone) + "')")
                cnx.commit()

                flash('You have successfully registered', 'success')
                return add_login_view()
        else:
            flash('Your password and re-entered password is not matching.', 'danger')
    elif request.method == 'POST':
        flash('Please fill out the form', 'danger')
    return render_template('signup.html', msg=msg)


@app.route('/updateownprofile')
def updateownprofile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        mycursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
        account = mycursor.fetchone()
        # Show the profile page with account info
        return render_template('updateownprofile.html', account=account)
    else:
        return redirect(url_for('login'))


# app.config["IMAGE_UPLOADS"] = "C:/Users/raja/PycharmProjects/FlaskOpencv_FaceRecognition/static/user_photo/"
app.config["IMAGE_UPLOADS"] = "static/user_photo"


@app.route('/updateownprofile', methods=['GET', 'POST'])
def updateownprofile_submit():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        i_d = request.form['i_d']
        userlist_id = session['user_id']
        photo = request.form['photo']
        if request.files:
            image = request.files["fileToUpload"]
            if image.filename != '' and image.filename != None:
                image.filename = first_name + "-" + image.filename
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                photo = image.filename
                session['user_photo'] = photo
            # return render_template("updateownprofile.html", uploaded_image=image.filename)
            # return updateownprofile()
        else:
            photo = request.form['photo']

        query = (
            "UPDATE users SET "
            "first_name=%s, last_name=%s, email=%s, phone=%s, photo=%s, dob=%s, i_d=%s "
            "WHERE id=%s"
        )

        values = (first_name, last_name, email, phone, photo, dob, i_d, userlist_id)

        mycursor.execute(query, values)
        cnx.commit()

    # return render_template("updateownprofile.html")
    return updateownprofile()


@app.route('/userlist')
def userlist():
    cnx = mysql.connector.connect(**config)
    mycursor = cnx.cursor()
    data1 = ""
    # mycursor.execute("select * from users where user_role!='teacher'")
    mycursor.execute(
        "SELECT DISTINCT(b.img_person), a.* FROM users a LEFT JOIN img_dataset b ON a.id = b.img_person WHERE user_role NOT IN ('teacher', 'admin')")
    data = mycursor.fetchall()
    creater_id = session['user_id']
    mycursor.execute("select * from tbl_groups WHERE creater_id='" + str(creater_id) + "'")
    data1 = mycursor.fetchall()
    mycursor.execute("select * from join_groups")
    data2 = mycursor.fetchall()
    # return jsonify(response=data)
    # return render_template('userlist.html')
    return render_template('userlist.html', data=data, data1=data1, data2=data2)


@app.route('/user_functions', methods=['GET', 'POST'])
def user_functions():
    userlistid = request.args.get('userlistid')
    action = request.args.get('action')
    if action == 'approved':
        mycursor.execute("UPDATE users SET approved='1' WHERE id='" + str(userlistid) + "'")
        cnx.commit()
    # return userlist()
    return redirect(url_for('userlist'))


@app.route('/group_functions', methods=['GET', 'POST'])
def group_functions():
    userlistid = request.args.get('userlistid')
    group_id = request.args.get('group_id')
    action = request.args.get('action')
    if action == 'invite':
        if not group_id or not userlistid:
            flash("Invalid group_id or userlistid", "danger")
        else:
            account = check_membership(group_id, userlistid)
            if account:
                flash("No course selected. Please Create a course and try again!", "danger")
            else:
                mycursor.execute("INSERT INTO join_groups (group_id, user_id) VALUES (%s, %s)", (group_id, userlistid))
                cnx.commit()
                flash("Student added successfully", "success")

    elif action == 'remove':
        if not group_id or not userlistid:
            flash("Invalid group_id or userlistid", "danger")
        else:
            account = check_membership(group_id, userlistid)
            if not account:
                flash("User is not in the group", "danger")
            else:
                mycursor.execute("DELETE FROM join_groups WHERE group_id=%s AND user_id=%s", (group_id, userlistid))
                cnx.commit()
                flash("Student removed from the group", "success")

    elif action == 'approved':
        mycursor.execute(
            "UPDATE join_groups SET user_approved='1' WHERE group_id=%s AND user_id=%s", (group_id, userlistid))
        cnx.commit()
        flash("User approval updated successfully", "success")

    elif request.method == "POST":
        group_id = request.form['select_group']
        for userlistid in request.form.getlist('userlist[]'):
            if not group_id or not userlistid:
                flash("Invalid group_id or userlistid", "danger")
            else:
                account = check_membership(group_id, userlistid)
                if account:
                    flash("Student already added to the group", "danger")
                else:
                    mycursor.execute("INSERT INTO join_groups (group_id, user_id) VALUES (%s, %s)", (group_id, userlistid))
                    cnx.commit()
                    flash("Student added successfully", "success")

    return redirect(url_for('userlist'))

def check_membership(group_id, userlistid):
    mycursor.execute("SELECT * FROM join_groups WHERE group_id=%s AND user_id=%s", (group_id, userlistid))
    return mycursor.fetchone()


@app.route('/grouprequest', methods=['GET', 'POST'])
def grouprequest():
    if 'loggedin' in session:
        m = ""
    else:
        return redirect(url_for('login'))

    group_id = request.args.get('group_id')
    action = request.args.get('action')
    groupteacher = request.args.get('groupteacher')
    groupname = request.args.get('groupname')
    msg = "yes"
    userrole = session['user_role']
    if action == 'invitelink' and userrole != 'teacher':
        userlistid = session['user_id']

        mycursor.execute(
            "SELECT * FROM join_groups WHERE group_id='" + str(group_id) + "' AND user_id='" + str(userlistid) + "'")
        account = mycursor.fetchone()
        if account:
            mycursor.execute(
                "SELECT * FROM join_groups WHERE user_approved = 0 AND group_id='" + str(
                    group_id) + "' AND user_id='" + str(
                    userlistid) + "'")
            accounts = mycursor.fetchone()
            if accounts:
                # return render_template("grouprequest.html", group_id=group_id,groupteacher=groupteacher,groupname=groupname)
                msg = "Please accept the request."
            else:
                msg = "You already a member of this group."
                return redirect(url_for('grouplist'))
        else:
            mycursor.execute("INSERT INTO join_groups ( group_id, user_id) VALUES ('" + str(group_id) + "','" + str(
                userlistid) + "')")
            cnx.commit()
            msg = "inserted"
        # return render_template("grouprequest.html", group_id=group_id,groupteacher=groupteacher,groupname=groupname)

    if request.method == "POST" and 'accept' in request.form:
        joinrequest = request.form['accept']
        print(joinrequest)
        userlistid = session['user_id']
        mycursor.execute(
            "UPDATE join_groups SET user_approved='1' WHERE group_id='" + str(group_id) + "' AND user_id='" + str(
                userlistid) + "'")
        cnx.commit()
        # return userlist()
        return redirect(url_for('grouplist'))

    if request.method == "POST" and 'reject' in request.form:
        reject = request.form['reject']
        print(reject)
        return redirect(url_for('grouplist'))

    print(msg)
    if msg == "yes":
        return redirect(url_for('updateownprofile'))

    return render_template('grouprequest.html', msg=msg, group_id=group_id, groupteacher=groupteacher,
                           groupname=groupname)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    # return redirect(url_for('login'))
    return login_submit()


@app.route('/groups', methods=['GET', 'POST'])
def groups():
    creater_id = session['user_id']

    if request.method == 'POST':
        # Check if the request is a renaming request
        group_id = request.form.get('group_id')
        new_group_name = request.form.get('new_group_name')

        if group_id and new_group_name:
            # Perform the update in your database (replace with your actual database update logic)
            mycursor.execute("UPDATE tbl_groups SET group_name = %s WHERE id = %s", (new_group_name, group_id))
            cnx.commit()
        else:
            # Handle the form submission for creating a new channel
            group_name = request.form.get('group_name')
            if group_name:
                mycursor.execute("INSERT INTO tbl_groups (group_name, creater_id) VALUES (%s, %s)",
                                 (group_name, creater_id))
                cnx.commit()

    # Fetch the updated data from the database
    mycursor.execute(
        "SELECT id, group_name, date_format(created, '%d-%m-%Y %W %H:%i:%s') FROM tbl_groups WHERE creater_id='" + str(
            creater_id) + "'")
    data = mycursor.fetchall()

    return render_template('groups.html', data=data)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    id = request.args.get('id')
    rurl = request.args.get('rurl')

    # Using parameterized query to prevent SQL injection
    query = "DELETE FROM tbl_groups WHERE id=%s"
    values = (id,)

    mycursor.execute(query, values)
    cnx.commit()

    return redirect(url_for(rurl))


@app.route('/grouplist', methods=['GET', 'POST'])
def grouplist():
    user_id = session['user_id']
    action = request.args.get('action')
    group_id = request.args.get('group_id')
    if action == 'invite' and (group_id is None or group_id == ''):
        # Handle the error, for example, return an error response
        return jsonify({'error': 'group_id is required for action=invite'}), 400

    if action == 'invite':
        mycursor.execute(
            "SELECT * FROM join_groups WHERE group_id='" + str(group_id) + "' AND user_id='" + str(user_id) + "'")
        account = mycursor.fetchone()
        if account:
            msg = ""
        else:
            mycursor.execute("INSERT INTO join_groups ( group_id, user_id) VALUES ('" + str(group_id) + "','" + str(
                user_id) + "')")
            cnx.commit()
        return redirect(url_for('userlist'))

    # mycursor.execute("SELECT join_groups.group_id,groups.group_name,join_groups.user_approved FROM join_groups left JOIN groups ON join_groups.group_id=groups.id WHERE user_id='" + str(user_id) + "'")
    mycursor.execute(
        "SELECT join_groups.group_id,tbl_groups.group_name,join_groups.user_approved,users.first_name,users.last_name FROM join_groups left JOIN tbl_groups ON join_groups.group_id=tbl_groups.id left JOIN users ON tbl_groups.creater_id=users.id WHERE user_id='" + str(
            user_id) + "'")
    data = mycursor.fetchall()

    group_id = request.args.get('group_id')
    groupteacher = request.args.get('groupteacher')
    groupname = request.args.get('groupname')
    action = request.args.get('action')
    data1 = ""
    if action == 'view_members':
        # mycursor.execute(
        #  "SELECT users.first_name,users.last_name,users.user_role FROM `join_groups` left JOIN groups ON join_groups.group_id=groups.id left JOIN users ON join_groups.user_id=users.id WHERE join_groups.user_approved='1' AND join_groups.group_id='" + str(
        #     group_id) + "'")
        mycursor.execute(
            "SELECT users.first_name,users.last_name,users.user_role FROM `join_groups` left JOIN tbl_groups ON join_groups.group_id=tbl_groups.id left JOIN users ON join_groups.user_id=users.id WHERE join_groups.group_id='" + str(
                group_id) + "'")
        data1 = mycursor.fetchall()

    if action == 'file_share':
        print("Received file upload request")
        if 'file' in request.files:
            print("File found in request")
            file = request.files['file']
            if file and allowed_file(file.filename):
                print("File is valid")
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Get user_id from the session
                user_id = session.get('user_id')
                print(f"User ID: {user_id}")

                if user_id is not None:
                    # Save file information to the database
                    mycursor.execute(
                        "INSERT INTO files (group_id, user_id, file_name, uploaded_by, upload_datetime) VALUES (%s, %s, %s, %s, NOW())",
                        (group_id, user_id, filename, user_id))
                    cnx.commit()  # Commit changes to the database
                    print("File successfully uploaded and database updated")
                else:
                    # Handle the case where user_id is not available in the session
                    flash('User ID not found. Unable to upload file.', 'error')
                    print("User ID not found. Unable to upload file.")

    mycursor.execute("SELECT * FROM files WHERE group_id=%s", (group_id,))
    file_data = mycursor.fetchall()

    return render_template('grouplist.html', data=data, data1=data1, groupteacher=groupteacher, groupname=groupname, file_data=file_data, group_id=group_id)


@app.route('/teachersignup')
def teachersignup():
    msg = ""
    return render_template('teachersignup.html', msg=msg)


@app.route('/teachersignup', methods=['POST'])
def teachersignup_submit():
    msg = ""
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'password' in request.form and 'email' in request.form:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        re_password = request.form['re_password']
        email = request.form['email']
        user_role = "teacher"
        phone = ""
        password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$'

        if password == re_password:
            mycursor.execute("SELECT * FROM users WHERE email = '%s'" % (email))
            account = mycursor.fetchone()
            if account:
                flash('Email already exists !', 'danger')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address !', 'danger')
            elif not re.match(r'[A-Za-z0-9]+', first_name):
                flash('First Name must contain only characters and numbers !', 'danger')
            elif not re.match(password_pattern, password):
                flash(
                    'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character (@, #, $, %, ^, &, +, =, !).',
                    'danger')
            elif not first_name or not password or not email:
                flash('Please fill out the form !', 'danger')
            else:
                mycursor.execute(
                    "insert into users ( first_name, last_name, email, password, user_role, phone) values('" + str(
                        first_name) + "', '" + str(last_name) + "', '" + str(email) + "', '" + str(
                        password) + "', '" + str(user_role) + "', '" + str(phone) + "')")
                cnx.commit()
                flash('You have successfully registered !', 'success')
                return add_login_view()
        else:
            flash('Your password and re-entered password is not matching.', 'danger')
    elif request.method == 'POST':
        flash('Please fill out the form !', 'danger')
    return render_template('teachersignup.html', msg=msg)


@app.route('/report', methods=['GET', 'POST'])
def report():
    user_id = session['user_id']
    user_role = session['user_role']
    filters = ""
    if request.method == 'POST' and 'filter' in request.form and 'startdate' in request.form and 'enddate' in request.form:
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        if request.form['startdate'] != "" and request.form['enddate'] != "":
            filters = " and a.accs_date BETWEEN '" + str(startdate) + "' AND '" + str(enddate) + "'"

    if request.method == 'POST' and 'filter' in request.form and 'group' in request.form:
        if request.form['group'] != "":
            group = request.form['group']
            filters += " and c.group_name LIKE '%" + str(group) + "%'"
    print(filters)
    if user_role != 'teacher':
        mycursor.execute(
            "select c.group_name, a.accs_prsn, b.first_name, b.last_name, date_format(a.accs_added, '%d-%m-%Y %W %H:%i:%s') "
            "  from accs_hist a "
            "  left join users b on a.accs_prsn = b.id "
            "  left join tbl_groups c on a.group_id = c.id "
            " where b.id = " + str(user_id) +
            "" + str(filters) +
            " order by a.accs_id desc")
    else:
        mycursor.execute(
            "select c.group_name, a.accs_prsn, b.first_name, b.last_name, date_format(a.accs_added, '%d-%m-%Y %W %H:%i:%s') "
            "  from accs_hist a "
            "  left join users b on a.accs_prsn = b.id "
            "  left join tbl_groups c on a.group_id = c.id "
            " where b.id != 0 and c.creater_id = " + str(user_id) +
            "" + str(filters) +
            " order by a.accs_id desc")

    data = mycursor.fetchall()
    return render_template('report.html', data=data)


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx'}


def allowed_file(filename):
    return True


UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/agrouplist', methods=['GET', 'POST'])
def agrouplist():

    cnx = mysql.connector.connect(**config)
    mycursor = cnx.cursor()

    group_id = request.args.get('group_id')
    groupteacher = request.args.get('groupteacher')
    groupname = request.args.get('groupname')
    action = request.args.get('action')
    data1 = ""
    data = ""
    data2 = ""
    if action == 'view_members':
        session['group_id'] = group_id
        session['groupteacher'] = groupteacher
        session['groupname'] = groupname
        session['actions'] = action

    if action == 'remove':
        userlist_id = request.args.get('userlist_id')
        mycursor.execute(
            "DELETE FROM join_groups WHERE group_id='" + str(group_id) + "' AND user_id='" + str(userlist_id) + "'")
        cnx.commit()

    if action == 'invite':
        userlist_id = request.args.get('userlist_id')
        mycursor.execute(
            "SELECT * FROM join_groups WHERE group_id='" + str(group_id) + "' AND user_id='" + str(userlist_id) + "'")
        account = mycursor.fetchone()
        if account:
            msg = ""
        else:
            mycursor.execute("INSERT INTO join_groups ( group_id, user_id) VALUES ('" + str(group_id) + "','" + str(
                userlist_id) + "')")
            cnx.commit()
    if action == 'file_share':
        print("Received file upload request")
        if 'file' in request.files:
            print("File found in request")
            file = request.files['file']
            if file and allowed_file(file.filename):
                print("File is valid")
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Get user_id from the session
                user_id = session.get('user_id')
                print(f"User ID: {user_id}")

                if user_id is not None:
                    # Save file information to the database
                    mycursor.execute(
                        "INSERT INTO files (group_id, user_id, file_name, uploaded_by, upload_datetime) VALUES (%s, %s, %s, %s, NOW())",
                        (group_id, user_id, filename, user_id))
                    cnx.commit()  # Commit changes to the database
                    print("File successfully uploaded and database updated")
                else:
                    # Handle the case where user_id is not available in the session
                    flash('User ID not found. Unable to upload file.', 'error')
                    print("User ID not found. Unable to upload file.")


    if session['actions'] == 'view_members':
        group_id = session['group_id']
        groupteacher = session['groupteacher']
        groupname = session['groupname']
        # mycursor.execute(
        #   "SELECT users.first_name,users.last_name,users.user_role,users.id,users.photo FROM `join_groups` left JOIN groups ON join_groups.group_id=groups.id left JOIN users ON join_groups.user_id=users.id WHERE join_groups.user_approved='1' AND join_groups.group_id='" + str(
        #     group_id) + "'")
        mycursor.execute(
            "SELECT users.first_name,users.last_name,users.user_role,users.id,users.photo FROM `join_groups` left JOIN tbl_groups ON join_groups.group_id=tbl_groups.id left JOIN users ON join_groups.user_id=users.id WHERE join_groups.group_id='" + str(
                group_id) + "'")
        data1 = mycursor.fetchall()
        mycursor.execute("select * from users where user_role!='teacher'")
        data2 = mycursor.fetchall()

    if action == 'view_report':
        userlist_id = request.args.get('userlist_id')
        mycursor.execute(
            "select a.accs_id, a.accs_prsn, b.first_name, b.last_name, date_format(a.accs_added, '%d-%m-%Y %W %H:%i:%s') "
            "  from accs_hist a "
            "  left join users b on a.accs_prsn = b.id "
            " where b.id = " + str(userlist_id) +
            " and a.group_id = '" + str(group_id) + "'"
                                                    " order by a.accs_id desc")
        data = mycursor.fetchall()



    mycursor.execute("SELECT * FROM files WHERE group_id=%s", (group_id,))
    file_data = mycursor.fetchall()

    user_id = session['user_id']
    mycursor.execute(
        "select * from random_attendance where DATE(created)=CURDATE() AND TIME_FORMAT(random_time, '%H:%i')>=TIME_FORMAT(CURRENT_TIME(), '%H:%i') AND group_id='" + str(
            group_id) + "' AND user_id='" + str(user_id) + "'")
    data3 = mycursor.fetchall()

    mycursor.execute(
        "select *,now() from random_attendance where DATE(created)=CURDATE() AND TIME_FORMAT(random_time, '%H:%i')<TIME_FORMAT(CURRENT_TIME(), '%H:%i') AND group_id='" + str(
            group_id) + "' AND user_id='" + str(user_id) + "'")
    data4 = mycursor.fetchall()

    return render_template('agrouplist.html', data=data, data1=data1, groupteacher=groupteacher, groupname=groupname,
                           group_id=group_id, data2=data2, data3=data3, data4=data4, file_data=file_data)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
@app.route('/loadattendanceData', methods=['GET', 'POST'])
def loadattendanceData():
    group_id = session['group_id']
    mycursor.execute(
        "select COUNT(a.accs_prsn) as v, b.first_name, b.last_name,a.accs_prsn from accs_hist a left join users b on a.accs_prsn = b.id where a.group_id = '" + str(
            group_id) + "' GROUP BY a.accs_prsn")
    data = mycursor.fetchall()

    return jsonify(response=data)


@app.route('/loadattendanceDatareport', methods=['GET', 'POST'])
def loadattendanceDatareport():
    user_id = session['user_id']
    user_role = session['user_role']
    # group_id = session['group_id']
    if user_role != 'teacher':
        mycursor.execute(
            "select COUNT(a.accs_prsn) as v, c.group_name, b.first_name, b.last_name,a.accs_prsn,a.group_id from accs_hist a left join users b on a.accs_prsn = b.id left join tbl_groups c on a.group_id=c.id WHERE a.accs_prsn='" + str(
                user_id) + "' GROUP BY a.group_id")
    else:
        mycursor.execute(
            "select COUNT(a.accs_prsn) as v, b.first_name, b.last_name,a.accs_prsn from accs_hist a left join users b on a.accs_prsn = b.id GROUP BY a.accs_prsn")

    data = mycursor.fetchall()

    return jsonify(response=data)


@app.route('/setrandomattendance', methods=['GET', 'POST'])
def setrandomattendance():
    if request.method == "POST":
        group_id = request.form['group_id']
        duration = request.form['duration']
        user_id = session['user_id']
        status = "active"
        # random_time = str(request.form.getlist['random_time[]'])
        for random_time in request.form.getlist('random_time[]'):
            print(random_time)
            mycursor.execute(
                "INSERT INTO random_attendance ( user_id, group_id, random_time, duration, status) VALUES ('" + str(
                    user_id) + "','" + str(
                    group_id) + "','" + str(random_time) + "','" + str(duration) + "','" + str(status) + "')")
            cnx.commit()
        print(random_time)

    data = ""
    # return jsonify(response=data)
    return redirect(url_for('agrouplist'))


@app.route('/countTodayAttenScan', methods=['GET', 'POST'])
def countTodayAttenScan():
    user_id = session['user_id']
    cnx = mysql.connector.connect(**config)
    # mycursor = cnx.cursor()
    mycursor = cnx.cursor(buffered=True)
    # mycursor.execute("select a.group_id,a.random_time,now(),CURRENT_TIME() from random_attendance a left join join_groups c on a.group_id=c.group_id WHERE c.user_id='" + str(user_id) + "' AND DATE(a.created)=CURDATE() AND a.random_time>CURRENT_TIME()")
    # mycursor.execute("select a.id from random_attendance a left join join_groups c on a.group_id=c.group_id WHERE c.user_id='" + str(user_id) + "' AND DATE(a.created)=CURDATE() AND TIME_FORMAT(a.random_time, '%H:%i')=TIME_FORMAT(CURRENT_TIME(), '%H:%i')")
    mycursor.execute(
        "select a.id from random_attendance a left join join_groups c on a.group_id=c.group_id WHERE c.user_id='" + str(
            user_id) + "' AND DATE(a.created)=CURDATE() AND TIME_FORMAT(a.random_time, '%H')=TIME_FORMAT(CURRENT_TIME(), '%H') AND TIME_FORMAT(CURRENT_TIME(), '%i') - TIME_FORMAT(a.random_time, '%i')=0")
    row = mycursor.fetchone()
    print(row)
    random_attendance_id = ""
    if row:
        print("row")

        random_attendance_id = str(row[0])
        mycursor.execute(
            "select count(*) from accs_hist a WHERE a.accs_prsn='" + str(
                user_id) + "' AND a.random_attendance_id ='" + str(random_attendance_id) + "'")
        row1 = mycursor.fetchone()
        rowcount = row1[0]
        if rowcount > 0:
            print("done already")
        else:
            session['random_attendance_id'] = random_attendance_id
    print(random_attendance_id)
    return jsonify({'random_attendance_id': random_attendance_id})


############################## User management routes #######################################

@app.route('/users')
def users():
    # Fetch and display the list of users from the database
    mycursor.execute("SELECT id, first_name, last_name, email, user_role, password FROM users")
    users = [{'id': user[0], 'first_name': user[1], 'last_name': user[2], 'email': user[3], 'user_role': user[4],
              'password': user[5]} for user in mycursor.fetchall()]
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    # Add a new user to the database
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        user_role = request.form['user_role']
        password = request.form['password']
        password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$'

        # Check if the email is already used by another user
        mycursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = mycursor.fetchone()

        if existing_user:
            flash('Email already in use by another user.', 'danger')
        elif not first_name or not last_name or not email or not user_role:
            flash('All fields are required.', 'danger')
        elif not re.match(password_pattern, password):
            flash(
                'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character (@, #, $, %, ^, &, +, =, !).',
                'danger')
        else:
            mycursor.execute(
                "INSERT INTO users (first_name, last_name, email, user_role, password) VALUES (%s, %s, %s, %s, %s)",
                (first_name, last_name, email, user_role, password))
            cnx.commit()
            flash('User added successfully.', 'success')

    return redirect(url_for('users'))


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Edit an existing user's information
    mycursor.execute("SELECT id, first_name, last_name, email, user_role, password FROM users WHERE id = %s",
                     (user_id,))
    user = mycursor.fetchone()

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('users'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        user_role = request.form['user_role']
        password = request.form['password']

        # Check if the email is already used by another user (excluding the user being edited)
        mycursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", (email, user_id))
        existing_user = mycursor.fetchone()

        if existing_user:
            flash('Email already in use by another user.', 'danger')
        elif not first_name or not last_name or not email or not user_role:
            flash('All fields are required.', 'danger')
        else:
            if password:  # Only update the password if it's not empty
                mycursor.execute(
                    "UPDATE users SET first_name = %s, last_name = %s, email = %s, user_role = %s, password = %s WHERE id = %s",
                    (first_name, last_name, email, user_role, password, user_id))
                cnx.commit()
                flash('User updated successfully.', 'success')
            else:
                mycursor.execute(
                    "UPDATE users SET first_name = %s, last_name = %s, email = %s, user_role = %s WHERE id = %s",
                    (first_name, last_name, email, user_role, user_id))
                cnx.commit()
                flash('User updated successfully.', 'success')
            return redirect(url_for('users'))

    return render_template('edit_user.html', user=user)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Delete a user from the database
    mycursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    cnx.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('users'))


@app.route('/updateprofile', methods=['GET'])
def updateprofile():
    userlist_id = ""
    if request.args.get('id') != "" and request.args.get('id') != None:
        session['userlist_id'] = request.args.get('id')
    userlist_id = session['userlist_id']
    mycursor.execute("SELECT * FROM users WHERE user_role!='teacher' AND id='" + str(userlist_id) + "'")
    account = mycursor.fetchone()
    # Show the profile page with account info
    return render_template('updateprofile.html', account=account)


@app.route('/updateprofile', methods=['POST'])
def updateprofile_submit():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        i_d = request.form['i_d']
        userlist_id = session['userlist_id']
        photo = request.form['photo']
        if request.files:
            image = request.files["fileToUpload"]
            if image.filename != '' and image.filename != None:
                image.filename = first_name + "-" + image.filename
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                photo = image.filename
            # return render_template("updateownprofile.html", uploaded_image=image.filename)
            # return updateownprofile()
        else:
            photo = request.form['photo']

        mycursor.execute(
            "UPDATE users SET first_name='" + str(first_name) + "',last_name='" + str(last_name) + "',email='" + str(
                email) + "',phone='" + str(phone) + "', photo='" + str(photo) + "', dob='" + str(dob) + "', i_d='" + str(
                i_d) + "' WHERE id='" + str(userlist_id) + "'")
        cnx.commit()

    # return render_template("updateprofile.html")
    return updateprofile()


#####################################################
@app.route("/meeting")
def meeting():
    return render_template("meeting.html")


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        room_id = request.form.get("roomID")
        return redirect(f"/meeting?roomID={room_id}")

    # Retrieve the group_id from the query parameter
    group_id = request.args.get("group_id")

    # Set room_id based on group_id (You may need to fetch the actual room_id)
    room_id = group_id

    # Automatically redirect to the meeting page with room_id
    return redirect(f"/meeting?roomID={room_id}")

# -------- Manage Course --------------
@app.route('/manage_groups')
def manage_groups():
    search_term = request.args.get('search_term', '')
    cnx = mysql.connector.connect(**config)
    mycursor = cnx.cursor()
    mycursor.execute("SELECT * FROM tbl_groups WHERE group_name LIKE %s OR creater_id = %s",
                    (f'%{search_term}%', search_term))
    groups = mycursor.fetchall()
    return render_template('manage_groups.html', groups=groups, search_term=search_term)

@app.route('/create_group', methods=['POST'])
def create_group():
    group_name = request.form['group_name']

    creater_id = request.form['creater_id']

    cnx = mysql.connector.connect(**config)

    mycursor = cnx.cursor()

    try:

        mycursor.execute("INSERT INTO tbl_groups (group_name, creater_id) VALUES (%s, %s)", (group_name, creater_id))

        cnx.commit()

        return redirect(url_for('manage_groups'))

    except Exception as e:

        # Handle exceptions, print or log the error for debugging

        print(f"Error creating group: {e}")

        cnx.rollback()

        # Optionally, you can redirect to an error page or display an error message

        return "Error creating group. Please try again."

    finally:

        mycursor.close()

        cnx.close()


@app.route('/update_group/<int:group_id>', methods=['GET', 'POST'])
def update_group(group_id):
    cnx = mysql.connector.connect(**config)
    mycursor = cnx.cursor()

    try:
        mycursor.execute("SELECT * FROM tbl_groups WHERE id = %s", (group_id,))
        group = mycursor.fetchone()

        if request.method == 'POST':
            group_id = request.form['group_id']
            group_name = request.form['group_name']
            creater_id = request.form['creater_id']

            mycursor.execute("UPDATE tbl_groups SET group_name=%s, creater_id=%s WHERE id=%s",
                             (group_name, creater_id, group_id))
            cnx.commit()

            return redirect(url_for('manage_groups'))

    except Exception as e:
        # Handle exceptions, print or log the error for debugging
        print(f"Error updating group: {e}")
        cnx.rollback()
        # Optionally, you can redirect to an error page or display an error message
        return "Error updating group. Please try again."

    finally:
        mycursor.close()
        cnx.close()

    return render_template('update_group.html', group=group)

@app.route('/delete_group/<int:group_id>')
def delete_group(group_id):
    cnx = mysql.connector.connect(**config)
    mycursor = cnx.cursor()

    # Delete associated records in the files table
    mycursor.execute("DELETE FROM files WHERE group_id = %s", (group_id,))
    cnx.commit()

    # Now, you can safely delete the group
    mycursor.execute("DELETE FROM tbl_groups WHERE id = %s", (group_id,))
    cnx.commit()

    return redirect(url_for('manage_groups'))

# -----------------END GROUP MANAGEMENT-----------------------


# ------------------ Train Request -------------------------

@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        # Establish a connection to the MySQL database
        cnx = mysql.connector.connect(**config)
        mycursor = cnx.cursor(buffered=True)

        # Check if the user already exists
        check_query = "SELECT id FROM users WHERE email = %s"
        mycursor.execute(check_query, (email,))
        existing_user = mycursor.fetchone()

        if existing_user:
            mycursor.close()
            cnx.close()
            return render_template('user_exists.html')

        # Insert a new user into the 'users' table
        insert_query = "INSERT INTO users (first_name, last_name, email, completed_training) VALUES (%s, %s, %s, %s)"
        values = (first_name, last_name, email, 0)
        mycursor.execute(insert_query, values)

        cnx.commit()
        mycursor.close()
        cnx.close()

        return render_template('request_submitted.html')

    return render_template('student_dashboard.html')


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        student_id = request.form['student_id']
        decision = request.form['decision']

        # Establish a connection to the MySQL database
        cnx = mysql.connector.connect(**config)
        mycursor = cnx.cursor(buffered=True)

        # Update the 'completed_training' field based on the decision
        update_query = "UPDATE users SET completed_training = %s WHERE id = %s"
        values = (1 if decision == 'approve' else 0, student_id)
        mycursor.execute(update_query, values)

        cnx.commit()
        mycursor.close()
        cnx.close()

    # Fetch and display pending face change requests
    cnx = mysql.connector.connect(**config)
    mycursor = cnx.cursor(buffered=True)

    pending_query = "SELECT id, first_name, last_name, email FROM users WHERE completed_training = 0"
    mycursor.execute(pending_query)
    pending_requests = mycursor.fetchall()

    mycursor.close()
    cnx.close()

    return render_template('admin_dashboard.html', pending_requests=pending_requests)

# -------------------- END TRAIN REQ ----------------

def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


@socketio.on("connect")
def test_connect():
    print("Connected")
    emit("my response", {"data": "Connected"})

def process_image_and_emit(image):
    # Process the image
    processed_image = face_recognition_socket(image)

    # Emit the processed image to clients
    emit("processed_image", processed_image)


@socketio.on("image")
def receive_image(image):
    # Decode the base64-encoded image data
    global last_processed_time

    image = base64_to_image(image)

    Thread(target=process_image_and_emit, args=(image,)).start()

    image = face_recognition_socket(image)
    if time.time() - last_processed_time >= 0.1:
        image = base64_to_image(image)
        Thread(target=process_image_and_emit, args=(image,)).start()
        last_processed_time = time.time()
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    frame_resized = image #cv2.resize(gray, (640, 360))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)

    processed_img_data = base64.b64encode(frame_encoded).decode()

    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data

    emit("processed_image", processed_img_data)




@socketio.on("trainimage")
def receive_trainimage(image):
    # Decode the base64-encoded image data
    image = base64_to_image(image)

    image = generate_dataset_socket(image)


    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    frame_resized = image #cv2.resize(gray, (640, 360))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)

    processed_img_data = base64.b64encode(frame_encoded).decode()

    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data

    emit("processed_trainimage", processed_img_data)



if __name__ == "__main__":
    #app.run()
    #app.run(host='127.0.0.1', port=5000, debug=True)
    socketio.run(app, port=20449, debug=True, allow_unsafe_werkzeug=True)

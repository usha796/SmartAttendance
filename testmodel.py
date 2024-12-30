# import cv2 
# # from controller import doorAutomate
# # import time

# video=cv2.VideoCapture(0)


# facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.read("Trainer.yml")

# name_list = ["", "Nilam"]

# imgBackground = cv2.imread("background.jpg")

# while True:
#     ret,frame=video.read()
#     gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = facedetect.detectMultiScale(gray, 1.3, 5)
#     for (x,y,w,h) in faces:
#         serial, conf = recognizer.predict(gray[y:y+h, x:x+w])
#         # print("Confidence Level:", conf)  # Printing confidence level
#         if conf>50:
#             cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
#             cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
#             cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
#             cv2.putText(frame, name_list[serial], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
#         else:
#             cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
#             cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
#             cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
#             cv2.putText(frame,"UNKNOWN", (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
#     frame=cv2.resize(frame, (300, 200))
#     imgBackground[150:150 + 200, 25:25 + 300] = frame
#     cv2.imshow("Frame",imgBackground)
    
#     k=cv2.waitKey(1)
    
#     # if k==ord('o') and conf>50:
#     #     doorAutomate(0)
#     #     time.sleep(10)
#     #     doorAutomate(1)
#     if k==ord("q"):
#         break

# video.release()
# cv2.destroyAllWindows()

# 


import cv2 
import datetime
import threading
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
attendance_recorded = set()
video = None
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Trainer.yml")
name_list = ["", "Nilam"]
imgBackground = cv2.imread("background.jpg")

def capture_video():
    global video, facedetect, recognizer, name_list, attendance_recorded
    video = cv2.VideoCapture(0)
    # if not video.isOpened():
    #  print("Error: Unable to open video capture device.") 
    while True:
        
        ret, frame = video.read()  # Read frame without checking ret

        
        # ret, frame = video.read()
        # ret, frame = video.read()
        # ret, frame = video.read()


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            serial, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf > 50:
                name = name_list[serial]
                if name not in attendance_recorded:
                    attendance_recorded.add(name)
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{name} is present. Time: {current_time}")
            else:
                name = "UNKNOWN"
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        frame = cv2.resize(frame, (300, 200))
        imgBackground[150:150 + 200, 25:25 + 300] = frame
        cv2.imshow("Frame",imgBackground)
        k = cv2.waitKey(1)
        if k == ord("q"):
            break
    video.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('attendancechart.html')

@app.route('/update_attendance', methods=['POST'])
def update_attendance():
    data = request.get_json()
    name = data['name']
    if name not in attendance_recorded:
        attendance_recorded.add(name)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{name} is present. Time: {current_time}")
        return jsonify({'status': 'success', 'message': f'Attendance recorded for {name}.'})
    else:
        return jsonify({'status': 'error', 'message': f'Attendance already recorded for {name}.'})

if __name__ == "__main__":
    t = threading.Thread(target=capture_video)
    t.start()
    app.run(debug=True)

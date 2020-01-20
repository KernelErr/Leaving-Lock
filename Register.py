import cv2
import time
import face_recognition
import numpy as np
import os
video_capture = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_DUPLEX
end_time = 0
countdown = 0
count = 0

user_path = "./users/"
user_name = "Owner"
if not os.path.exists(user_path):
    os.mkdir(user_path)

while(True):
    ret, frame = video_capture.read()
    if ret:
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame, model="cnn")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        tips = "Face"
        
        if len(face_locations) == 1:
            start_time = time.time()
            if end_time < 1:
                end_time = time.time()
            elif (start_time-end_time > 5) and (start_time-end_time <= 35):
                tips = "Registering"
                if not os.path.exists(user_path + user_name):
                    os.mkdir(user_path + user_name)
                np.save(user_path + user_name + "/" + str(count) + ".npy", face_encodings[0])
                count += 1
            elif start_time-end_time > 35:
                tips = "Done"
        else:
            end_time = time.time()
            tips = "Face"

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, tips, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
    cv2.putText(frame, "Single person facing this screen for 35s to register.", (20, 40), font, 0.6, (0, 255, 255), 2)
    cv2.imshow('Registering Face...', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
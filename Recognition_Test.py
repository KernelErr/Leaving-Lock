import face_recognition
import cv2
import numpy as np
import os
import time
import pyautogui


video_capture = cv2.VideoCapture(0)


known_face_encodings = [
]
user_path = "./users/"
user_name = "Owner"
saved_encodings = os.listdir(user_path + user_name + "/")

for file in saved_encodings:
    file = user_path + user_name + "/" + file
    known_face_encodings.append(np.load(file))

while True:
    ret, frame = video_capture.read()

    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame, model="cnn")
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        face_distances = list(face_distances <= 0.3)
        if True in face_distances:
            name = user_name

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
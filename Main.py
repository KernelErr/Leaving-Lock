import face_recognition
import cv2
import numpy as np
import os
import time
end_time = 0

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
    known_here = False

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
        
        if (not known_here) and (name == user_name):
            known_here = True

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    if known_here:
        cv2.putText(frame, "Safe", (20, 40), font, 0.6, (0, 255, 255), 2)
        end_time = time.time()
    else:
        start_time = time.time()
        cv2.putText(frame, "Warning", (20, 40), font, 0.6, (0, 255, 255), 2)
        if end_time < 1:
            end_time = time.time()
        elif start_time-end_time > 10:
            os.system("rundll32.exe user32.dll LockWorkStation")
            end_time = time.time()

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
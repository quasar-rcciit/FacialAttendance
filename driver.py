import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from PIL import Image
import urllib.request
import requests
import internet_ping
import attendance


ping = internet_ping.is_connected()

if ping == True:
    pass
else:
    print("Internet connection not found! Please connect to internet")
    exit()

jsondata = attendance.jsondata

mylist = jsondata
path = "ImageAttendance"
attendance.download(mylist)
images = []
classNames = []
mylist = os.listdir(path)
print(mylist)
for cl in mylist:
    currImg = cv2.imread(f"{path}/{cl}")
    images.append(currImg)
    classNames.append(os.path.splitext(cl)[0])
    # print(currImg)
    # print(images)
    # print(classNames)
    # exit()

print(classNames)

encodeListKnown = attendance.findEncodings(images)
print("Encoding complete!")
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, facesCurrFrame)

    for encodeFace, faceLoc in zip(encodeCurrFrame, facesCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 35), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 35), cv2.FILLED)
            cv2.putText(
                img,
                name,
                (x1 + 16, y2 - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )
            attendance.markAttendance(name)
    cv2.imshow("Webcam", img)
    cv2.waitKey(1)

# faceLoc = face_recognition.face_locations(imgElon)[0]
# encodeElon = face_recognition.face_encodings(imgElon)[0]
# cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
#
# faceLocTest = face_recognition.face_locations(imgTest)[0]
# encodeElonTest = face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
#
# results = face_recognition.compare_faces([encodeElon],encodeElonTest)
# faceDis = face_recognition.face_distance([encodeElon],encodeElonTest)

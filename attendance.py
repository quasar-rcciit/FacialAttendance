import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from PIL import Image
import urllib.request
import requests
jsondata = [{
    "imagepath": "https://static.dezeen.com/uploads/2021/06/elon-musk-architect_dezeen_1704_col_1.jpg",
    "imagename": "Elon Mask",

},{
    "imagepath": "https://content.fortune.com/wp-content/uploads/2020/09/CNV.10.20.FORTUNE_BILL_AND_MELINDA_GATES_030-vertical.jpg",
    "imagename": "Bill gates",

},{
    "imagepath": "https://media.wired.com/photos/5cd03fc84ef5ad318eea3885/master/w_2560%2Cc_limit/microsoft-3590.jpg",
    "imagename": "Satya Nadella",

}]
# path = "E:\pics"
mylist = jsondata
path = "ImageAttendance"
for cl in mylist:
    currImg = cl["imagepath"]
    # setting filename and image URL
    i = 0
    filename = str(i)
    image_url = cl["imagepath"]
    im = Image.open(requests.get(image_url, stream=True).raw)
    im.save("E:\code\\" + "FacialAttendance\ImageAttendance\p" + cl["imagename"] + ".jpg")
    i = i + 1
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


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    with open("Attendance.csv", "r+") as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(",")
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            tmString = now.strftime("%H:%M:%S")
            dtString = now.strftime("%d/%m/%Y")
            f.writelines(f"\n{name},{tmString},{dtString}")

        print(myDataList)


encodeListKnown = findEncodings(images)
print("Encoding Complete")
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
            markAttendance(name)
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

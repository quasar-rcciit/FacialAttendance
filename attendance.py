import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from PIL import Image
import urllib.request
import requests
import internet_ping


jsondata = [
    {
        "imagepath": "https://static.dezeen.com/uploads/2021/06/elon-musk-architect_dezeen_1704_col_1.jpg",
        "imagename": "Elon Mask",
    },
    {
        "imagepath": "https://content.fortune.com/wp-content/uploads/2020/09/CNV.10.20.FORTUNE_BILL_AND_MELINDA_GATES_030-vertical.jpg",
        "imagename": "Bill gates",
    },
    {
        "imagepath": "https://media.wired.com/photos/5cd03fc84ef5ad318eea3885/master/w_2560%2Cc_limit/microsoft-3590.jpg",
        "imagename": "Satya Nadella",
    },
]


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


def download(mylist):
    for cl in mylist:
        currImg = cl["imagepath"]
    # setting filename and image URL
    i = 0
    filename = str(i)
    image_url = cl["imagepath"]
    im = Image.open(requests.get(image_url, stream=True).raw)
    im.save(
        "E:\code\\" + "FacialAttendance\ImageAttendance\p" + cl["imagename"] + ".jpg"
    )
    i = i + 1

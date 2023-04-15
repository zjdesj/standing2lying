import os
import pandas as pd
import numpy as np
import cv2
import re
import time
from ultralytics import YOLO
dpath = '/content/s2l/standing2lying/results/D4'
# os.chdir('/content/drive/MyDrive/bi-seq-202302/standing2lying')


def getFiles(dir):
    files = os.listdir(dir)
    files = [file for file in files if os.path.splitext(file)[1] == '.csv']
    return files


fs = sorted(getFiles(dpath))

print(fs)

v8model = YOLO('/content/s2l/standing2lying/weight/best.pt')


def getName(name):
    print('name', name)
    m = re.match(r'(D\d{2}_\d{14})', name)
    return m.group(1)


def saveRet(data, name):
    print('saved file\'s name:', name)
    df = pd.DataFrame(data)
    df.to_csv(name)


def getFrame(num, cap):
    print('--当前帧---', num)
    cap.set(cv2.CAP_PROP_POS_FRAMES, num - 1)
    ret_val, img0 = cap.read()
    return img0


def saveImg(name, img):
    path = '/content/drive/MyDrive/bi-seq-202302/standing2lying/yolo/tt/' + name
    cv2.imwrite(path, img)


for f in fs:
    ret = []
    df = pd.read_csv(os.path.join(dpath, f), sep=',')
    val = df.values
    frames = val[:, 1]
    mname = getName(f)
    cap = cv2.VideoCapture(os.path.join('/content/videos/', mname + '.mp4'))
    for frame in frames:
        #img = getFrame(frame, cap)
        name = mname + '-' + str(frame) + '.jpg'
        img = getFrame(frame, cap)
        #saveImg(name, img)
        [results] = v8model(img)
        rr = results.boxes
        cls = -1
        con = -1
        if len(rr.cls):
            cls = int(rr.cls[0].item())
            con = rr.conf[0].item()
            tmp = [frame, len(rr.boxes), cls, con, rr.cls.tolist()]
        ret.append(tmp)

    saveRet(ret, '/content/s2l/standing2lying/results/DD4/' + mname + '.csv')

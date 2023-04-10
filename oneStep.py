import sys
import os
import pandas as pd
import cv2
import numpy as np
import time

from crop import get_crop
from loadModel import getV8, loadResnet
from getFrames import getFrame
from keras.utils import img_to_array


def getVideo(videoPath):
    cap = cv2.VideoCapture(videoPath)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('--- start: video 信息：')
    print('fps = ', fps)
    print('frames = ', frames)
    print('--- end: video 信息：')
    return [cap, frames]


def img2Array(img):
    if len(img):
        #img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #img2 = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
        img2 = cv2.resize(img, (224, 224), interpolation=cv2.INTER_NEAREST)

        x = img_to_array(img2)
        #x = np.expand_dims(img2, axis=2).repeat(3, axis=2)
        x = np.expand_dims(x, axis=0)
        return x
    return []


def getImgArray(v8model, img):
    img0 = get_crop(v8model, img)

    return img2Array(img0)


def saveRet(data, videoPath):
    name = os.path.splitext(videoPath)[0]
    name = os.path.split(name)[1] + '_' + str(time.time()) + '.csv'
    print('saved file\'s name:', name)
    cols = ['ind']
    cols = cols + ['time']
    df = pd.DataFrame(data, columns=cols)
    df.to_csv(
        '/content/drive/MyDrive/bi-seq-202302/standing2lying/result-one/' + name)


def getModelInstances(confs):
    for conf in confs:
        print(conf["yolo"], conf["resnet"])
        conf["yolo"] = getV8(conf["yolo"])
        conf["resnet"] = loadResnet(conf["resnet"])
    return confs


def processVideoKeyFrames(videoPath, frames, framesDir):
    v8model = getV8()

    [cap, frameNum] = getVideo(videoPath)

    time0 = time.time()

    ret = []

    for frame in frames:
        item = [frame]
        start_time = time.time()

        getFrame(v8model, frame, cap, videoPath, framesDir)

        end_time = time.time()
        item.append(end_time - start_time)
        ret.append(item)

    time1 = time.time()
    print("总耗时: {:.2f}秒".format(time1 - time0))

    saveRet(ret, videoPath)
    return frameNum

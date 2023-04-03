#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__FREQUENCY__ = 7

import sys
import os
import pandas as pd
import cv2
import numpy as np
import time
import yaml

from crop import get_crop
from loadModel import getV8, loadResnet
from getFrames import getFrame
from keras.utils import img_to_array


def getConfs():
    with open('./conf.yaml', 'r') as f:
        confs = yaml.load(f, Loader=yaml.FullLoader)

    return confs["confs"]


def getVideo(videoPath):
    cap = cv2.VideoCapture(videoPath)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('--- start: video 信息：')
    print('fps = ', fps)
    print('frames = ', frames)
    print('--- end: video 信息：')
    return cap


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


def resnetPredict(model, x):
    if len(x) == 0:
        return [[], -1]

    item = []
    preds = model.predict(x)

    [[a, b]] = preds
    item.append([a, b])

    if a > b:
        item.append(0)
    else:
        item.append(1)
    return item


def saveRet(data, videoPath):
    confs = getConfs()
    name = os.path.splitext(videoPath)[0]
    name = os.path.split(name)[1] + '_' + str(time.time()) + '.csv'
    print('saved file\'s name:', name)
    cols = ['ind']
    for item in confs:
        cols = cols + [item["name"], item["name"] + '_val']
    cols = cols + ['time']
    df = pd.DataFrame(data, columns=cols)
    df.to_csv(
        '/content/drive/MyDrive/bi-seq-202302/standing2lying/results-test/' + name)


def getModelInstances(confs):
    for conf in confs:
        print(conf["yolo"], conf["resnet"])
        conf["yolo"] = getV8(conf["yolo"])
        conf["resnet"] = loadResnet(conf["resnet"])
    print(confs)
    return confs


def processVideo(videoPath):
    confs = getConfs()
    modelsArr = getModelInstances(confs)
    #v8model = getV8()
    #resnetModel = loadResnet()

    cap = getVideo(videoPath)

    ret_val, img0 = cap.read()

    count = 0
    time0 = time.time()

    ret = []

    while ret_val:
        start_time = time.time()
        count += 1

        if count % __FREQUENCY__ != 0:
            ret_val, img0 = cap.read()
            continue

        print(count)

        item = [count]

        tmp = []
        for models in modelsArr:
            v8model = models["yolo"]
            resnetModel = models["resnet"]

            imgArray = getImgArray(v8model, img0)

            [[pred], pose] = resnetPredict(resnetModel, imgArray)
            tmp.append(pred, pose)

        item = item + tmp
        ret_val, img0 = cap.read()
        end_time = time.time()
        item.append(end_time - start_time)
        ret.append(item)

    time1 = time.time()
    print("总耗时: {:.2f}秒".format(time1 - time0))
    print(count)

    saveRet(ret, videoPath)


def processVideoKeyFrames(videoPath, frames, framesDir):
    confs = getConfs()
    modelsArr = getModelInstances(confs)
    #resnetModel = loadResnet()

    cap = getVideo(videoPath)
    time0 = time.time()

    ret = []

    for frame in frames:
        item = [frame]
        start_time = time.time()

        tmp = []
        for models in modelsArr:
            v8model = models["yolo"]
            resnetModel = models["resnet"]
            imgArray = img2Array(
                getFrame(v8model, frame, cap, videoPath, framesDir))
            predictRet = resnetPredict(resnetModel, imgArray)
            tmp = tmp + predictRet
        item = item + tmp
        end_time = time.time()
        item.append(end_time - start_time)
        ret.append(item)

    time1 = time.time()
    print("总耗时: {:.2f}秒".format(time1 - time0))

    saveRet(ret, videoPath)


if __name__ == '__main__':
    #video_path = '/content/drive/MyDrive/bi-seq-202302/videos/D01_20210519140930.mp4'
    #video_path = '/content/drive/MyDrive/bi-seq-202302/videos/316videos/D01_20210519190605.mp4'
    #short_path = '/content/drive/MyDrive/bi-seq-202302/videos/short.mp4'
    #print('在这使用path', video_path)

    # processVideo(video_path)
    confs = getConfs()
    getModelInstances(confs)

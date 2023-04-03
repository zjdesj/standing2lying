#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pandas as pd
import cv2
import time
import numpy as np
from keras.utils import load_img, img_to_array

from loadModel import loadResnet, getV8
from crop import get_crop

__frameStrategy__ = 7
__resnetPath__ = ''


def getCap(videoPath):
    cap = cv2.VideoCapture(videoPath)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('--- start: video 信息：')
    ret_val, img0 = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    print(frames, fps)
    print('--- end: video 信息：')
    return cap


def getInference(videoPath, savePath, isGray=False):

    v8model = getV8()
    resnetModel = loadResnet()

    cap = getCap(videoPath)

    count = 0
    time0 = time.time()

    ret = []

    while ret_val:
        start_time = time.time()

        count += 1

        if count % __frameStrategy__ != 0:  # 固定帧取一帧
            ret_val, img0 = cap.read()
            continue

        img01 = get_crop(img0)
        item = [count]
        if len(img01):
            if isGray:
                img01 = cv2.cvtColor(img01, cv2.COLOR_BGR2GRAY)
            img1 = cv2.resize(img01, (224, 224), interpolation=cv2.INTER_AREA)

            x = img_to_array(img1)
            print(x.shape)
            x = np.expand_dims(x, axis=0)
            print(x.shape)
            preds = resnetModel.predict(x)

            [[a, b]] = preds
            item.append(preds)
            if a > b:
                item.append(0)
            else:
                item.append(1)

        else:
            item.append([])
            item.append(-1)
        ret_val, img0 = cap.read()
        end_time = time.time()
        item.append(end_time - start_time)
        ret.append(item)
    time1 = time.time()
    print("总耗时: {:.2f}秒".format(time1 - time0))
    print(count)

    df = pd.DataFrame(ret, columns=['ind', 'preds', 'results', 'time'])
    df.to_csv(savePath)


if __name__ == '__main__':
    args = sys.argv
    print(args)

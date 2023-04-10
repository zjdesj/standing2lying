import sys
import os
import pandas as pd
import cv2
import numpy as np
import time

from crop import get_crop
from loadModel import getV8


def getVideo(videoPath):
    cap = cv2.VideoCapture(videoPath)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('--- start: video 信息：')
    print('fps = ', fps)
    print('frames = ', frames)
    print('--- end: video 信息：')
    return [cap, frames]


def saveRet(data, videoPath):
    name = os.path.splitext(videoPath)[0]
    name = os.path.split(name)[1] + '_' + str(time.time()) + '.csv'
    print('saved file\'s name:', name)
    cols = ['ind']
    cols = cols + ['time']
    df = pd.DataFrame(data, columns=cols)
    df.to_csv(
        './results/' + name)


def getFrame(v8model, num, cap):
    print('--当前帧---', num)
    cap.set(cv2.CAP_PROP_POS_FRAMES, num)
    ret_val, img0 = cap.read()
    return img0


def processVideoKeyFramesByOne(videoPath, frames, framesDir):
    v8model = getV8()

    [cap, frameNum] = getVideo(videoPath)

    time0 = time.time()

    ret = []

    for frame in frames:
        item = [frame]
        start_time = time.time()

        img = getFrame(v8model, frame, cap)
        [v8ret] = v8model(img)
        print(v8ret.boxes)
        print(v8ret.probs)

        end_time = time.time()
        item.append(end_time - start_time)
        ret.append(item)

    time1 = time.time()
    print("总耗时: {:.2f}秒".format(time1 - time0))

    saveRet(ret, videoPath)
    return frameNum

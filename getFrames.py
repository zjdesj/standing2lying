#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import cv2
import pandas as pd
from crop import get_crop
from loadModel import getV8

v8model = getV8()

# 从视频获取单帧


def getFrame(num, cap, video_path='', framesDir=''):
    print('--当前帧---', num)
    cap.set(cv2.CAP_PROP_POS_FRAMES, num)
    ret_val, img0 = cap.read()

    #img0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

    #img01 = get_crop(v8model, img0, True)
    img01 = get_crop(v8model, img0, video_path, num, framesDir, True)
    print('--当前帧结束--', num)
    return img01

# 从单视频获取多帧


def getBatchFramesFromSingleVideo(arr, video_path, framesDir='/content/drive/MyDrive/bi-seq-202302/standing2lying/frames-2'):
    print(video_path, arr)
    cap = cv2.VideoCapture(video_path)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('--- start: video 信息：')
    print('videopath', video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('fps = ', fps)
    print('frames = ', frames)
    print('--- end: video 信息：')
    for item in arr:
        if item >= frames:
            return
        img = getFrame(item, cap, video_path, framesDir)

# 从多视频获取多帧


def getBatchFramesFromVideos(videoArr):
    for item in videoArr:
        frames = item['frames']
        video_path = item['video_path']
        getBatchFramesFromSingleVideo(frames, video_path)


def getBatchFramesFromVideosInCsv(data):
    for item in data:
        #frames = [int(x) for x in item[1:] if int(x) > 0]
        frames = [int(x) for x in item[1:] if x == x and x != '\t']
        video_path = item[0]
        getBatchFramesFromSingleVideo(frames, video_path)


def readData(csvPath):
    df = pd.read_csv(csvPath, sep=',', header=None)
    return df.values
# 使用举例


if __name__ == '__main__':
    #video_path = '/content/drive/MyDrive/bi-seq-202302/videos/transferedVideos/D01_20210520120026.mp4'
    #short_path = '/content/drive/MyDrive/bi-seq-202302/videos/short.mp4'
    # getBatchFramesFromVideos([
    #    {"frames": [119], "video_path": short_path},
    #    {"frames": [200], "video_path": short_path}])

    #csvPath = './frames.csv'
    csvPath = sys.argv[1]
    data = readData(csvPath)
    getBatchFramesFromVideosInCsv(data)

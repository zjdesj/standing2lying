import sys
import os
import pandas as pd
import cv2
import numpy as np
import time

from crop import get_crop
from loadModel import getV8

from extractKeyFrames import KeyFrameGetter


def getVideo(videoPath):
    cap = cv2.VideoCapture(videoPath)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('--- start: video 信息：')
    print('fps = ', fps)
    print('frames = ', frames)
    print('--- end: video 信息：')
    return frames


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

        [v8ret] = v8model(img, save=True, save_txt=True, save_conf=True)
        #print('v8ret.boxes::', v8ret.boxes)
        print('v8ret.probs::', v8ret.classes)

        end_time = time.time()
        item.append(end_time - start_time)
        ret.append(item)

    time1 = time.time()
    print("总耗时: {:.2f}秒".format(time1 - time0))

    saveRet(ret, videoPath)
    return frameNum


def saveRet(data, videoPath, retDir):
    name = os.path.splitext(videoPath)[0]
    name = os.path.split(name)[1] + '_' + str(time.time()) + '.csv'
    df = pd.DataFrame(data)
    saveFileName = os.path.join(retDir, name)
    print('saved file\'s name:', saveFileName)
    df.to_csv(saveFileName)


def processVideoByKeyFrames(video_path, retDir, frames, dir_path):
    a = time.time()
    v8model = getV8()
    ret = []

    cap = cv2.VideoCapture(video_path)

    for frame in frames:
        print('frame no:', frame)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame - 1)
        ret_val, img = cap.read()
        # 可存储
        # if ret_val:
        #    path = os.path.join(dir_path, str(frame) + '.jpg')
        #    cv2.imwrite(path, img)

        [results] = v8model(img)

        rr = results.boxes
        cls = -1
        con = -1
        if len(rr.cls):
            cls = int(rr.cls[0].item())
            con = rr.conf[0].item()
        tmp = [frame, len(rr.boxes), cls, con, rr.cls.tolist()]

        ret.append(tmp)
    saveRet(ret, video_path, retDir)
    b = time.time()
    print("总耗时: {:.2f}秒".format(b - a))


def processVideoByKeyFramesDir(framesDir, retDir, v8model):
    a = time.time()
    ret = []
    frames = os.listdir(framesDir)

    for frame in frames:
        print('frame no:', frame)
        path = os.path.join(framesDir, frame)
        [results] = v8model(path)

        rr = results.boxes
        cls = -1
        con = -1
        if len(rr.cls):
            cls = int(rr.cls[0].item())
            con = rr.conf[0].item()
        tmp = [frame, len(rr.boxes), cls, con, rr.cls.tolist()]

        ret.append(tmp)
    saveRet(ret, framesDir, retDir)
    b = time.time()
    print("总耗时: {:.2f}秒".format(b - a))


def processVideo(video_path, retDir, filename):
    a = time.time()
    v8model = getV8()
    ret = []

    results = v8model(video_path, stream=True)
    for r in results:
        rr = r.boxes
        cls = -1
        con = -1
        if len(rr.cls):
            cls = int(rr.cls[0].item())
            con = rr.conf[0].item()
        tmp = [len(rr.boxes), cls, con, rr.cls.tolist()]
        ret.append(tmp)

    saveRet(ret, video_path, retDir)

    b = time.time()
    print("总耗时: {:.2f}秒".format(b - a))


def processVideos(videoDir, framesDir, retDir):
    framesArr = []
    ret = []
    for root, dirs, files in os.walk(videoDir):
        for file in sorted(files):
            source_path = os.path.join(root, file)
            filename = os.path.splitext(file)[0]
            dir_path = framesDir + filename  # + '/'

            print("源文件目录为", root)
            print("源文件路径为", source_path)
            print("目的文件路径为", dir_path)

            if os.path.exists(dir_path):
                continue
                #os.rename(dir_path, dir_path + '.bak.' + str(time.time()))
            os.makedirs(dir_path)

            arr = getKeyFrames(source_path, dir_path)
            keyFrames = fuseLastFrame(arr, source_path)
            print('keyFrames :', keyFrames)

            #processVideo(source_path, retDir, filename)
            processVideoByKeyFrames(source_path, retDir, keyFrames, dir_path)


def getKeyFrames(source_path, dir_path):
    kfg = KeyFrameGetter(source_path, dir_path, 100)
    a = time.time()
    kfg.load_diff_between_frm(alpha=0.07)  # 获取模型参数
    print(kfg.idx)
    return kfg.idx


def fuseLastFrame(arr, videoPath):
    frames = getVideo(videoPath)

    if arr[-1] < frames:
        arr.append(frames)
    return arr


def precessKeyFrames(framesDir, retDir):
    v8model = getV8()
    print('os.listdir(framesDir)', os.listdir(framesDir))
    for dir in os.listdir(framesDir):
        processVideoByKeyFramesDir(
            os.path.join(framesDir, dir), retDir, v8model)


if __name__ == '__main__':
    videoDir = sys.argv[1]
    types = sys.argv[2]
    # 需要确定的地址
    #videoDir = '/content/drive/MyDrive/bi-seq-202302/videos/316videos/me'
    #videoDir = './video'
    framesDir = './img/'
    retDir = './results/DD03-23'
    if types == 'key':
        precessKeyFrames(videoDir, retDir)
    else:
        processVideos(videoDir, framesDir, retDir)

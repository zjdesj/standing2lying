import sys
import os
import cv2
import pandas as pd


def getVideoFrames(videoDir):
    ret = []
    files = os.listdir(videoDir)
    for file in files:
        cap = cv2.VideoCapture(os.path.join(videoDir, file))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        ret.append({"name": file, "frames": frames})
        print('--- start: video 信息：')
        print('videopath', file)
        print('frames = ', frames)
        print('--- end: video 信息：')
    print(ret)
    return ret


def saveRet(data, dir):
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(dir, 'videoFrames.csv'))


if __name__ == '__main__':

    videoDir = sys.argv[1]
    # 需要确定的地址
    #videoDir = '/content/drive/MyDrive/bi-seq-202302/videos/316videos/me'
    #videoDir = '/content/video'
    dir = '/content/drive/MyDrive/bi-seq-202302/standing2lying/'
    data = getVideoFrames(videoDir)
    saveRet(data, dir)

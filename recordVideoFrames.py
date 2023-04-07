import sys
import os
import cv2


def getVideoFrames(videoDir, dir):
    ret = []
    files = os.listDir(videoDir)
    for file in files:
        cap = cv2.VideoCapture(file)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        ret.append({"name": file, "frames": frames})
        print('--- start: video 信息：')
        print('videopath', file)
        print('frames = ', frames)
        print('--- end: video 信息：')
    print(ret)


if __name__ == '__main__':

    videoDir = sys.argv[1]
    # 需要确定的地址
    #videoDir = '/content/drive/MyDrive/bi-seq-202302/videos/316videos/me'
    #videoDir = '/content/video'
    dir = '/content/drive/MyDrive/bi-seq-202302/standing2lying/'
    getVideoFrames(videoDir, dir)

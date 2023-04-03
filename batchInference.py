
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import time
from twoSteps import processVideo


def getName(path, type):
    name = os.path.splitext(path)[0]
    name = os.path.split(name)[1] + '_' + str(time.time()) + type
    return name


def getBatchRets(path):
    print('sss', os.listdir(path))
    files = [x for x in os.listdir(path) if os.path.splitext(x)[1] == '.mp4']
    print(files)

    for file in files:
        print(os.path.join(path, file))
        #logFile = getName(file, '.log')
        processVideo(os.path.join(path, file))


if __name__ == '__main__':
    path = '/content/drive/MyDrive/bi-seq-202302/videos/316videos/'
    print('14在这使用path', path)
    getBatchRets(path)

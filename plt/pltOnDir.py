import re
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

modelNames = ['', '330_69', '330_57', '330_65', '324_69', '324_57', '324_65']


def groupByDay(files):
    ret = {}

    for file in files:
        m = re.match(r'(D\d{2})_\d{4}(\d{10})', file)
        day = m.group(1)
        time = m.group(2)
        if not day in ret.keys():
            ret[day] = []

        ret[day].append({"name": file, "time": time})

    return ret


def insertFrames(data):
    pointer = 0
    ret = []
    # max = 71400 #临时设置
    for item in data:
        if pointer > item[0]:
            pointer = 0
        while pointer <= item[0]:
            tmp = [pointer]
            for val in item[1:]:
                tmp.append(val)

            ret.append(tmp)
            pointer += 1
    print(ret[1:5])
    print('ret length:', len(ret))
    return ret


def stitch(day, item):
    ret = []
    for piece in day:
        df = pd.read_csv(piece['name'], sep=',')
        val = df.values
        predictionsOnKeyFrames = val[:, 1:14:2]
        ret.extend(predictionsOnKeyFrames)
    print(np.shape(ret))
    print(ret[0])
    ret = insertFrames(ret)
    data = np.transpose(ret)
    print('拼接后的数据：', len(ret))

    df = pd.DataFrame(ret, columns=modelNames)
    df.to_csv('./stitch_' + item + '.csv')

    return data


def plotImg(imgPath, data, ind):
    print('imagePath: ', imgPath)
    plt.figure(figsize=(60, 3))

    plt.xlabel('key_frames')
    plt.ylabel('status')
    # plt.title(csvFile)
    plt.plot(data[ind], 'bo',)
    plt.savefig(imgPath)
    plt.show()


def getImgName(file):
    pureFileName = os.path.split(file)[1]
    name = os.path.splitext(pureFileName)[0]
    return name + '.png'


def stitchAll(ret):
    for item in ret.keys():
        dayArr = ret[item]
        dayArr.sort(key=lambda s: int(s["time"]))
        print('dayArr: ', dayArr)
        dayFrames = stitch(dayArr, item)
        for ind in list(range(1, 7)):
            path = '/content/drive/MyDrive/bi-seq-202302/standing2lying/results-final/' + \
                item + '_' + modelNames[ind] + '.png'
            plotImg(path, dayFrames, ind),


def getFiles(dir):
    files = os.listdir(dir)
    files = [file for file in files if os.path.splitext(file)[1] == '.csv']
    return files


if __name__ == '__main__':

    csvDir = sys.argv[1]
    files = getFiles(csvDir)
    ret = stitchAll(groupByDay(files))

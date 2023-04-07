import os

from shutil import copyfile


def getFiles(dir):
    files = os.listdir(dir)
    files = [file for file in files if os.path.splitext(file)[1] == '.csv']
    return files


files = getFiles(
    '/content/drive/MyDrive/bi-seq-202302/standing2lying/result-final/')


D1 = ["D01_20210520070305", "D01_20210520075225", "D01_20210520084143", "D01_20210520102108", "D01_20210520111043", "D01_20210520093131", "D01_20210520012728", "D01_20210520003946", "D01_20210520030230", "D01_20210520043724", "D01_20210520034954", "D01_20210520052436", "D01_20210520061326", "D01_20210520021502", "D01_20210519181707",
      "D01_20210519195401", "D01_20210519204133", "D01_20210519212904", "D01_20210519221635", "D01_20210519230415", "D01_20210519235151", "D01_20210519190605", "D01_20210519123012", "D01_20210519131958", "D01_20210519115715", "D01_20210519140930", "D01_20210519145854", "D01_20210519154835", "D01_20210519163805", "D01_20210519172725", ]


def moveData(day=D1, name='D1'):
    sortedDay = sorted(day)
    print(sortedDay)
    D1Path = '/content/drive/MyDrive/bi-seq-202302/standing2lying/result-final/' + name
    os.makedirs(D1Path)

    for dir in day:
        for file in files:
            if dir in file:
                copyfile(file, os.path.join(D1Path, file))
                break


moveData()

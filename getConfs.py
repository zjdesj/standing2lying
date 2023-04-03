import yaml
from loadModel import getV8, loadResnet


def getConfs():
    with open('./conf.yaml', 'r') as f:
        confs = yaml.load(f, Loader=yaml.FullLoader)

    return confs


def getModelInstances(confs):
    arr = confs["confs"]
    for conf in arr:
        print(conf["yolo"], conf["resnet"])
        conf["yolo"] = getV8(conf["yolo"])
        conf["resnet"] = loadResnet(conf["resnet"])
    print(arr)


confs = getConfs()
getModelInstances(confs)

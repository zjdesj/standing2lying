#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ultralytics import YOLO

# 加载基础权重
model = YOLO('yolov8n.pt')


def train(dataPath):
    # 训练文件
    model.train(data=dataPath, batch=48, epochs=300)
    #model.train(data=dataPath, batch=32, epochs=300, check_resume=True)


def val():
    model.val()


if __name__ == '__main__':
    train('./data/data.yaml')

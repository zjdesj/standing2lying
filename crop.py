# 输入img 获取截图的流
import os
import cv2

# def get_crop(ret):


def get_crop(v8model, img, video_path='', frame=0, framesDir='/content/drive/MyDrive/bi-seq-202302/standing2lying/frames', save=False, modelCombinationName=''):
    try:
        [ret] = v8model(img, conf=0.5)
        #[ret] = v8model(img, conf=0.6, max_det=1, save=True)
        print('获取的预测牛数量', len(ret.boxes))

        i = 0
        inx = 0
        area = 0

        for box in ret.boxes:
            w = int(box.xywh[0][2])
            h = int(box.xywh[0][3])
            print('i = ', i, ', w * h =', w, h, w * h)
            if w * h > area:
                area = w * h
                inx = i
            i = i + 1

        print('最终使用牛的为：', inx)
        tar = ret.boxes[inx]
        w1 = int(tar.xywh[0][2])
        h1 = int(tar.xywh[0][3])
        x1 = int(tar.xyxy[0][0])
        y1 = int(tar.xyxy[0][1])
        crop_img = img[y1: y1 + h1, x1: x1 + w1]
        if save:
            filename = os.path.split(video_path)[1].strip('.mp4')
            #print('filename :', filename)
            path = os.path.join(framesDir, filename +
                                '-' + str(frame) + '-' + str(inx) + '-' + modelCombinationName + '.jpg')
            print('dir path: ', path)
            # pathFullImg = os.path.join(framesDir, filename +
            #                           '-' + str(frame) + '.jpg')
            #cv2.imwrite(pathFullImg, img)
            cv2.imwrite(path, crop_img)
        return crop_img
    except:
        print('出错了：', video_path, frame)
        return []


if __name__ == '__main__':
    get_crop()

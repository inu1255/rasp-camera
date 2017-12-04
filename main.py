#!/usr/bin/env python
# coding=utf-8

import cv2
from camera import Camera

camera = cv2.VideoCapture(0) # 参数0表示第一个摄像头
# 判断视频是否打开
if (camera.isOpened()):
    print('Open')
else:
    print('摄像头未打开')

ca = Camera(camera)
ca.run()

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()
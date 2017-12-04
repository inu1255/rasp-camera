#!/usr/bin/env python
# coding=utf-8

import os
import time
import numpy as np
import cv2.cv as cv
import cv2

class Camera(object):
    def __init__(self, camera, image_path="images"):
        # 判断视频是否打开
        if not camera.isOpened():
            print "摄像头未打开"
            exit(1)

        self.image_path = image_path
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)
        self.camera = camera
        self.fps = camera.get(cv2.cv.CV_CAP_PROP_FPS) 
        self.size = (int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))) 
        print('fps:'+repr(self.fps)+' size:'+repr(self.size))
        
        self.es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 1, 0, 3, 8)

        self.background = None
        self.last_save_at = 0
        self.last_back_at = 0
        self.mp4 = None

    def run(self):
        while True:
            # 读取视频流
            grabbed, frame = self.camera.read()
            if not grabbed:
                continue
            # 对帧进行预处理，先转灰度图，再进行高斯滤波。
            # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
            frame_gray = cv2.resize(frame,(640,400))
            frame_gray = cv2.cvtColor(frame_gray, cv2.COLOR_BGR2GRAY)
            frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)

            now = time.time()
            # 将第一帧设置为整个输入的背景
            if self.last_back_at + 1 < now:
                self.last_back_at = now
                self.background = frame_gray
                continue

            # 对于每个从背景之后读取的帧都会计算其与北京之间的差异，并得到一个差分图（different map）。
            # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
            diff = cv2.absdiff(self.background, frame_gray)
            diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1] # 二值化阈值处理
            diff = cv2.dilate(diff, self.es, iterations=2) # 形态学膨胀

            cnz = cv2.countNonZero(diff)
            if cnz>500:
                self.background = frame_gray
                self.last_back_at = 0
                self.saveJpg(frame)
                self.begin(frame)
            else:
                self.stop(frame)

            # cv2.imshow('diff', diff)

            key = cv2.waitKey(1) & 0xFF
            # 按'q'健退出循环
            if key == ord('q'):
                break
    
    def begin(self, image):
        now = time.time()
        if not self.mp4:
            self.mp4 = cv2.VideoWriter('tmp.mp4', cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), self.fps, self.size)
            self.begin_record_at = now
        self.record(image,now)
        self.last_record_at = now
    
    def record(self,image,now):
        if self.mp4:
            t = time.localtime(now)
            s = time.strftime('%Y-%m-%d %H:%M:%S',t)
            image = cv.fromarray(image)
            cv.PutText(image, s, (30,30), self.font, (255,0,0))
            self.mp4.write(np.asarray(image))

    def stop(self, image):
        now = time.time()
        if self.mp4 and self.last_record_at + 5 < now:
            self.mp4.release()
            self.mp4 = None
            t = time.localtime(self.begin_record_at)
            d = time.strftime(self.image_path+'/%Y%m%d',t)
            fb = time.strftime('%H%M%S',t)
            fe = time.strftime('%H%M%S',time.localtime(now))
            if not os.path.exists(d):
                os.mkdir(d)
            filename = "%s/%s-%s.mp4" % (d,fb,fe)
            if os.path.exists("tmp.mp4"):
                os.rename("tmp.mp4",filename)
                print "成功 %s" % filenames
            else:
                print "失败 %s" % filenames
        self.record(image,now)            

    def saveJpg(self, image):
        now = time.time()
        if self.last_save_at + 5 < now:
            t = time.localtime(now)
            d = time.strftime(self.image_path+'/%Y%m%d',t)
            f = time.strftime('%H%M%S',t)
            s = (now - int(now))*1000
            if not os.path.exists(d):
                os.mkdir(d)
            filename = "%s/%s.%03d.jpg" % (d,f,s)
            self.last_save_at = now
            cv2.imwrite(filename,image,[int(cv2.IMWRITE_JPEG_QUALITY), 86])
            os.system("qq send buddy 929909260 '%s'" % filename)

import os
import time
import numpy as np
import cv2.cv as cv
import cv2

camera = cv2.VideoCapture(0)

fps = camera.get(cv2.cv.CV_CAP_PROP_FPS) 
size = (int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

grabbed, frame = camera.read()
writer = cv2.VideoWriter("tmp.avi", cv.CV_FOURCC('M', 'J', 'P', 'G'), 5, size, 1)
font=cv.InitFont(cv.CV_FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 1, 0, 3, 8)
image = cv.fromarray(frame)
cv.PutText(image, "2017-01-01 09:09:09", (30,30), font, (255,0,0))
cv2.imwrite("a.jpg",np.asarray(image))
writer.write(np.asarray(image))
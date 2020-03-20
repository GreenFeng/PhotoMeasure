# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 19:12:37 2019
@author: 27179
"""
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

# mouse callback function
def pointinfo(event,x,y,flags,param):
    global img,point
    color = (0,0,255)
    place = str(y) + "," + str(x)
    if event==cv2.EVENT_LBUTTONDOWN:
        if flags==(cv2.EVENT_FLAG_CTRLKEY+cv2.EVENT_FLAG_LBUTTON):
            cv2.line(img, (x-20,y), (x+20,y), (0,255,0), 1)
            cv2.line(img, (x,y-20), (x,y+20), (0,255,0), 1)
            cv2.putText(img, place, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, color)
            point = [x,y]
        else:
            cv2.line(img, (x-10,y), (x+10,y), (0,255,0), 1)
            cv2.line(img, (x,y-10), (x,y+10), (0,255,0), 1)
            cv2.putText(img, place, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, color)
    elif event==cv2.EVENT_LBUTTONUP:
        ret, img = video.read()
# catch picture from usb camera
video= cv2.VideoCapture(0)
video.set(3,1024)
video.set(4,1280)
video.set(5,30)

cv2.namedWindow('image',cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback('image',pointinfo)
ret, img = video.read()

point = np.zeros((1,2))
while(1):
    cv2.imshow('image',img)
    cv2.putText(img,"prese 'l' to get lefe photo",(100,100),cv2.FONT_HERSHEY_COMPLEX ,1,(255,0,0))
    cv2.putText(img,"prese 'r' to get right photo",(100,100),cv2.FONT_HERSHEY_COMPLEX ,1,(255,0,0))
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()

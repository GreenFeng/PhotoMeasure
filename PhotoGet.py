# -*- coding: utf-8 -*-
'''
@author: hui_DR
@time: 2019.07.04
@project: photo meather
@describe: this section is to get two pictures for double camera length measure
'''
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

def getTwoPictures():
    video= cv2.VideoCapture(0)
#    video.set(3,1024)
#    video.set(4,1280)
#    video.set(5,30)
    color = (0,0,255)
    while(1):
        ret, img = video.read()
        cv2.putText(img,"prese 'l' to get lefe photo",(10,30),cv2.FONT_HERSHEY_COMPLEX ,0.5,(255,0,0))
        cv2.putText(img,"prese 'r' to get right photo",(10,50),cv2.FONT_HERSHEY_COMPLEX ,0.5,(255,0,0))
        cv2.imshow('getTwoPictures',img)
        key_board = cv2.waitKey(1)
#        the if-elif-else contribute samesnot so friendly to cv2.VideoCapture
        if key_board == ord('l'):
            ret, img = video.read()
            cv2.imwrite('left.png',img)
            cv2.putText(img, 'catch left', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color)
            cv2.imshow('getTwoPictures',img)
            cv2.waitKey(1)
            time.sleep(3)
        if key_board == ord('r'):
            ret, img = video.read()
            cv2.imwrite('right.png',img)
            cv2.putText(img, 'catch right', (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color)
            cv2.imshow('getTwoPictures',img)
            cv2.waitKey(1)
            time.sleep(3)
        # "27" = "Esc"
        if key_board == 27:
            break
    video.release()
    cv2.destroyAllWindows()
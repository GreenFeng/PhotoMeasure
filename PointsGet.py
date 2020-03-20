# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 08:33:42 2019
@author: 27179
"""
import numpy as np
import cv2

point_x = np.zeros((2,))
point_y = np.zeros((2,))
X = Y = -1
def pointinfo(event,x,y,flags,param):
    global img, point_x, point_y, X, Y
    if event==cv2.EVENT_LBUTTONDOWN or event==cv2.EVENT_RBUTTONDOWN:
        X,Y = x,y
        if flags==(cv2.EVENT_FLAG_CTRLKEY+cv2.EVENT_FLAG_LBUTTON):
            point_x[0] = x
        elif flags==(cv2.EVENT_FLAG_ALTKEY+cv2.EVENT_FLAG_LBUTTON):
            point_x[1] = x
        elif flags==(cv2.EVENT_FLAG_CTRLKEY+cv2.EVENT_FLAG_RBUTTON):
            point_y[0] = y
        elif flags==(cv2.EVENT_FLAG_ALTKEY+cv2.EVENT_FLAG_RBUTTON):
            point_y[1] = y
    elif event==cv2.EVENT_LBUTTONUP or event==cv2.EVENT_RBUTTONUP:
        X = Y = -1

key_point = np.zeros((4,1,2),np.int)
Ncount = 0
def key_point_catch(event,x,y,flags,param):
    global img, key_point, Ncount,  X, Y
    if event==cv2.EVENT_LBUTTONDOWN:
        X,Y = x,y
        if flags==(cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_LBUTTON) and Ncount<4:
            key_point[Ncount] = [x,y]
            Ncount += 1
    elif event==cv2.EVENT_LBUTTONUP:
        X = Y = -1
#if event.X>0:
#    place = str(event.Y) + "," + str(event.X)
#    num = str(event.Ncount)
#    cv2.circle(img,(event.X,event.Y),5,color,2)
#    cv2.putText(img, place, (event.X,event.Y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color)
#    cv2.putText(img, num, (event.X,event.Y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color)
#elif event.Ncount==4:
#    ret,img = video.read()
#    cv2.drawContours(img, [event.key_point[:]],-1,(0,0,255),2)
#else:
#    ret,img = video.read()                
#if key_board==27:
#    break
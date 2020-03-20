# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:22:54 2019

@author: 27179
"""

import cv2
import numpy as np
import glob

# Load previously saved data
with np.load('CameraFeature.npz') as X:
    mtx, dist, rvecs, tvecs = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

def draw(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)
    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)
    return img

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((9*11,3), np.float32)
objp[:,:2] = np.mgrid[0:11,0:9].T.reshape(-1,2)*20

axis = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0],
                   [0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])*30
n = 0
for fname in glob.glob('*.jpg'):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (9,11),None)
    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners,(9,11),(-1,-1),criteria)
        imgpts, jac = cv2.projectPoints(axis, rvecs[n], tvecs[n], mtx, dist)
        img = draw(img,corners2,imgpts)
        cv2.imshow('img',img)
        n += 1
        # "27" = "Esc"
        if cv2.waitKey(0) != 27:
            break

cv2.destroyAllWindows()
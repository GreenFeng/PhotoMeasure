# -*- coding: utf-8 -*-
'''
@author: hui_DR
@time: 2019.07.04
@project: photo meather
@describe: section1 is to 
'''
import numpy as np
import cv2
import glob

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((9*11,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:11].T.reshape(-1,2)*20

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)*10
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

#glob moude could be use when you need input all the variates
images = glob.glob('*.jpg')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9,11), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2=cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

n = 0
for fname in images:
    img = cv2.imread(fname)
    imgpts, jac = cv2.projectPoints(axis, rvecs[n], tvecs[n], mtx, dist)
    img = draw(img,imgpoints[n],imgpts)
    cv2.imshow('img',img)
    if cv2.waitKey(0)==27:
        n += 1
    else:
        break
cv2.destroyAllWindows()
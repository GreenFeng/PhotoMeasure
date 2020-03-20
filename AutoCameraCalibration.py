# -*- coding: utf-8 -*-
'''
@author: hui_DR
@time: 2019.07.04
@project: photo meather
@describe: this is camera calibrat method
'''
import numpy as np
import cv2
import time
import glob

def CalibrationWithVideo():
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((9*11,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:11].T.reshape(-1,2)*20
    # arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.
    
    video = cv2.VideoCapture(0)
    n = 0
    while 1:
        ret,img = video.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow('gray',gray)
        
        # "27" = "Esc"
        if cv2.waitKey(1)==27:
            break
        # find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (9,11), None)
        # if found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            cv2.imwrite(str(n)+'.jpg',img)
            corners2=cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (9,11), corners2, ret)
            cv2.imshow('img', img)
            n += 1
            if n==15:
                break
            cv2.waitKey(1)
            time.sleep(3)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.savez('CameraFeature',mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs, ret=ret)
    video.release()
    cv2.destroyAllWindows()

def CalibrationWithPicture():
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((9*11,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:11].T.reshape(-1,2)*20
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    n = 0
    for fname in glob.glob('*.jpg'):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9,11),None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2=cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (9,11), corners2, ret)
            cv2.imshow('img', img)
            n += 1
            if n==15:
                break
            cv2.waitKey(1)
            time.sleep(0.1)
    cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.savez('CameraFeature',mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs, ret=ret)
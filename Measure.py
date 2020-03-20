# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:48:45 2019
mainly about the photo measure meoth
@author: 27179
"""
import cv2
import time
import numpy as np
import PointsGet as event

color = (0, 0, 255)
data = np.load('CameraFeature.npz')
[mtx, dist, rvecs, tvecs, ret] = [data[d] for d in data]

p_l = cv2.imread('left.png')
p_r = cv2.imread('right.png')

img = np.hstack((p_l,p_r))

z_space,h_space = 0,0

def Manually( ):
    global z_space, h_space, img, p_r, p_l, mtx, dist, rvecs, tvecs
    cv2.imshow('measure',img)
    cv2.setMouseCallback('measure',event.pointinfo)
    while 1:
        cv2.imshow('measure',  img)
        key_board = cv2.waitKey(1)
        
        # get the distance of choose points
        if event.point_y[1]>0 and z_space!=0:
            h_space = np.diff(event.point_y)
            h_space = z_space*h_space/(mtx[0,0])
            space_info = "this thing's higeht is "+str(h_space)[1:6]+"cm"   
            cv2.putText(img, space_info, (10,20),cv2.FONT_HERSHEY_COMPLEX ,0.7,(255,0,0))
                
        # get the distance of choose point
        if event.point_x[1]>0:
            z_space = np.diff(event.point_x)
            z_space = 20*mtx[0,0]  / ((p_l.shape[1]-z_space))
            space_info = "this point's distance is "+str(z_space)[1:6]+"cm"
            cv2.putText(img, space_info, (10,50),cv2.FONT_HERSHEY_COMPLEX ,0.7,(255,0,0))

        if event.X !=-1 :
            place = str(event.Y) + "," + str(event.X)
            # cv2.line(img, (event.X-20,event.Y+20), (event.X+20,event.Y-20), (0,255,0), 1)
            # cv2.line(img, (event.X-20,event.Y-20), (event.X+20,event.Y+20), (0,255,0), 1)
            cv2.circle(img,(event.X,event.Y),5,color,2)
            cv2.putText(img, place, (event.X,event.Y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color)
            cv2.imshow('measure',img)
            cv2.waitKey(1)
        # "27" = "Esc"
        if key_board==27:
            break
        
    cv2.destroyAllWindows()

def Autoly( ):
    global z_space, h_space, img, p_r, p_l, mtx, dist, rvecs, tvecs
    img = np.hstack((p_l,p_r))
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(p_l,None)
    kp2, des2 = orb.detectAndCompute(p_r,None)
    
    bf = cv2.BFMatcher()
    matches = bf.match(des1,des2)
    matches = sorted(matches, key = lambda x:x.distance)   
    
    src_pts = np.float32( [kp1[matches[0].queryIdx].pt] ).reshape(2)
    dst_pts = np.float32( [kp2[matches[0].trainIdx].pt] ).reshape(2)
    z_space = src_pts[0]-dst_pts[0]
    
    dst_pts[0]+=p_l.shape[1]
    img0 = cv2.circle(img,tuple(src_pts),5,color,2)    
    img0 = cv2.circle(img,tuple(dst_pts),5,color,2)
    # img0 = cv2.line(img, tuple(src_pts), tuple(dst_pts), (255,0,0), 2)
    
    z_space = 20*mtx[0,0] / (z_space)
    space_info = "this point's distance is "+str(z_space)[0:5]+"cm"
    
    cv2.putText(img0, space_info, (10,50), cv2.FONT_HERSHEY_COMPLEX , 0.7, (255,0,0))
    cv2.imshow("measure",img0)
    if cv2.waitKey(0)==27:
        cv2.destroyAllWindows()
    
def Singally():
    video = cv2.VideoCapture(0)
    global mtx, dist, rvecs, tvecs
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((9*11,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:11].T.reshape(-1,2)*20
    
    while 1:
        ret,img = video.read()
        
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9,11),None)
        if ret==True:
            corners2=cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            cv2.drawChessboardCorners(img, (9,11), corners2, ret)
            ret, rvecs, tvecs = cv2.solvePnP(objp, corners2, mtx, dist)
            rvecs, jacobian = cv2.Rodrigues(rvecs,dist)
            M2 = np.hstack((rvecs,tvecs))
            W = np.zeros([4,1])
            W[3,0] = 1
            coordinate_camera = M2 @ W
            place = "distance is " + str(coordinate_camera[2,0]/10)[0:5]+"cm"
            x_y = [ int(corners2[0][0,0]),int(corners2[0][0,1]) ]
            cv2.putText(img, place, tuple(x_y), cv2.FONT_HERSHEY_COMPLEX , 0.5, (255,0,0))
            cv2.imshow('key_point_catch',img)
            key_board = cv2.waitKey(1)
        else:
            cv2.imshow('key_point_catch',img)
            key_board = cv2.waitKey(1)
            
        # "27" = "Esc"
        if key_board==27:
            break
        
    video.release()
    cv2.destroyAllWindows()
    
def Correct():
    pass

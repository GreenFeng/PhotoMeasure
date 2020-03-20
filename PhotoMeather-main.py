# -*- coding: utf-8 -*-
import AutoCameraCalibration as calibrat
import PhotoGet as getphoto
import Measure as measure

# calibrate the camera by video
# calibrat.CalibrationWithVideo()

# calibrate the camera by default pictures
calibrat.CalibrationWithPicture()

# catch two pictures
# getphoto.getTwoPictures()

# use two pictures to measure hight and distance of the chosen points mannually
measure.Manually()
# move camera 10cm and use feature recognition measure special point autoly
measure.Autoly()

# use the video find a chessboard and measure the distance
measure.Singally()
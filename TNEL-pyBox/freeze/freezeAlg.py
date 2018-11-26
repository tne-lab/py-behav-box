import numpy as np
import cv2
import argparse
import datetime
import imutils
import time
import pandas as pd

class Vid:
    def __init__(self, videoPath, winName):
        self.cap = cv2.VideoCapture(videoPath)
        if self.cap.isOpened():
            self.startFrame = 0
            self.spf = int((1/self.cap.get(5))*1000)
            #self.cap.set(1,self.startFrame)
            self.winName = winName
            self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cv2.namedWindow(self.winName)
            self.min = 0
            self.timeFrozen = 0
            self.text = ''
            self.capError = False
            self.freezeFile = open('freezes2.txt','w')
            self.isFrozen = False
            self.threshold = 20
            self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.index = 0
        else:
            self.capError = True
        self.csv = pd.read_csv('FR1_freezing.csv')
        self.csvText = ''

    def frameBar(self,winName,trackName,min, max):
        cv2.createTrackbar(trackName, winName,min,max,
        lambda x: self.picFrame(x, self))

    def picFrame(x, frame, self):
        self.startFrame = frame
        self.cap.set(1,self.startFrame)
        #Reset Frozen time
        self.isFrozen = False
        self.timeFrozen = 0

    def setByTime(self):
        self.cap.set(0,self.timeToMilli(self.csv['Time'][self.index]))
        self.index+=1

    def timeToMilli(self, s):
        s = s.replace(".",":")
        hours, minutes, seconds, milliseconds = s.split(":")
        return int(hours)*60*60*1000 + int(minutes)*60*1000 + int(seconds)*1000 + int(milliseconds)

    def genROI(self, frame):
        self.r = cv2.selectROI(frame)
        cv2.destroyWindow("ROI selector")

    def genPrev(self, frame, prevFrame):
        self.prevFrame = frame
        self.prevThresh = self.calcInitThresh(frame, prevFrame)

    def run(self, time_from_GUI, vid_cur_time, time_diff):
        #Get frame
        ret, frame = self.cap.read()
        if not ret:
            print('error in getting read')
            break

        # Create ROI if not done yet
        # Otherwise grab ROI
        imgROI = frame[int(self.r[1]):int(self.r[1]+self.r[3]),int(self.r[0]):int(self.r[0] + self.r[2])]

        #Make gray and blur
        gray = cv2.cvtColor(imgROI, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        cv2.imshow(self.winName,gray)

        movingPxls = self.calcMovingPixels(gray)

        # Moving or frozen?
        if movingPxls>70:
            self.text = 'move'
            self.timeFrozen = 0
            if self.isFrozen:
                self.isFrozen = False
                self.freezeFile.write('end freeze: ' + str(self.milliToTime(self.cap.get(0))) + '\n')
        else:
            if self.checkFreeze() and not self.isFrozen:
                self.isFrozen = True
                self.freezeFile.write('freeze: ' + str(self.milliToTime(self.cap.get(0))) + '\n')
                self.text = 'freeze'

        if self.csv['Freezing'][self.index-1]:
            self.csvText = 'Freeze'
        else:
            self.csvText = 'move'

        ### NEED TO CHANGE THIS
        self.writeStuff(time_from_GUI, vid_cur_time, time_diff, prevThresh, gray)
        # Write stuff on screen

        cv2.imshow('thresh',prevThresh)
        # Get next frame
        self.startFrame+=1

        if cv2.waitKey(self.spf) & 0xFF == ord('q'):
            break

    def calcInitThresh(self, frame, prevFrame):
        frameDelta = cv2.absdiff(frame, prevFrame)
        return cv2.threshold(frameDelta, self.threshold, 255, cv2.THRESH_BINARY)[1]

    def calcMovingPixels(self, frame, prevFrame, prevThresh):
        #Start motion detection
        # compute the absolute difference between the current frame and
        # previous frame
        frameDelta = cv2.absdiff(frame, self.prevFrame)
        thresh = cv2.threshold(frameDelta, self.threshold, 255, cv2.THRESH_BINARY)[1]

        diff = cv2.subtract(thresh, self.prevThresh)
        movingPxls = cv2.countNonZero(diff)
        self.prevThresh = thresh
        self.prevFrame = frame
        return movingPxls, thresh, frame

    def checkFreeze(self):
        if self.timeFrozen < 0:
            self.timeFrozen+=self.spf
            print('freeze time: ' + str(self.timeFrozen))
            return False
        else:
            self.timeFrozen+=self.spf
            return True

    def close(self):
        self.freezeFile.close()
        self.cap.release()
        cv2.destroyAllWindows()

    def milliToTime(milliseconds):
        seconds=(milliseconds/1000)%60
        minutes=(milliseconds/(1000*60))%60
        hours=(milliseconds/(1000*60*60))%24
        return str(int(hours)) + ":" + str(int(minutes)) + ":" + str(seconds)

    def writeStuff(time_from_GUI, vid_cur_time, time_diff, prevThresh, gray):
        cv2.putText(gray,"NIDAQ time = " + str(time_from_GUI),(20,405), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(gray,"Video time = :" + str(vid_cur_time),(20,430), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(gray,"time diff = :" + str(time_diff),(20,455), font, 0.5,(255,255,255),2,cv2.LINE_AA)

        cv2.putText(prevThresh,"Moving Pixels = " + str(moving_pixels),(20,430), font, 0.5,(255,255,255),2,cv2.LINE_AA)


        cv2.putText(prevThresh, self.text, (10, 50),cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)
        cv2.putText(prevThresh, str(self.timeFrozen), (100, 50),cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)

        cv2.putText(prevThresh, self.csvText, (10, 75),cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)
        cv2.putText(prevThresh, str(self.startFrame), (10,95), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255),2)

        cv2.putText(prevThresh, str(self.csv['Time'][self.index-1]), (10,110), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255),2)
        cv2.putText(prevThresh, self.milliToTime(self.cap.get(0)), (10,125), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255),2)

def main():
    vid = Vid('FR_con1.avi','vid')
    vid.frameBar('vid','frameNumber',0, vid.length)
    vid.run()
    vid.close()


main()

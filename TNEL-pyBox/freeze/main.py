import numpy as np
import cv2
from vidClass import Vid
import argparse
import datetime
import imutils
import time

class Vid:
    def __init__(self, videoPath, winName):
        self.cap = cv2.VideoCapture(videoPath)
        self.startFrame = 0
        self.fps = int((1/self.cap.get(cv2.cv2.CAP_PROP_FPS))*1000)
        self.cap.set(1,self.startFrame)
        self.winName = winName
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cv2.namedWindow(self.winName)
        self.min = 0
        self.firstFrame = None

    def trackBar(self,winName,trackName,min, max):
        cv2.createTrackbar(trackName, winName,min,max,
        lambda x: self.picFrame(x, self))

    def picFrame(x, frame, self):
        self.startFrame = frame
        self.cap.set(1,self.startFrame)

    def run(self):
        while(self.cap.isOpened()):
            #Get frame
            ret, frame = self.cap.read()
            try:
                imgROI = frame[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0] + r[2])]
            except:
                r = cv2.selectROI(frame)
                cv2.destroyWindow("ROI selector")
                continue

            if not ret:
                break
            text = 'freeze'
            #Make gray and blur
            gray = cv2.cvtColor(imgROI, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            cv2.imshow(self.winName,gray)


            self.startFrame+=1
            if self.firstFrame is None:
            		self.firstFrame = gray
            		continue
            else:
                #Start motion detection
            	# compute the absolute difference between the current frame and
            	# first frame
                frameDelta = cv2.absdiff(self.firstFrame, gray)
                self.firstFrame = gray
                thresh = cv2.threshold(frameDelta, 23, 255, cv2.THRESH_BINARY)[1]

                try:
                    diff = cv2.subtract(thresh, prevThres)
                    moving_pixels = cv2.countNonZero(diff)
                    print(moving_pixels)
                    prevThres = thresh
                except:
                    prevThres = thresh
                    continue


            if moving_pixels>40:
                text = 'move'

            cv2.putText(thresh,text, (10, 50),cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)
            cv2.imshow('thresh',thresh)
            if cv2.waitKey(self.fps) & 0xFF == ord('q'):
                break

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()



def main():
    vid = Vid('FR_con1.avi','vid')
    vid.trackBar('vid','frameNumber',0, vid.length)
    vid.run()
    vid.close()


main()

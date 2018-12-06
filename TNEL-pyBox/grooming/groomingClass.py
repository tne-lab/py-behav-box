from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import argparse
import imutils
import time
import cv2
# https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/

class GroomingVid:
    def __init__(self, videoPath, winName = 'vid'):
        self.winName = winName
        self.cap = cv2.VideoCapture(videoPath)
        if self.cap.isOpened():
            print('opened vid')
            # Setup video
            self.startFrame = 1
            self.cap.set(1,self.startFrame)
            ret, self.frame = self.cap.read()
            #cv2.namedWindow(self.winName)
            # Get info from video
            self.spf = int((1/self.cap.get(5))*1000)
            self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Init vars
            self.text = ''
            self.capError = False
            # in milliseconds (2000 = 2 seconds)
            self.freezeLength = 5000

            # Trackbars
            #self.frameBar(winName,'frameNumber',0, self.length)
        else:
            print('error opening vid')
            self.capError = True

        self.leftCoords = (0,0)
        self.rightCoords = (0,0)
        self.listCoords = [self.leftCoords, self.rightCoords]
        self.leftDisappeared = 0
        self.rightDisappeared = 0

        self.ready = False

#######################################################################################
#######################################################################################
    # grooming alg
    def update(self, rects):
        if len(rects) == 0:
            # No hands detected..
            self.leftDisappeared += 1
            self.rightDisappeared += 1
            return

        inputCentroids = np.zeroes((lens(rects), 2), dtype="int")

        for(i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        D = dist.cdist(np.array(self.listCoords), inputCentroids)


        lowestVal = D.argmin(axis=1)
        for i in range(self.listCoords):
            self.listCoords[i] = inputCentroids[lowestVal[i]]

        # Handle disappear #


#######################################################################################
#######################################################################################
    # Call this every loop
    def run(self,q, back_q):
        while(self.cap.isOpened()):
            vid_cur_time = time.perf_counter()
            print('running')
            '''
            if not self.ready:
                print('not ready')
                ret, self.frame = self.cap.read()
                imgROI = self.frame[int(self.r[1]):int(self.r[1]+self.r[3]),int(self.r[0]):int(self.r[0] + self.r[2])]
                print('we small')
                #Make gray and blur
                gray = cv2.cvtColor(imgROI, cv2.COLOR_BGR2GRAY)
                print('and gray')
                # Still blur?
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
                print('and blurred')
                print('and we wnat to show')
                cv2.imshow(self.winName, gray)
                print('but..')

            else:
            '''
            # Run video
            try:
                msg = q.pop()
                time_from_GUI = msg['cur_time']
                STATE = msg['STATE']
                msg['time_diff'] = vid_cur_time - time_from_GUI
                msg['vid_time'] = vid_cur_time
                #msg['out'] = out
            except:
                return
            #Get frame
            ret, frame = self.cap.read()
            if not ret:
                print('error in getting read')
                return
            # Grab only ROI
            imgROI = frame[int(self.r[1]):int(self.r[1]+self.r[3]),int(self.r[0]):int(self.r[0] + self.r[2])]
            #Make gray and blur
            gray = cv2.cvtColor(imgROI, cv2.COLOR_BGR2GRAY)
            # Still blur?
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            cv2.imshow(self.winName, frame)
            #getBlobs(gray)
            #self.update()
            #drawHands()

            '''


            # grooming or not?
            if movingPxls > 70:
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

            # Write stuff on screen
            self.writeStuff(msg['cur_time'], msg['vid_time'], msg['time_diff'], movingPxls, frame)
            if msg['STATE'] == 'REC':
                msg['out'].write(frame)
                '''
            # Show the frames

            #self.setupHands()

            # Create dict to send back to main GUI
            #backDict = {'vid_time':vid_cur_time, 'Grooming':self.grooming, 'NIDAQ_time':time_from_GUI, 'Vid-NIDAQ':msg['time_diff']}
            #back_q.put(backDict)

            # Get next frame and check if we are done
            self.startFrame+=1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print('done')
                self.close()
                return

            #if msg['STATE'] == 'STOP':
            #    self.close()
            #    return

    # Close everything
    def close(self):
        self.freezeFile.close()
        self.cap.release()
        cv2.destroyAllWindows()


################################################################################################
################################################################################################

    # Start etting up hands and color mask
    def setupHands(self):
        print('Double click left hand first, then right hand')
        self.leftCoords = (0,0)
        self.rightCoords = (0,0)
        cv2.setMouseCallback(self.winName, lambda event,  x, y, flags, param : self.setHands(event, x, y, flags, param))

    # Mouseclick callback to setup hand locations
    def setHands(self, event, x, y, flags, param):
        print('mouseclick')
        if event == cv2.EVENT_LBUTTONDBLCLK:
            if self.leftCoords == (0,0):
                self.leftCoords = (x,y)
            elif self.rightCoords == (0,0):
                self.rightCoords = (x,y)
                # after right hand clicked wait for color click
                cv2.setMouseCallback(self.winName, None)
                print("Hand setup complete")
                self.detectColor()

    # Start hand color mask setup
    def detectColor(self):
        print("Double click on hand color now!! Do it twice and try to get the highest and lowest shade")
        self.lower = None
        self.upper = None
        cv2.setMouseCallback(self.winName, lambda event, x, y, flags, param: self.getColor(event, x, y, flags, param))

    def getColor(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            # Turn these into a range..?? Average over a region of interest???
            # For now click twice. Pretty wonky and proabably wont work.. Maybe just create a range of like 25 will be better
            if self.lower is None:
                self.lower = np.array(self.frame[y, x], dtype = "uint8")
            elif self.upper is None:
                self.upper = np.array(self.frame[y, x], dtype = "uint8")

            if self.lower is not None and self.upper is not None:
                self.mask =  cv2.inRange(self.frame, lower, upper)
                print("Mask created, ready to start!")
                cv2.setMouseCallback(self.winName, None)
                self.ready = True


            #self.mask = cv2.bitwise_and(image, image, mask = mask)
            #cv2.imshow("images", np.hstack([image, output]))
	        #cv2.waitKey(0)



    # Creates a trackbar to scroll through frames. Could use some work
    # to account for any trackbar
    def frameBar(self,winName,trackName, min, max):
        cv2.createTrackbar(trackName, winName,min,max,
        lambda x: self.picFrame(x, self))


    # Create Region of Interest coordinates
    def genROI(self):
        self.r = cv2.selectROI(self.frame)
        cv2.destroyWindow("ROI selector")

        # Timing stuff
    # Go from milliseconds to time string
    def milliToTime(self, milliseconds):
        seconds=(milliseconds/1000)%60
        minutes=(milliseconds/(1000*60))%60
        hours=(milliseconds/(1000*60*60))%24
        return str(int(hours)) + ":" + str(int(minutes)) + ":" + str(seconds)
    # Go from time string to milliseconds
    def timeToMilli(self, s):
        s = s.replace(".",":")
        hours, minutes, seconds, milliseconds = s.split(":")
        return int(hours)*60*60*1000 + int(minutes)*60*1000 + int(seconds)*1000 + int(milliseconds)

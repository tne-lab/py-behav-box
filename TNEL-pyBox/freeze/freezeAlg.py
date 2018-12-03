import cv2
import time

class Vid:
    def __init__(self, videoPath, winName):
        self.cap = cv2.VideoCapture(videoPath)
        if self.cap.isOpened():
            # Setup video
            self.startFrame = 1
            self.cap.set(1,self.startFrame)
            self.winName = winName
            cv2.namedWindow(self.winName)
            # Get info from video
            self.spf = int((1/self.cap.get(5))*1000)
            self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Init vars
            self.min = 0
            self.timeFrozen = 0
            self.text = ''
            self.capError = False
            self.freezeFile = open('freezes2.txt','w')
            self.isFrozen = False
            self.threshold = 8
            # in milliseconds (2000 = 2 seconds)
            self.freezeLength = 5000

            # Trackbars
            cv2.createTrackbar('threshold', 'vid', 0, 30,
            lambda x: self.changeThresh(x, self))
            self.frameBar(winName,'frameNumber',0, self.length)
        else:
            print('error opening vid')
            self.capError = True

#######################################################################################
#######################################################################################
    # Call this every loop
    def run(self, q, back_q, out):
        while(self.cap.isOpened()):
            vid_cur_time = time.perf_counter()

            # Run video
            try:
                msg = q.pop()
                time_from_GUI = msg['cur_time']
                STATE = msg['STATE']
                msg['time_diff'] = vid_cur_time - time_from_GUI
                msg['vid_time'] = vid_cur_time
                msg['out'] = out
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
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            movingPxls = self.calcMovingPixels(gray)

            # Moving or frozen?
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

            # Show the frames
            cv2.imshow('thresh',self.prevThresh)
            cv2.imshow(self.winName,frame)

            # Create dict to send back to main GUI
            backDict = {'vid_time':vid_cur_time, 'FROZEN':self.isFrozen, 'NIDAQ_time':time_from_GUI, 'Vid-NIDAQ':msg['time_diff']}
            back_q.put(backDict)

            # Get next frame and check if we are done
            self.startFrame+=1
            if cv2.waitKey(self.spf) & 0xFF == ord('q'):
                self.close()
                return
            if msg['STATE'] == 'STOP':
                self.close()
                return

################################################################################################
################################################################################################

    # Close everything
    def close(self):
        self.freezeFile.close()
        self.cap.release()
        cv2.destroyAllWindows()

    ### Helper Functions ###

    # Creates a trackbar to scroll through frames. Could use some work
    # to account for any trackbar
    def frameBar(self,winName,trackName, min, max):
        cv2.createTrackbar(trackName, winName,min,max,
        lambda x: self.picFrame(x, self))

    # Change the threshold
    def changeThresh(x, thresh, self):
        self.threshold = thresh

    # Changes the frame to start at
    def picFrame(x, frame, self):
        self.startFrame = frame
        self.cap.set(1,self.startFrame)
        # Reset Frozen time
        self.isFrozen = False
        self.timeFrozen = 0

    # Create Region of Interest coordinates
    def genROI(self, frame):
        self.r = cv2.selectROI(frame)
        cv2.destroyWindow("ROI selector")

    # Create a previous frame and thresh to be used for comparison
    def genPrev(self, frame, prevFrame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        self.prevFrame = gray
        prevGray = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)
        prevGray = cv2.GaussianBlur(prevGray, (21, 21), 0)
        self.prevThresh = self.calcInitThresh(gray, prevGray)

    # Creates threshold for first time
    def calcInitThresh(self, frame, prevFrame):
        frameDelta = cv2.absdiff(frame, prevFrame)
        return cv2.threshold(frameDelta, self.threshold, 255, cv2.THRESH_BINARY)[1]

    # Get moving pixels count
    def calcMovingPixels(self, frame):
        # Motion detection
        # compute the absolute difference between the current frame and
        # previous frame
        frameDelta = cv2.absdiff(frame, self.prevFrame)
        thresh = cv2.threshold(frameDelta, self.threshold, 255, cv2.THRESH_BINARY)[1]

        diff = cv2.subtract(thresh, self.prevThresh)
        movingPxls = cv2.countNonZero(diff)
        self.prevThresh = thresh
        self.prevFrame = frame
        return movingPxls

    # If frozen look at how long its been frozen to change state
    def checkFreeze(self):
        if self.timeFrozen < self.freezeLength:
            self.timeFrozen+=self.spf
            return False
        else:
            self.timeFrozen+=self.spf
            return True

    # Wrtie a ton of stuff on frames...
    def writeStuff(self, time_from_GUI, vid_time, time_diff, movingPxls, frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,"NIDAQ time = " + str(time_from_GUI),(20,405), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,"Video time = :" + str(vid_time),(20,430), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,"time diff = :" + str(time_diff),(20,455), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(self.prevThresh,"Moving Pixels = " + str(movingPxls),(20,430), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame, self.text, (10, 50),font, .5, (255, 255, 255), 2)
        cv2.putText(self.prevThresh, str(self.timeFrozen), (100, 50),font, .5, (255, 255, 255), 2)
        cv2.putText(self.prevThresh, str(self.startFrame), (10,95), font, .5, (255,255,255),2)
        cv2.putText(self.prevThresh, str(self.length), (10,110), font, .5, (255,255,255),2)

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

print('freezeAlg Loaded')

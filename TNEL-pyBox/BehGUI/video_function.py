import cv2
import time

class Vid:
    def __init__(self, videoPath, q, back_q, winName = 'vid'):
        self.cap = cv2.VideoCapture(videoPath)
        self.winName = winName
        self.q = q
        self.back_q = back_q
        self.out = None
        self.outPath = 'NOT SET'
        cv2.namedWindow('vid')
        if self.cap.isOpened():
            if not self.vidOrLive(videoPath):
                return False
            # Setup video
            self.startFrame = 1
            self.cap.set(1,self.startFrame)
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
            cv2.createTrackbar('threshold', 'vid', 0, 30,
            lambda thresh: self.changeThresh(thresh))
            # Init some stuff
            self.initROIFrames()
            self.back_q.put('vid ready')
        else:
            print('error opening vid')
            self.capError = True

    # Init based on video file or livestream
    def vidOrLive(self, videoPath):
        # Check if video or livestream
        # Video File
        if isinstance(videoPath, str):
            # Get info from video
            self.mspf = int((1/self.cap.get(5))*1000)
            print(self.mspf)
            self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Trackbars
            self.frameBar(self.winName,'frameNumber',0, self.length)
            return True
        # livestream!
        elif isinstance(videoPath, int): # Calculates Frames Per Sec (FPS)
            # Number of frames to capture
            numFrames = 60;

            # Start time
            start = time.time()
            # Grab a few frames
            for i in range(0, numFrames) :
                ret, frame = self.cap.read()
            # End time
            end = time.time()
            # Time elapsed
            seconds = end - start
            # Calculate frames per second
            fps  = numFrames / seconds;
            self.mspf = int(1/fps * 1000)
            self.length = None
            return True
        # Something else?
        else:
            print('other video type.. Going to break')
            return False

    # Generates inital stuff. GET Region of Interest (ROI)
    def initROIFrames(self):
        ret, frame = self.cap.read()
        if not ret:
            print('frame read error')
            return
        self.genROI(frame)

        # Gen prev frame and threshold (Use size of ROI)
        self.startFrame+=1
        ret, newFrame = self.cap.read()
        if not ret:
            print('frame read error')
            return
        frameROI = frame[int(self.r[1]):int(self.r[1]+self.r[3]),int(self.r[0]):int(self.r[0] + self.r[2])]
        newFrameROI = newFrame[int(self.r[1]):int(self.r[1]+self.r[3]),int(self.r[0]):int(self.r[0] + self.r[2])]
        self.genPrev(newFrameROI, frameROI)


#######################################################################################
#######################################################################################
    # Call this every loop
    def run(self):
        movingPxls = 0
        while(self.cap.isOpened()):
            vid_cur_time = time.perf_counter()

            # Run video
            try:
                msg = self.q.pop()
                time_from_GUI = msg['cur_time']
                STATE = msg['STATE']# "REC" "STOP" "FREEZE_DETECT"
                msg['time_diff'] = vid_cur_time - time_from_GUI
                msg['vid_time'] = vid_cur_time
                if msg['PATH_FILE'] != self.outPath:
                    self.openOutfile(msg['PATH_FILE'], self.cap.get(4) , self.cap.get(3))
            except IndexError:
                continue
            #Get frame
            #if msg['STATE'] == "FREEZE_DETECT":
            #self.initROIFrames()
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
                    #back_q.put({'FREEZE' : False, 'TIME' : time_from_GUI})
            else:
                if self.checkFreeze() and not self.isFrozen:
                    self.isFrozen = True
                    self.freezeFile.write('freeze: ' + str(self.milliToTime(self.cap.get(0))) + '\n')
                    #back_q.put({'FREEZE' : True, 'TIME' : time_from_GUI})
                    self.text = 'freeze'

            # Write stuff on screen (need to add trial number and probably not time differential)
            #self.drawInfo(msg['cur_time'], msg['trial_num'], movingPxls, frame)
            self.writeStuff(msg['cur_time'], msg['vid_time'], msg['time_diff'], movingPxls, msg['STATE'], frame)

            # draw trial start circle

            if msg['STATE'] == 'REC':
                self.out.write(frame)

            # Show the frames
            cv2.imshow('thresh',self.prevThresh)
            cv2.imshow(self.winName,frame)

            # Create dict to send back to main GUI
            backDict = {'vid_time':vid_cur_time, 'FROZEN':self.isFrozen, 'NIDAQ_time':time_from_GUI, 'Vid-NIDAQ':msg['time_diff']}
            self.back_q.put(backDict)

            # Get next frame and check if we are done
            self.startFrame+=1
            if cv2.waitKey(self.mspf) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                self.out.release()
                self.close()
                return

            if msg['STATE'] == 'STOP':
                cv2.destroyAllWindows()
                self.out.release()
                self.close()
                return


################################################################################################
################################################################################################

    def openOutfile(self, path, height, width):
        self.outPath = path
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # for AVI files
        print(1.0/self.mspf * 1000)
        self.out = cv2.VideoWriter(path,fourcc, 1.0/self.mspf * 1000, (int(width),int(height)))
        print("SAVING TO: ", path)

    def mouse_callback(self, event, x, y, flags, params):
        if event == 2:
            self.clicks = int(self.frame[x, y])
### #set mouse callback function for window
#cv2.setMouseCallback('image', mouse_callback)

    # Close everything
    def close(self):
        self.freezeFile.close()
        self.cap.release()
        cv2.destroyAllWindows()
        for i in range(1,10):
            cv2.waitKey(1)

    ### Helper Functions ###


    # Update screen info
    def drawInfo(self, time_from_GUI, trial_num, movingPxls, frame):
        #cv2.circle(frame, (x,y), 15, (255,0,0))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,"NIDAQ time = " + str(time_from_GUI),(20,405), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame, self.text, (10, 50),font, .5, (255, 255, 255), 2)
        cv2.putText(self.prevThresh,"Moving Pixels = " + str(movingPxls),(20,430), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(self.prevThresh, "Trial Number = " + str(trial_num), (100, 50),font, .5, (255, 255, 255), 2)

    # Wrtie a ton of stuff on frames...
    def writeStuff(self, time_from_GUI, vid_time, time_diff, movingPxls, state, frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,"NIDAQ time = " + str(time_from_GUI),(20,405), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,"Video time = " + str(vid_time),(20,430), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,"time diff = " + str(time_diff),(20,455), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame, self.text, (10, 50),font, .5, (255, 255, 255), 2)
        #if state == "FREEZE_DETECT":
        cv2.putText(self.prevThresh,"Moving Pixels = " + str(movingPxls),(20,430), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(self.prevThresh, "Time frozen = " + str(self.timeFrozen), (100, 50),font, .5, (255, 255, 255), 2)
        cv2.putText(self.prevThresh, "Current frame = " + str(self.startFrame), (10,95), font, .5, (255,255,255),2)
        cv2.putText(self.prevThresh, "Number of frames = " + str(self.length), (10,110), font, .5, (255,255,255),2)

    # Creates a trackbar to scroll through frames. Could use some work
    # to account for any trackbar
    def frameBar(self,winName,trackName, min, max):
        cv2.createTrackbar(trackName, winName,min,max,
        lambda x: self.picFrame(x, self))

    # Change the threshold
    def changeThresh(self, thresh):
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
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,"SELECT REGION OF INTEREST (CLICK AND DRAG MOUSE TO DRAW A RECTANGLE)",(20,405), font, 0.6,(255,255,255),2,cv2.LINE_AA)
        self.r = cv2.selectROI(frame)
        cv2.destroyWindow("ROI selector")

    # Create a previous frame and thresh to be used for comparison on first frames only
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
            self.timeFrozen+=self.mspf
            return False
        else:
            self.timeFrozen+=self.mspf
            return True

    # Timing stuff
    # Go from milliseconds to time string
    def milliToTime(self, milliseconds):
        seconds = (milliseconds/1000) % 60
        minutes = (milliseconds/(1000*60)) % 60
        hours = (milliseconds/(1000*60*60)) % 24
        return str(int(hours)) + ":" + str(int(minutes)) + ":" + str(seconds)
    # Go from time string to milliseconds
    def timeToMilli(self, s):
        s = s.replace(".",":")
        hours, minutes, seconds, milliseconds = s.split(":")
        return int(hours)*60*60*1000 + int(minutes)*60*1000 + int(seconds)*1000 + int(milliseconds)

def runVid(q, back_q):
    vid = Vid(0, q ,back_q)

    if not vid.capError:
        vid.run()
        vid.close()
        return
    else:
        print('error opening video')

print('freezeAlg Loaded')

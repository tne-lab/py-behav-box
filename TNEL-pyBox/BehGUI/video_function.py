import cv2
import time

class Vid:
    def __init__(self, videoPath, q, back_q, winName = 'vid'):
        self.cap = cv2.VideoCapture(videoPath)
        self.winName = winName
        self.q = q
        self.back_q = back_q
        self.out = None
        self.outPath = ''

        self.CAMERA_ON = False
        self.RECORD = False
        self.FLIP = False

        self.ROIenabled = False
        self.ROIstr = ""
        self.ROIGEN = True
        #self.ROI = (0,0,0,0)
        self.freezeEnable = False
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
            self.exptStarted = False
            #self.initROIFrames()
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
        if self.ROIGEN:
            self.genROI(frame)
        # Gen prev frame and threshold (Use size of ROI)
        self.startFrame+=1
        ret, newFrame = self.cap.read()
        if not ret:
            print('frame read error')
            return
        frameROI = frame[int(self.ROI[1]):int(self.ROI[1]+self.ROI[3]),int(self.ROI[0]):int(self.ROI[0] + self.ROI[2])]
        newFrameROI = newFrame[int(self.ROI[1]):int(self.ROI[1]+self.ROI[3]),int(self.ROI[0]):int(self.ROI[0] + self.ROI[2])]
        self.genPrev(newFrameROI, frameROI)
        self.ROIenabled = True
        self.freezeEnable = True

#######################################################################################
#######################################################################################
    # Call this every loop
    def run(self):
        while(self.cap.isOpened()):
            vid_cur_time = time.perf_counter()
            #Get frame
            ret, frame = self.cap.read()
            if self.FLIP:
                frame = cv2.flip(frame,flipCode = 0)# flipcodes: 1 = hflip, 0 = vflip

            # Run video
            try:
                msg = self.q.pop()
                time_from_GUI = msg['cur_time']
                self.FLIP = msg['FLIP']
                STATE = msg['STATE'] # NOTE: NOTE: STATE = (ON,OFF,  REC_VID,REC_STOP, START_EXPT,STOP_EXPT)
                if STATE == 'ON':
                    self.CAMERA_ON = True
                if STATE == 'OFF':
                    self.CAMERA_ON = False
                    self.RECORD = False
                if STATE == 'START_EXPT':
                    self.exptStarted = True
                if STATE == 'REC_VID':
                    self.RECORD = True
                if STATE == 'REC_STOP':
                    #self.exptStarted = False
                    self.RECORD = False
                if 'ROI' in msg and not self.ROIenabled:
                    if msg['ROI'] in 'GENERATE':
                        self.ROIGEN = True
                        self.initROIFrames()
                    else: # NOTE: ROI sent from PROTOCOL file
                        self.ROIstr = msg['ROI']
                        ROIstr = msg['ROI'][1:-1] #Remove first and last char "(" and ")" from (x,y,width,height)
                        ROIlist = ROIstr.split(",")
                        self.ROI = [int(x) for x in ROIlist]
                        self.ROIGEN = False
                        self.initROIFrames()



                msg['time_diff'] = vid_cur_time - time_from_GUI
                msg['vid_time'] = vid_cur_time
                if self.RECORD:
                    if msg['PATH_FILE'] != self.outPath:
                        self.openOutfile(msg['PATH_FILE'], self.cap.get(4) , self.cap.get(3))
            except IndexError:
                #print("Error in run()")
                pass

            if not ret:
                print('error in getting read')
                return

            # Grab only ROI
            if self.ROIenabled:
                imgWithinROI = frame[int(self.ROI[1]):int(self.ROI[1]+self.ROI[3]),int(self.ROI[0]):int(self.ROI[0] + self.ROI[2])]
                #Make gray and blur
                gray = cv2.cvtColor(imgWithinROI, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

            #if self.freezeEnable: if ROIenabled then Freeze is also enabled
                movingPxls = self.calcMovingPixels(gray)

                # Moving or frozen?
                ######!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FIX THIS
                if movingPxls > 100: #NOTE:   THIS SHOULD BE VALUE SENT FROM CALIBRATION OR FROM PROTOCOL
                    self.text = 'move'
                    self.timeFrozen = 0
                    if self.isFrozen:
                        self.isFrozen = False
                        try:
                            self.freezeFile.write('end freeze: ' + str(self.milliToTime(self.cap.get(0))) + '\n')
                        except: print("Freeze file closed")
                        #back_q.put({'FREEZE' : False, 'TIME' : time_from_GUI})
                else:
                    if self.checkFreeze() and not self.isFrozen:
                        self.isFrozen = True
                        try:
                            self.freezeFile.write('freeze: ' + str(self.milliToTime(self.cap.get(0))) + '\n')
                        except: print("Freeze file closed")
                        #back_q.put({'FREEZE' : True, 'TIME' : time_from_GUI})
                        self.text = 'freeze'

                cv2.putText(self.prevThresh,"Moving Pixels = " + str(movingPxls),(20,430), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2,cv2.LINE_AA)
                cv2.moveWindow('thresh',1400,30)# window, x, y. x = 1024 (touchscree w) + gui width =
                cv2.imshow('thresh',self.prevThresh)

            # Write stuff on screen (need to add trial number and probably not time differential)
            self.drawInfo(msg['cur_time'], str(msg['trial_num']), frame)
            #self.writeStuff(msg['cur_time'], msg['vid_time'], msg['time_diff'], movingPxls, frame)
            # draw trial start circle
            #print("STATE",msg['STATE'])
            #if self.ROIenabled:  print("ROI: ", self.ROI)
            if msg['STATE'] == 'START_EXPT': # NOTE: STATE = (ON,OFF, FLIP, REC_VID,REC_STOP, START_EXPT,STOP_EXPT)

                #if self.FLIP:
                #    recframe = cv2.flip(frame,flipCode = 0)# flipcodes: 1 = hflip, 0 = vflip
                #else:
                #    recframe = frame# flipcodes: 1 = hflip, 0 = vflip
                if self.RECORD:
                    self.out.write(frame)
            if msg['STATE'] == 'REC_STOP': # NOTE: STATE = (ON,OFF,  REC_VID,REC_STOP, START_EXPT,STOP_EXPT)
                self.out.release() # CLOSE VIDEO FILE
                #self.out.close()
                self.freezeFile.close()
                self.RECORD = False

            # Show the frames
            cv2.imshow(self.winName,frame)

            # Create dict to send back to main GUI
            if self.ROIenabled:
                backDict = {'vid_time':vid_cur_time, 'FROZEN':self.isFrozen, 'NIDAQ_time':time_from_GUI, 'Vid-NIDAQ':msg['time_diff'], 'ROI':self.ROIstr}
            else:
                backDict = {'vid_time':vid_cur_time, 'FROZEN':self.isFrozen, 'NIDAQ_time':time_from_GUI, 'Vid-NIDAQ':msg['time_diff']}
            self.back_q.put(backDict)

            # Get next frame and check if we are done
            self.startFrame+=1
            if cv2.waitKey(self.mspf) & 0xFF == ord('q'):
                self.close()
                return

            if msg['STATE'] == 'OFF': #  # NOTE: STATE = (ON,OFF, REC_VID,REC_STOP, START_EXPT,STOP_EXPT)
                self.close()
                return


################################################################################################
################################################################################################

    def openOutfile(self, path, height, width):
        self.outPath = path
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # for AVI files
        print(1.0/self.mspf * 1000)
        self.out = cv2.VideoWriter(path,fourcc, 1.0/self.mspf * 1000, (int(width),int(height)))
        print("SAVING TO: ", path, " in video_function.py line 215\n\n")

    def mouse_callback(self, event, x, y, flags, params):
        if event == 2:
            self.clicks = int(self.frame[x, y])
### #set mouse callback function for window
#cv2.setMouseCallback('image', mouse_callback)

    # Close everything
    def close(self):
        self.freezeFile.close()
        self.cap.release()
        self.out.release()
        #self.out.close()
        cv2.destroyAllWindows()
        for i in range(1,10):
            cv2.waitKey(1)

    ### Helper Functions ###


    # Update screen info
    def drawInfo(self, time_from_GUI, trial_num, frame):
        if self.exptStarted:
            cv2.circle(frame, (30,455), 20, (0,255,0) ,thickness = -1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        #print("NIDAQ time = " + str(round(time_from_GUI,3) ))
        cv2.putText(frame,"NIDAQ time = " + str(round(time_from_GUI,3)),(20,405), font, 0.5,( 255,0,0),2,cv2.LINE_AA)
        cv2.putText(frame, self.text, (10, 50),font, .5, (255, 255, 255), 2)
        cv2.putText(frame, "Trial Number = " + str(trial_num), (20, 425),font, .5, ( 255, 0,0), 2,cv2.LINE_AA)

    # Wrtie a ton of stuff on frames...
    def writeStuff(self, time_from_GUI, vid_time, time_diff, movingPxls, frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,"NIDAQ time = " + str(round(time_from_GUI,3)),(20,405), font, 0.5,(255,0,0),2,cv2.LINE_AA)
        cv2.putText(frame,"Video time = " + str(round(vid_time,3)),(20,430), font, 0.5,(255,0,0),2,cv2.LINE_AA)
        cv2.putText(frame,"time diff = " + str(time_diff),(20,455), font, 0.5,(255,0,0),2,cv2.LINE_AA)
        cv2.putText(frame, self.text, (10, 50),font, .5, (255, 255, 255), 2)
        cv2.putText(self.prevThresh,"Moving Pixels = " + str(movingPxls),(20,430), font, 0.5,(255,0,0),2,cv2.LINE_AA)
        cv2.putText(self.prevThresh, "Time frozen = " + str(self.timeFrozen), (100, 50),font, .5, ( 255,0,0), 2)
        cv2.putText(self.prevThresh, "Current frame = " + str(self.startFrame), (10,95), font, .5,( 255,0,255),2)
        cv2.putText(self.prevThresh, "Number of frames = " + str(self.length), (10,110), font, .5, ( 255,0,0),2)

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
        if self.FLIP:
            frame = cv2.flip(frame,flipCode = 0)# flipcodes: 1 = hflip, 0 = vflip
        cv2.putText(frame,"SELECT REGION OF INTEREST (CLICK AND DRAG MOUSE TO DRAW A RECTANGLE)",(20,405), font, 0.4,(0,255,0),2,cv2.LINE_AA)
        ROI = cv2.selectROI(frame) #NOTE: NOT A STR, but tupple of 4 numbers: (x,y,w,h)
        self.ROIstr = str(ROI)
        #print("ROI CONVERTED TO STR",self.ROIstr )
        cv2.destroyWindow("ROI selector")
        self.ROI = [int(x) for x in ROI]

        #print("###############################")
        #print("#    ROI: ",self.ROI,"          #")
        #print("###############################")
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

def runVid(q, back_q): # THIS TURNS ON MAIN Camera (if available)
    vid = Vid(0, q ,back_q)

    if not vid.capError:
        vid.run()
        vid.close()
        return
    else:
        print('error opening video in video funcion.py')

def runSimpleVid(q):# THIS TURNS ON 2nd Camera (if available)
    simpleVid = SimpleVid(1,q) # 0 is the camera number

    if not simpleVid.capError:
        simpleVid.run()
        return

class SimpleVid:
    def __init__(self,path,q):
        self.cap = self.cap = cv2.VideoCapture(path)
        self.q = q
        self.capError = False
        self.outPath = 'NOT SET'
        self.rec = False
        self.FLIPAUX = False
        self.out = None

        if not self.cap.isOpened():
            print('error opening aux vid, probably doesn\'t exist')
            self.capError = True

    def run(self):
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if self.FLIPAUX:
                frame = cv2.flip(frame,flipCode = 0)# flipcodes: 1 = hflip, 0 = vflip
            if not ret:
                print('Error loading frame, probably last frame')
                return
            # Show the frame
            cv2.imshow('Aux Camera', frame)

            if self.rec:
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.out.write(grayFrame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                self.cap.release()
                self.out.release()
                return

            if not self.q.empty():
                msg = self.q.get()
                if msg['STATE'] == 'OFF':
                    cv2.destroyAllWindows()
                    self.cap.release()
                    self.out.release()
                    return
                if msg['STATE'] == 'REC_STOP' and self.rec == True:
                    self.out.release()
                    self.rec = False
                    continue
                if msg['PATH_FILE'] != self.outPath:
                    self.openOutfile(msg['PATH_FILE'], self.cap.get(4) , self.cap.get(3))
                    self.rec = True
                if msg['FLIPAUX']: self.FLIPAUX = msg['FLIPAUX']

    def openOutfile(self, path, height, width):
        self.outPath = path
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # for AVI files
        self.out = cv2.VideoWriter(path,fourcc, 30, (int(width),int(height)))

print('freezeAlg Loaded')

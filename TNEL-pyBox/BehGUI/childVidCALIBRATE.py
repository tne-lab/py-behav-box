from multiprocessing import Process,Queue
from collections import deque
import numpy as np
import cv2
import time
from numpy import array, float32

### Check if camera opened successfully
##if (cap.isOpened()== False):
##    print("")
##    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
##    print("Error opening video stream or file")
##else: length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
startFrame = 0
threshVal = 0
max_moving_pix = 500
min_val = 0
max_val = 0
cap = cv2.VideoCapture('C:\\Users\\ephys-2\\Desktop\\FLAVsSTUFF\\DATA\\FREEZE_CALIBRATE\\FR_con1.avi') #
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
spf = 1/fps
frameRate = int(1000*spf)
print (fps)



##    cv.THRESH_BINARY
##    cv.THRESH_BINARY_INV
##    cv.THRESH_TRUNC
##    cv.THRESH_TOZERO
##    cv.THRESH_TOZERO_INV
def myThresholdAdaptive(img):
    #adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, theshold type, blocksize, constant subtracted from mean)
    return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

def smooth(gray):
    gray_smooth = cv2.GaussianBlur(gray,(11,11),0)
    return gray_smooth
    
def sharpen(img):
    kernel = array([[-1, -1, -1],
                    [-1,  9, -1],
                    [-1, -1, -1]])
    return cv2.filter2D(img ,-1,kernel) # ddepth = -1, means destination image has depth same as input image.

# EDGE
def canny_edges(img,min_val,max_val):
    return cv2.Canny(img,min_val,max_val,apertureSize = 3)

# HORIZONTAL
def horizontalEdges5X5(img):
    kernel = np.array([ [-1, -1, -1, -1, -1],
                        [-1, -1, -1, -1, -1],
                        [  4, 4,  4,  4,  4],
                        [-1, -1, -1, -1, -1],
                        [-1, -1, -1, -1, -1] ],np.float32) # kernel should be floating point type.
    return cv2.filter2D(img ,-1,kernel) # ddepth = -1, means destination image has depth same as input image.

def horizontalEdges(img):
    kernel = array([ [-1, -1,-1],
                     [ 2,  2, 2],
                     [-1, -1,-1] ]) # kernel should be floating point type.
    return cv2.filter2D(img ,-1,kernel) # ddepth = -1, means destination image has depth same as input image.

# VERTICAL
def verticalEdges5X5(img):
    kernel = np.array([ [ 0, 0,-2, 0, 0],
                        [ 0, 0,-1, 0, 0],
                        [ 0, 0, 6, 0, 0],
                        [ 0, 0,-1, 0, 0],
                        [ 0, 0,-2, 0, 0] ],np.float32) # kernel should be floating point type.
    return cv2.filter2D(img ,-1,kernel) # ddepth = -1, means destination image has depth same as input image.
def verticalEdges(img):
    kernel = array([ [-1, 2,-1],
                     [-1, 2,-1],
                     [-1, 2,-1] ]) # kernel should be floating point type.

                     #[-1, -1,-1] ],float32) # kernel should be floating point type.
    return cv2.filter2D(img ,-1,kernel) # ddepth = -1, means destination image has depth same as input image.

def nothing(x):
    pass 

def minCannyVal(x):
    global min_val
    min_val = cv2.getTrackbarPos('min_value', 'gray_smooth')
    
def maxCannyVal(x):
    global max_val
    max_val = cv2.getTrackbarPos('max_value', 'gray_smooth')
    
def picFrame(x):
    global startFrame, cap
    startFrame=cv2.getTrackbarPos("StartFrame", "gray_smooth")
    cap.set(1,startFrame)
    #print("TRACKBAR POS: ",startFrame)

def thresholding(x):
    global threshVal
    threshVal=cv2.getTrackbarPos("Threshold", "gray_smooth")

def SetMinMovingPixels(x):
    global max_moving_pix
    max_moving_pix=cv2.getTrackbarPos("MinMovingPix", "gray_smooth")
    



    
def vidCapture(q,back_q):
    global startFrame,threshVal,max_moving_pix,min_val,max_val,  cap
    freeze_time= 2 #sec
    
    cv2.namedWindow('vidWindow')
    cv2.namedWindow('diff')
    cv2.namedWindow("gray_smooth")
    backDict={}
    print('In child video')
    #cap = cv2.VideoCapture(0) # (0) specifies the camera
    

    font = cv2.FONT_HERSHEY_SIMPLEX
    #cv.CreateTrackbar(trackbarName, windowName, value, count, onChange) 
    cv2.createTrackbar("StartFrame", "gray_smooth",0,length,picFrame)# The last param 'picFrame' is to run a function, but we dont need one
    cv2.createTrackbar("Threshold", "gray_smooth",0,255,thresholding)# The last param 'thresholding' is to run a function, but we dont need one
    cv2.createTrackbar("MinMovingPix", "gray_smooth",0,200000,SetMinMovingPixels)# The last param 'SetMinMovingPixels' is to run a function, but we dont need one
    startFrame=cv2.getTrackbarPos("StartFrame", "gray_smooth")
    threshVal = cv2.getTrackbarPos("Threshold", "gray_smooth")
    max_moving_pix = cv2.getTrackbarPos("max_moving_pix", "gray_smooth")
    
    cv2.createTrackbar('min_value','gray_smooth',0,500,minCannyVal)
    cv2.createTrackbar('max_value','gray_smooth',0,500,maxCannyVal)



    try:
        text = q.pop()
    except:
        print ("Epty deque")
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # for AVI files
    out = cv2.VideoWriter(text['PATH_FILE'],fourcc, 20.0, (640,480))

    print("SAVING TO: ",text['PATH_FILE'])

    
    ret, frame = cap.read()
    # Select ROI
    r = cv2.selectROI(frame)
    # Crop image
    imgROI = frame[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0] + r[2])]
    #prev_gray = cv2.cvtColor(imgROI , cv2.COLOR_BGR2GRAY)
    #prev_gray_smooth = smooth(prev_gray)
    #kernel = np.ones((5,5),np.float32)/25
    #kernelBlur = cv2.filter2D(imgROI,-1,kernel)

    cv2.waitKey(0)
    cv2.destroyWindow("ROI selector")
    cv2.destroyWindow("image")
    cv2.destroyWindow('vidWindow')
       
    STILL = False
    FROZEN = False
    moving_pixels = 0.0
    moving_pix_run = []
    moving_pix_sum = 0
    mean_moving_pix = 0.0
    loops = 1
    while(True):
        startFrame +=1
        vid_cur_time = time.perf_counter()
        # ROI ON PREV IMAGE
        imgROI = frame[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0] + r[2])] 
        
        prev_gray = cv2.cvtColor(imgROI , cv2.COLOR_BGR2GRAY)
        prev_gray_smooth = smooth(prev_gray)
        
        prev_grayThresh = myThresholdAdaptive(prev_gray_smooth)
        prev_horizEdges = horizontalEdges(prev_gray)
        prev_horizEdges5 = horizontalEdges5X5(prev_gray)
        prev_cannyEdges = canny_edges(prev_gray,min_val,max_val)
        
        prev_edgesH = smooth(cv2.subtract(prev_gray_smooth,smooth(prev_horizEdges)))
        prev_edgesH5 = smooth(cv2.subtract(prev_gray_smooth,smooth(prev_horizEdges5)))
        #prev_keep_edges = 
        
        # ROI ON CURRENT IMAGE
        ret, frame = cap.read() # Returns a T or F boolean and frame
        imgROI = frame[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0] + r[2])]

        gray = cv2.cvtColor(imgROI , cv2.COLOR_BGR2GRAY)
        gray_smooth = smooth(gray)
        gray_col = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
        
        grayThresh = myThresholdAdaptive(gray_smooth)
        horizEdges = horizontalEdges(gray)
        horizEdges5 = horizontalEdges5X5(gray)
        cannyEdges = canny_edges(gray,min_val,max_val)
        
        edgesH =  smooth(cv2.subtract(gray_smooth,smooth(horizEdges)))
        edgesH5 =  smooth(cv2.subtract(gray_smooth,smooth(horizEdges5)))
        
        # DIFFERENCES
        diff = cv2.subtract(edgesH, prev_edgesH)
        diff5= cv2.subtract(edgesH5, prev_edgesH5)
        
        
        moving_pixels = cv2.countNonZero(diff)
        moving_pixels5 = cv2.countNonZero(diff5)
        
        moving_pix_sum += moving_pixels
        moving_pix_run.append(moving_pixels)

        # AVERAGE MOVING PIXELS
        if loops % 20 == 0: # divisible by 100
            #print(moving_pix_run[len(moving_pix_run)-20:])
            #print(sum(moving_pix_run[len(moving_pix_run)-20:]))
            mean_moving_pix = sum(moving_pix_run[len(moving_pix_run)-20:])/20.0
        
        loops += 1
        if moving_pixels < max_moving_pix: # Possibly freezing (freezing is 2 sec or more)
            if STILL:
                #tot_moving_pix = tot_moving_pix + moving_pixels
                tot_freeze_tm = vid_cur_time - freeze_start_tm
                if tot_freeze_tm > freeze_time:
                    FROZEN = True
                    
            else:
                STILL = True
                freeze_start_tm = vid_cur_time
        else:
            STILL = False
            FROZEN = False

        try:
            text = q.pop()
            time_from_GUI = text['cur_time']
            STATE = text['STATE']
            #print('Child:',time_from_GUI)
        except:
            pass
            #print('empty queue')
        
        time_diff = vid_cur_time - time_from_GUI 
        #backDict = {'vid_time':vid_cur_time,'FROZEN':FROZEN}
        backDict = {'vid_time':vid_cur_time, 'FROZEN':FROZEN, 'NIDAQ_time':time_from_GUI, 'Vid-NIDAQ':time_diff}
        #print("childVid backDict",backDict)
        
        #back_q.append(backDict)

        try:
            back_q.append(backDict)
        except:
            print("Unable to send back FROZEN")
            
        if ret==True:
            if STATE == 'ON' or STATE == 'REC':
                #putText(img,text,(x,y),font,fontScale,color,thickness = 1, lineType = LINE_8,bool bottomLeftOrigin = false)
                if FROZEN:
                    cv2.putText(gray_col,"Frozen",(20,380), font, 0.5,(0,0,255),2,cv2.LINE_AA)        
                cv2.putText(gray_col,"NIDAQ time = " + str(time_from_GUI),(20,405), font, 0.5,(255,0,0),2,cv2.LINE_AA)
                cv2.putText(gray_col,"Video time = :" + str(round(startFrame*spf/60.0,4)),(20,430), font, 0.5,(255,0,0),2,cv2.LINE_AA)
                cv2.putText(gray_col,"time diff = :" + str(time_diff),(20,455), font, 0.5,(255,0,0),2,cv2.LINE_AA)
                cv2.imshow("orig",gray_col,)



                if STATE == 'REC':
                    out.write(gray_smooth_col) # Write to file

                cv2.imshow("gray_smooth",gray_smooth)
                cv2.imshow('diff', cv2.subtract(gray,prev_gray))
                cv2.imshow('diff2',cv2.subtract(gray_smooth,prev_gray_smooth))
                
                cv2.imshow('diff3',cv2.subtract(cv2.add(gray_smooth,smooth(horizEdges5)),cv2.add(prev_gray_smooth,smooth(prev_horizEdges5))))

                prev_canny_diff = cv2.subtract(smooth(prev_horizEdges5),smooth(prev_cannyEdges))
                canny_diff = cv2.subtract(smooth(horizEdges5),smooth(cannyEdges))
                cv2.imshow('cannydiff',canny_diff)
                cv2.imshow('diff4',cv2.subtract(cv2.subtract(gray_smooth,canny_diff),cv2.subtract(prev_gray_smooth,prev_canny_diff)))

                diffcol = cv2.cvtColor(cv2.subtract(gray_smooth,prev_gray_smooth),cv2.COLOR_GRAY2BGR)
                cv2.putText(diffcol,"Moving Pixels = " + str(moving_pixels),(20,20), font, 1.0,(255,0,0),2,cv2.LINE_AA)
                cv2.putText(diffcol,"Moving Pixels5 = " + str(moving_pixels5),(20,20), font, 1.0,(255,0,0),2,cv2.LINE_AA)
                cv2.putText(diffcol,"mean Moving Pixels = " + str(mean_moving_pix),(20,45), font, 1.0,(255,0,0),2,cv2.LINE_AA)                
                

                #cv2.imshow('edges',edges)
                cv2.imshow('Hirizedges',horizEdges)
                cv2.imshow('Hirizedges5',horizEdges5)
                cv2.imshow('cannyedges',cannyEdges)
                
                #cv2.imshow("smooth-diff",cv2.subtract(gray_smooth,cv2.subtract( smooth(horizEdges5),smooth(cannyEdges))))
                #cv2.imshow('Thresh',thresh)
                #cv2.imshow("gray_smooth",gray_smooth)
                if cv2.waitKey(frameRate) & 0xFF == ord('q'): # Press 'Q' to quit
                    break
            if STATE == 'STOP':
                break

        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    #conn.close()

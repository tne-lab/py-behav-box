from multiprocessing import Process,Queue
from collections import deque
import numpy as np
import cv2
import time

# Define the codec and create VideoWriter object

def vidCapture(q,back_q):
    backDict={}
    print('In child video')
    cap = cv2.VideoCapture(0) # (0) specifies the camera

    font = cv2.FONT_HERSHEY_SIMPLEX

    try:
        text = q.pop()
    except:
        print ("Epty deque")
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # for AVI files
    out = cv2.VideoWriter(text['PATH_FILE'],fourcc, 20.0, (640,480))
    # NOTE: FOURCC is short for "four character code" - an identifier for a video codec, compression format, color or pixel format
    #       used in media files
    #
    #     FourCC is a 4-byte code used to specify the video codec. The list of available codes can be found in fourcc.org.
    #     It is platform dependent. 
    #     fourcc = cv2.cv.CV_FOURCC('M','S','V','C') # compression quality is set to it's maximum. 
    #     fourcc = -1 # a Windows Video Compression dialog box opens which allows the user to select
    #              a video compression AND set 

    print("SAVING TO: ",text['PATH_FILE'])
    ret, frame = cap.read() 
    #while(cap.isOpened()):
    STILL = False
    FROZEN = False
    tot_moving_pix = 0.0
    while(True):
        vid_cur_time = time.perf_counter()
        prev_gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        ret, frame = cap.read() # Returns a T or F boolean and frame
        gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        diff = cv2.subtract(gray , prev_gray)
        ret1,thresh = cv2.threshold(diff,50,255,cv2.THRESH_BINARY)
        moving_pixels = cv2.countNonZero(thresh)
        if moving_pixels < 200: # Possibly freezing (freezing is 2 sec or more)
            if STILL:
                #tot_moving_pix = tot_moving_pix + moving_pixels
                tot_freeze_tm = vid_cur_time - freeze_start_tm
                if tot_freeze_tm > 2.0:
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
    	
                cv2.putText(frame,"NIDAQ time = " + str(time_from_GUI),(20,405), font, 0.5,(255,255,255),2,cv2.LINE_AA)
                
                cv2.putText(frame,"Video time = :" + str(vid_cur_time),(20,430), font, 0.5,(255,255,255),2,cv2.LINE_AA)
                cv2.putText(frame,"time diff = :" + str(time_diff),(20,455), font, 0.5,(255,255,255),2,cv2.LINE_AA)

                cv2.putText(thresh,"Moving Pixels = " + str(moving_pixels),(20,430), font, 0.5,(255,255,255),2,cv2.LINE_AA)

                if FROZEN:
                    cv2.putText(frame,"Frozen",(20,380), font, 0.5,(255,255,255),2,cv2.LINE_AA)
                if STATE == 'REC':
                    out.write(frame) # Write to file

                cv2.imshow('frame',frame)
                cv2.imshow('diff',thresh)
                #cv2.imshow('gray ',gray)
                if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'Q' to quit
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

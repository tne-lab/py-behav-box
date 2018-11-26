from multiprocessing import Process,Queue
from collections import deque
import numpy as np
import cv2
import time
import freezeAlg

# Define the codec and create VideoWriter object

def vidCapture(q,back_q):
    backDict={}
    print('In child video')
    cap = cv2.VideoCapture('FR1_con1.avi') # (0) specifies the camera
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Get path from parent
    try:
        text = q.pop()
    except:
        print ("Epty deque")
    # Create recording vid
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # for AVI files
    out = cv2.VideoWriter(text['PATH_FILE'],fourcc, 20.0, (640,480))

    print("SAVING TO: ",text['PATH_FILE'])

    # Create video class
    vid = freezeAlg.Vid('FR_con1.avi','vid')
    if not vid.capError:
        # Create class and gen initial stuff
        vid.trackBar('vid','frameNumber',0, vid.length)
        ret, frame = vid.cap.read()
        vid.genROI(frame)
        re, newFrame = vid.cap.read()
        vid.genPrev(newFrame, frame)

        while(vid.cap.isOpened()):
            vid_cur_time = time.perf_counter()
            # Run video
            try:
                msg = q.pop()
                time_from_GUI = msg['cur_time']
                STATE = msg['STATE']
            except:
                pass

            time_diff = vid_cur_time - time_from_GUI
            backDict = {'vid_time':vid_cur_time, 'FROZEN':vid.isFrozen, 'NIDAQ_time':time_from_GUI, 'Vid-NIDAQ':time_diff}

            vid.run(msg)

            try:
                back_q.append(backDict)
            except:
                print("Unable to send back FROZEN")
                
            vid.close()

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

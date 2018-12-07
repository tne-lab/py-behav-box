from multiprocessing import Process,Queue
from collections import deque
import numpy as np
import cv2
import time

# Define the codec and create VideoWriter object
EXPT_FILE_LOADED = False
def do_protocol(pq,back_pq):
    print('In child protocol')
    msgFromGUI = pq.pop()

    
##            text = q.pop()
##            time_from_GUI = text['cur_time']    
##    if EXPT_FILE_LOADED:
##        load_expt_file()
    
    protoDict={}


    msgFromGUI = pq.pop()
    print(msgFromGUI)
        

    backDict = {{"FAN_ON":True,"CAB_LIGHT":True, "CAMERA": True, "REC":True,"FOOD_LIGHT":True,
                 "EXTEND_LEVERS":True, "CONDITIONS":{}}
    try:
        back_q.append(backDict)
    except:
        print("Unable to send back backDict")
            
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

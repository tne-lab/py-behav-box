from multiprocessing import Process,Queue
import numpy as np
import cv2
import time
import json
import zmq


# Define the codec and create VideoWriter object

def vidCapture(q):

    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = 'Change me!'
    while(cap.isOpened()):
        cur_time = str(time.perf_counter())
        ret, frame = cap.read()

        if q.empty() == False:
            text = q.get(False)


        if ret==True:
            #frame = cv2.flip(frame,0)
            cv2.putText(frame,text,(20,435), font, 1,(255,255,255),2,cv2.LINE_AA)
            cv2.putText(frame,cur_time,(20,465), font, 1,(255,255,255),2,cv2.LINE_AA)
            # write the frame
            #out.write(frame) # Write to file

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'Q' to quit
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    #conn.close()

from collections import deque
import cv2
import time

import freezeAlg

def vidCapture(q,back_q):
    print('In child video')

    # Get path from parent thread
    try:
        text = q.pop()
    except:
        print('recording path not in queue')
        return

    # Define the codec and create VideoWriter object
    # Create recording vid
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # for AVI files
    outfile = cv2.VideoWriter(text['REC_FILE'],fourcc, 20.0, (640,480))
    print("SAVING TO: ",text['REC_FILE'])

    # Create video class
    # Need path to vid or 0 for camera
    vid = freezeAlg.Vid(0)
    if not vid.capError:
        # Make ROI

        # Run the video thread
        vid.run(q, back_q, outfile)
        return
    else:
        print('error opening video')

from collections import deque
import cv2
import time

import freezeAlg

def vidCapture(q,back_q):
    print('In child video')

    # Get path from parent thread
    # Define the codec and create VideoWriter object
    # Create recording vid


    # Create video class
    # Need path to vid or 0 for camera
    vid = freezeAlg.Vid(0, q ,back_q)
    if not vid.capError:
        # Make ROI

        # Run the video thread
        vid.run()
        return
    else:
        print('error opening video')

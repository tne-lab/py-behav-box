from collections import deque
import cv2
import time
import freezeAlg

def vidCapture(q,back_q):
    backDict={}
    print('In child video')

    # Get path from parent thread
    try:
        print('hello')
        text = q.pop()
        print(text)
    except:
        print('recording path not in queue')

    # Define the codec and create VideoWriter object
    # Create recording vid
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # for AVI files
    out = cv2.VideoWriter(text['PATH_FILE'],fourcc, 20.0, (640,480))
    print("SAVING TO: ",text['PATH_FILE'], " in child Vid2 line 22.")

    # Create video class
    vid = freezeAlg.Vid(0,'vid')
    if not vid.capError:
        # Make ROI
        ret, frame = vid.cap.read()
        if not ret:
            print('frame read error')
            return
        vid.genROI(frame)

        # Gen prev frame and threshold (Use size of ROI)
        vid.startFrame+=1
        ret, newFrame = vid.cap.read()
        if not ret:
            print('frame read error')
            return
        frameROI = frame[int(vid.r[1]):int(vid.r[1]+vid.r[3]),int(vid.r[0]):int(vid.r[0] + vid.r[2])]
        newFrameROI = newFrame[int(vid.r[1]):int(vid.r[1]+vid.r[3]),int(vid.r[0]):int(vid.r[0] + vid.r[2])]
        vid.genPrev(newFrameROI, frameROI)

        # Run the video thread
        vid.run(q, back_q, out)

        return

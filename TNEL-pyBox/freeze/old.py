    cv2.namedWindow('vid')
    cap = cv2.VideoCapture('FR_con1.avi')
    frameNumber = 0
    cv2.createTrackbar("frameNumber", "vid",0,255, picFrame)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.cv2.CAP_PROP_FPS)

    #Start at frame 0
    cap.set(1,frameNumber)

    while(cap.isOpened()):
        #Set and read frame
        frameNumber = cv2.getTrackbarPos("frameNumber",'vid')
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frameNumber+=1
        cv2.imshow('vid',gray)

        if cv2.waitKey(int((1/fps)*1000)) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

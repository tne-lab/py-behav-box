from groomingClass import GroomingVid
import collections
from queue import Queue
import threading
import time

## 11:10 has a good grooming image!

def main():
    gr = GroomingVid('/home/ephys/Documents/groom.avi')
    gr.genROI()

    time.sleep(0.2)


    q = collections.deque(maxlen = 1)
    back_q = Queue()

    p = threading.Thread(target=gr.run, args=(q,back_q,))
    dict = {'STATE' : 'ON', 'cur_time' : time.perf_counter()}
    q.append(dict)
    p.start()

    while True:
        if not p.isAlive():
            break
        time.sleep(.01)
        dict = {'STATE' : 'ON', 'cur_time' : time.perf_counter()}
        q.append(dict)
        try:
            back = back_q.pop()
            print(back)
        except:
            continue


if __name__ == "__main__":
    main()



'''
    (H, W) = (None, None)


    cap = cv2.VideoCapture(videoPath)
    while cap.isOpened():
        # read the next frame from the video stream and resize it
    	frame = vs.read()
    	frame = imutils.resize(frame, width=400)
        gr.genROI(frame)
    	# if the frame dimensions are None, grab them
    	if W is None or H is None:
    		(H, W) = frame.shape[:2]

        #### CHANGE OUR OBJECT DETECTION ############################
        # Kind o flike USURF with a color mask on hands
        # sift(too slow? U-SURF(unsigned stuff) - not open source oh no
        # FAST_FEATURE DETECTOR, BRIEF, ORB?, FEATURE MATCHING (FLANN or BRUTE FORCE)
    	# construct a blob from the frame, pass it through the network,
    	# obtain our output predictions, and initialize the list of
    	# bounding box rectangles
    	blob = cv2.dnn.blobFromImage(frame, 1.0, (W, H),
    		(104.0, 177.0, 123.0))
    	net.setInput(blob)
    	detections = net.forward()
    	rects = []
    	for i in range(0, detections.shape[2]):
    		# filter out weak detections by ensuring the predicted
    		# probability is greater than a minimum threshold
    		if detections[0, 0, i, 2] > args["confidence"]:
    			# compute the (x, y)-coordinates of the bounding box for
    			# the object, then update the bounding box rectangles list
    			box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
    			rects.append(box.astype("int"))

    			# draw a bounding box surrounding the object so we can
    			# visualize it
    			(startX, startY, endX, endY) = box.astype("int")
    			cv2.rectangle(frame, (startX, startY), (endX, endY),
    				(0, 255, 0), 2)

        objects = gr.update(rects)
    	# loop over the tracked objects
        for (objectID, centroid) in objects.items():
    		# draw both the ID of the object and the centroid of the
    		# object on the output frame
    		text = "ID {}".format(objectID)
    		cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
    			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
        # show the output frame
    	cv2.imshow("Frame", frame)
    	key = cv2.waitKey(1) & 0xFF

    	# if the `q` key was pressed, break from the loop
    	if key == ord("q"):
    		break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
'''

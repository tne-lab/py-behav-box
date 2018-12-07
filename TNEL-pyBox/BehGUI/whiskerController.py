import whiskerTouch
import time
from multiprocessing import Process, Queue
import threading

def main():
    trialNum = 3
    # Note this is Queue() not deque(what we were using before) here. Simplier and easier to implement a FIFO
    whiskerQ = Queue(maxsize = trialNum + 1) # Might want to check this size to be correct and not losing trials..
    whiskerBack_q = Queue()

    
    # Init whisker thread (lots of optional args here, check main function to see them) (trial_length,ON_RESPONSE,media_dir...)
    whiskerThread = threading.Thread(target = whiskerTouch.main, args=(whiskerQ,whiskerBack_q), kwargs={'ON_RESPONSE': True})

    for i in range(0,trialNum):
        # Can change pics/xy however you would like
        whiskerQ.put({'end' : False, 'next' : True, 'pics': ['santa_fe.bmp','test.bmp'], 'XYarray' : [(0,100),(250,100)]})
    whiskerQ.put({'end' : True})

    # Start whisker thread after Q is full
    whiskerThread.start()

    # msg in form of => {'picture' : picName, 'XY' : (x,y)}
    for i in range(0,30):
        time.sleep(1)
        if whiskerBack_q.empty() == False:
            msg = whiskerBack_q.get()
            print("from parent", msg)


if __name__ == '__main__':
    main()

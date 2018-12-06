import childVid
from multiprocessing import Process, Queue
from datetime import datetime
import time, sys


def VideoOn(STATE):
    myDict = {'R_pad':'0'}
    q = Queue(1)
    p = Process(target=childVid.vidCapture, args=(q,))
    if STATE[0] == 'START':
        p.start()
        for i in range(0,1000):
            cur_time = time.perf_counter()
            print('cur_time: ',cur_time)
            myDict['R_pad'] = cur_time
            #x = input('Type to video: ')
            q.put(myDict)
    elif STATE[0] == 'STOP':
        p.terminate()
        print("videoOFF")
    
if __name__ == '__main__':
    VideoOn(sys.argv[1])

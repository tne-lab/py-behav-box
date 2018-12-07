import childVid
from multiprocessing import Process, Queue
from datetime import datetime
import time,sys

if __name__ == '__main__':
    myDict = {'R_pad':'0'}
    q = Queue(1)
    p = Process(target=childVid.vidCapture, args=(q,))
    p.start()
    for i in range(0,100):
        cur_time = time.perf_counter()
        print('cur_time: ',cur_time)
        myDict['R_pad'] = cur_time
        #x = input('Type to video: ')
        q.put(myDict)
    p.terminate()
    print("argv[0] = ", sys.argv[0])
    print("argv[1] = ",sys.argv[1])

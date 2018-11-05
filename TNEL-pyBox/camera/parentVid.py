import multiCamera
from multiprocessing import Process, Queue
from datetime import datetime
import time

if __name__ == '__main__':
    q = Queue()
    p = Process(target=multiCamera.run, args=(q,))
    p.start()
    for i in range(0,5):
        x = input('Type to video: ')
        dict = {'hello':time.perf_counter()}
        q.put(dict)
    p.terminate()

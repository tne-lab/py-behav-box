import childTest
from multiprocessing import Pipe
from queue import Queue
import threading
from datetime import datetime
import time
import pipes

import collections
timestamp = 0

def main():
    q = Queue(1)
    parentConn, childConn = Pipe(1)
    c = collections.deque(maxlen = 1)
    
    t = threading.Thread(target=childTest.run, args=(c,))
    t.start()
    for i in range(0,1000):
        print('time: ', time.perf_counter())
        c.append(time.perf_counter())
        time.sleep(.3)

import childVid
import threading
import time
import collections
from multiprocessing import Queue


def main():
    q = collections.deque(maxlen = 1)
    back_q = Queue()

    p = threading.Thread(target=childVid.vidCapture, args=(q,back_q,))
    q.append({'PATH_FILE':'recs/first.avi'})
    p.start()

    while True:
        if not p.isAlive():
            break
        time.sleep(.01)
        dict = {'STATE' : 'REC', 'cur_time' : time.perf_counter()}
        q.append(dict)
        try:
            back = back_q.pop()
            print(back)
        except:
            continue

if __name__ == '__main__':
        main()

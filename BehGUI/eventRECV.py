import zmqClasses

def rcv(back_q, q, flags = [b'event', b'ttl']): # NOTE : See line 38 in experiment.py to change flags
    rcv = zmqClasses.RCVEvent(5557, flags)

    while True:
        msg = rcv.rcv()
        if msg:
            back_q.put(msg)
        if not q.empty():
            return

if __name__ == "__main__":
    rcv()

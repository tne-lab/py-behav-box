import zmqClasses

def rcv(back_q, q, flags = [b'event']):
    rcv = zmqClasses.RCVEvent(5557, flags)

    while True:
        msg = rcv.rcv()
        if msg:
            back_q.put(msg)
        if not q.empty():
            break

if __name__ == "__main__":
    rcv()

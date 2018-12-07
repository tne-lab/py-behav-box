import zmqClasses

def rcv(q, back_q, flags = [b'event']):
    rcv = zmqClasses.RCVEvent(5557, flags)

    while True:
        back_q.put(rcv.rcv())
        if not q.empty():
            q.get()
            break

if __name__ == "__main__":
    rcv()

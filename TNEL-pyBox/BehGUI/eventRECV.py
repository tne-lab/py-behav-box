import zmqClasses

def rcv(back_q, flags = [b'event']):
    rcv = zmqClasses.RCVEvent(5557, flags)

    while True:
        back_q.put(rcv.rcv())

if __name__ == "__main__":
    rcv()

import zmqClasses

def main():
    rcv = zmqClasses.RCVEvent(5557, [b'event',b'spike'])

    for i in range(0,10):
        rcv.rcv()

main()

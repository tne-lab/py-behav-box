import zmqClasses

def main():
    rcv = zmqClasses.RCVEvent(5558, [b'event',b'spike', b'text', b'binary'])

    for i in range(0,10):
        rcv.rcv()

main()

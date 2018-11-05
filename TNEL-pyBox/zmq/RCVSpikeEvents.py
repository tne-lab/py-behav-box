import zmq
import numpy as np

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5557")
# 1 for data events , 2 for spikes!
socket.setsockopt(zmq.SUBSCRIBE, b'\x02\x00')

for request in range(10):
    print('waiting')

    recv = socket.recv_multipart()

    #skip raw data
    for part in recv[:-1]:
        print(part)

    print('\n')

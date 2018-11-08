import zmq
import numpy as np
from convertString import convertString

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5557")
# 1 for data events , 2 for spikes!
socket.setsockopt(zmq.SUBSCRIBE, b'\x01\x00')
socket.setsockopt(zmq.SUBSCRIBE, b'\x02\x00')

for request in range(10):
    print('waiting')

    recv = socket.recv_multipart()
    type = recv[0]
    if type == b'\x01\x00':
        eventData = {'type' : 'Event'}
    elif type == b'\x02\x00':
        eventData = {'type' : 'Spike'}


    eventData['timestamp'] =  convertString(recv[1].decode('utf-8'))

    #skip raw data
    for i in range(2,len(recv)-1,2):
        eventData[recv[i].decode('utf-8')] = convertString(recv[i+1].decode('utf-8'))

    print(eventData)
    print('\n')


#

'''
Event packet structure:
EventType - 1byte 0
SubType - 1byte 1
Source processor ID - 2bytes 3-4
Source Subprocessor index - 2 bytes 5-6
Source Event index - 2 bytes 7-8
Timestamp - 8 bytes 9-17
Event Virtual Channel - 2 bytes 18-20
data - variable 20+

The first bit of EventType will be set to 1
 when the event is recorded to avoid re-recording events.
  This will go away when the probe system is implemented.
'''

import zmq
import random
import codecs
import numpy as np
import struct

random.seed()

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5557")
socket.setsockopt(zmq.SUBSCRIBE, b'\x01\x00')
#  Do 10 requests, waiting each time for a response
for request in range(10):
    print('waiting')
    #  Get the reply.
    [type, timestamp, value, raw] = socket.recv_multipart()

    print("Received reply %s " % (request))
    print(timestamp)
    print(value)
    '''
    hex = raw.hex()
    num = int(hex,16)
    binary = bin(num)
    #floattime = struct.unpack('<d',bin(int(binary[69:133],2)).encode('utf-8')[2:])[0]
    #floattime = struct.pack('I',int(binary[66:130],2))
    #print(bin(int(binary[66:130],2)).encode('utf-8')[2:])
    print('EventType', binary[2:10])
    print('SubType', binary[11:18])
    print('Source Proc ID', binary[19:35])
    print('Source Subproc Index', binary [35:51])
    print('source Event Index', binary[52:68])
    print('timestamp', binary[69:133])
#    print('to float',floattime)
    print('event Virtual Channgel', binary[133:149] )
    print('data', binary[150:])
'''
    #codecs.decode(timestamp,'hex')
    #cleanTime = timestamp.decode('hex')
    #print(cleanTime)

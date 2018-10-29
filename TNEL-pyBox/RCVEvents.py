#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

'''
Event packet structure:
EventType - 1byte
SubType - 1byte
Source processor ID - 2bytes
Source Subprocessor index - 2 bytes
Source Event index - 2 bytes
Timestamp - 8 bytes
Event Virtual Channel - 2 bytes
data - variable

The first bit of EventType will be set to 1
 when the event is recorded to avoid re-recording events.
  This will go away when the probe system is implemented.
'''

import zmq
import random
import codecs

random.seed()

def createPacket():
    EventType = b'00000001'
    SubType = b'00000001'
    SourceID = b'0000000000000001'
    SourceSubIndex  = b'0000000000000001'
    Timestamp = b'0010000000100000001000000010000000100000001000000010000000100000'
    EventVirtualChannel = b'0000000000000001'
    data = bytearray(random.randint(0,10))
    return b"".join([EventType, SubType, SourceID, SourceSubIndex, Timestamp, EventVirtualChannel, data])

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5557")
socket.setsockopt(zmq.SUBSCRIBE, b'\x01\x00')
#  Do 10 requests, waiting each time for a response
for request in range(10):
    #print("Sending request %s ..." % request)
    #socket.send(createPacket())
    print('waiting')
    #  Get the reply.
    [type, timestamp, message] = socket.recv_multipart()
    print("Received reply %s [ %s ]" % (request, timestamp))
    time=''
    #for p in timestamp:
    #    time+=str(p)

    print(time)

    #print(message)
    #print(message)
    #codecs.decode(timestamp,'hex')
    #cleanTime = timestamp.decode('hex')
    #print(cleanTime)

import zmq

def switch(x):
    return {
    '0' : b'startAcquisition ',
    '1' : b'stopAcquisition ',
    '2' : b'getExperimentNumber',
    '3' : b'startRecord RecDir=C:\\Users\\Ephys\\Desktop\\RecDir PrependText=hello AppendText=',
    '4' : b'stopRecord'
    }[x]

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

#  Do 10 requests, waiting each time for a response
for request in range(5):
    print("Sending request %s ..." % request)
    control = input('0 : startAcquisition \n1 : stopAcquisition\n2 : getExperimentNumber\n3 : startRecord\n4 : stopRecord\n')
    socket.send(switch(control))

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))

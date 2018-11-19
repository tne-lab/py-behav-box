import zmq
import numpy as np
from convertString import convertString
import json


def parseJson(jsonStr):
    for key in jsonStr.keys():
        if type(jsonStr[key]) is dict:
            print(key + "\t")
            parseJson(jsonStr[key])
        else:
            print(key, ": ", jsonStr[key])

def main():
    context = zmq.Context()

    #  Socket to listen to OE
    print("Connecting to hello world server...")
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5557")
    #Have to Set to the beginning for the envelope!
    socket.setsockopt(zmq.SUBSCRIBE, b'event')
    socket.setsockopt(zmq.SUBSCRIBE, b'spike')

    for request in range(10):
        print('waiting')

        #Get raw input from socket
        envelope, jsonStr = socket.recv_multipart()
        print(envelope)

        #Our actual json object (last part)
        jsonStr = json.loads(jsonStr);
        parseJson(jsonStr)

        print('\n')
main()

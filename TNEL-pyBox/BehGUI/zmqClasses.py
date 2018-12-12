import zmq
import numpy as np
from convertString import convertString
import json

class RCVEvent:
    # SUBSCRIBE can be a list of vars, need to be in byte string format => b'spike'
    def __init__(self, port, SUBSCRIBE):
        print("Connecting recviever to Open Ephys \n")
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:" + str(port))
        self.socket.setsockopt(zmq.RCVTIMEO, 500)

        for sub in SUBSCRIBE:
            self.socket.setsockopt(zmq.SUBSCRIBE, sub)

    def rcv(self):
        try:
            #Get raw input from socket
            envelope, jsonStr = self.socket.recv_multipart()
            #print(envelope)

            #Our actual json object (last part)
            jsonStr = json.loads(jsonStr);
            #print(self.parseJson(jsonStr))
            #print(jsonStr)
            #print('\n')
            return jsonStr
        except:
            return False

    # First version of Json parser that breaks up the json object
    # Doesn't really do anything useful yet. Probably change this depending on how we want to do stuff
    def parseJson(self, jsonStr):
        for key in jsonStr.keys():
            if type(jsonStr[key]) is dict:
                print(key + "\t")
                self.parseJson(jsonStr[key])
            else:
                print(key, ": ", convertString(jsonStr[key]))
    # And this prints it out pretty
    def prettyJson(jsonStr, tab = ''):
        for key in jsonStr.keys():
            if type(jsonStr[key]) is dict:
                print(key + "\n", end='')
                prettyJson(jsonStr[key], tab + '\t')
            else:
                print(tab, key, ": ", convertString(jsonStr[key]))

class SNDEvent:
    # port default is 5556 for event rcver on OE
    # recordingDir changes the dir..
    # prependText and appendText add info to either the beginning or end of filename
    def __init__(self, port, recordingDir = '', prependText = '', appendText = ''):
        context = zmq.Context()
        #  Socket to talk to OE
        print("Connecting sender to Open Ephys \n")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:" + str(port))

        # Store the vars needed for recording right away. Defaults to blank
        self.recordingDir = recordingDir.encode("utf-8")
        self.prependText = prependText.encode("utf-8")
        self.appendText = appendText.encode("utf-8")

        # Flag vars for case statement
        self.START_ACQ = '0'
        self.STOP_ACQ = '1'
        self.GET_EXP_NUM = '2'
        self.START_REC = '3'
        self.STOP_REC = '4'

    # Asks what you want to send to OE
    def send(self, case = -1):
        if case == -1:
            print('Choose an option...')
            control = input('0 : startAcquisition \n1 : stopAcquisition\n2 : getExperimentNumber\n3 : startRecord\n4 : stopRecord\n')
        elif  0 <= int(case) and int(case) <= 4:
            control = case
        else:
            print('case not created')
            return
        print('sned a ' + control + ' to oe \n\n')
        self.socket.send(self.switch(control))

        #  Get the reply.
        message = self.socket.recv()
        print("Received reply %s " %  message)

    # Function that acts as a C switch. Gets your desired string
    def switch(self, x):
        return {
        '0' : b'startAcquisition ',
        '1' : b'stopAcquisition ',
        '2' : b'getExperimentNumber',
        '3' : b"".join([b'startRecord RecDir=', self.recordingDir,  b' prependText=', self.prependText, b' appendText=', self.appendText]),
        '4' : b'stopRecord'
        }[x]

    # Changes the vars set at __init__
    def changeRecordingVars(self, recordingDir = 'NOCHANGE', prependText = 'NOCHANGE', appendText = 'NOCHANGE'):
        if recordingDir != 'NOCHANGE':
            self.recordingDir = recordingDir.encode("utf-8")
        if prependText != 'NOCHANGE':
            self.prependText = prependText.encode("utf-8")
        if appendText != 'NOCHANGE':
            self.appendText = appendText.encode("utf-8")

    # Sends whatever string was sent. Use switch function to see examples of how to send
    def sendStr(self, string):
        # Encode into byte string and send
        self.socket.send(string.encode("utf-8"))
        #  Get the reply.
        message = self.socket.recv()
        print("Received reply %s " %  message)


## UNUSED ------------------------------

#### ZMQ classes to kill external processes ####
    # Maybe hardcode port so you don't need to think about that?
# Head GUI process has this. Send a kill command to let others know experiment is over.
class GUIPub:
    def __init__(self, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://localhost:" + str(port))

    def sendKill(self):
        self.socket.send(b'kill')

# Other processes that need to be told when experiment is over
class GUISub:
    def __init__(self, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.bind("tcp://localhost:" + str(port))
        self.socket.setsockopt(zmq.SUBSCRIBE, b'kill')

    # Non blocking check for a kill command from main GUI
    def checkKill(self):
        try:
            self.socket.recv(flags=zmq.NOBLOCK)
            return True
        except zmq.Again as e:
            return False
##############################################

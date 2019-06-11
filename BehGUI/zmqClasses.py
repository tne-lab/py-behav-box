import zmq
import numpy as np
from convertString import convertString
import json

class RCVEvent:
    # SUBSCRIBE can be a list of vars, need to be in byte string format => b'spike'
    def __init__(self, port, SUBSCRIBE):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:" + str(port))
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        for sub in SUBSCRIBE:
            self.socket.setsockopt(zmq.SUBSCRIBE, sub)

    def rcv(self):
        #Get raw input from socket
        sockets = self.poller.poll(200)
        for socket in sockets:
        #msg = self.socket.recv_multipart()
            msg = socket[0].recv_multipart()
            #msg = bmsg.decode('utf-8')
            #print('event recv', len(msg))
            if len(msg) == 1:
                envelope = msg
                #print(envelope, 'header')
            elif len(msg)==2:
                envelope, jsonStr = msg
                #Our actual json object (last part)
                jsonStr = json.loads(jsonStr);
                #print(self.parseJson(jsonStr))
                #print(jsonStr, 'just json')
                #print('\n')
                return jsonStr
            else:
                return false

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
    def __init__(self, port, recordingDir = '', prependText = '', appendText = '', TTLChannel = 0):
        context = zmq.Context()
        #  Socket to talk to OE
        print("Connecting sender to Open Ephys \n")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:" + str(port))

        # Store the vars needed for recording right away. Defaults to blank
        self.recordingDir = recordingDir.encode("utf-8")
        self.prependText = prependText.encode("utf-8")
        self.appendText = appendText.encode("utf-8")

        #Store TTL Channel
        self.TTLChannel = str(TTLChannel).encode("utf-8")


        # Flag vars for case statement
        self.INPUT = '-1'
        self.START_ACQ = '0'
        self.STOP_ACQ = '1'
        self.GET_EXP_NUM = '2'
        self.START_REC = '3'
        self.STOP_REC = '4'
        self.TTL_ON = '5'
        self.TTL_OFF = '6'

# send on/off
#send what bit to set

    # Asks what you want to send to OE
    def send(self, case = '-1'):
        if case == '-1':
            print('Choose an option...')
            control = input('0 : startAcquisition \n1 : stopAcquisition\n2 : getExperimentNumber\n3 : startRecord\n4 : stopRecord\n5 : TTLEventOn\n6 : TTLEventOff\nMy Input: ')
        elif int(case) <= 6:
            control = case
        else:
            print('case not created')
            return
        self.socket.send(self.switch(control))

        #  Get the reply.
        message = self.socket.recv()
        print("Received reply %s " %  message)

    def sendTTL(ON_OFF, TTL_CHAN):
        if ON_OFF:
            self.socket.send(b"".join([b'TTL Channel=', TTL_CHAN, b' on=1']))
        else:
            self.socket.send(b"".join([b'TTL Channel=', TTL_CHAN, b' on=0']))

    # Function that acts as a C switch. Gets your desired string
    def switch(self, x):
        return {
        '0' : b'startAcquisition ',
        '1' : b'stopAcquisition ',
        '2' : b'getExperimentNumber',
        '3' : b"".join([b'startRecord RecDir=', self.recordingDir,  b' prependText=', self.prependText, b' appendText=', self.appendText]),
        '4' : b'stopRecord',
        '5' : b"".join([b'TTL Channel=', self.TTLChannel, b' on=1']),
        '6' : b"".join([b'TTL Channel=', self.TTLChannel, b' on=0'])
        }[x]

    # Changes the vars set at __init__
    def changeVars(self, recordingDir = 'NOCHANGE', prependText = 'NOCHANGE', appendText = 'NOCHANGE', TTLChannel = 'NOCHANGE'):
        if recordingDir != 'NOCHANGE':
            self.recordingDir = recordingDir.encode("utf-8")
        if prependText != 'NOCHANGE':
            self.prependText = prependText.encode("utf-8")
        if appendText != 'NOCHANGE':
            self.appendText = appendText.encode("utf-8")
        if TTLChannel != 'NOCHANGE':
            self.TTLChannel = str(TTLChannel).encode("utf-8")

    # Sends string. Use switch function to see examples of how to send
    def sendStr(self, string):
        # Encode into byte string and send
        self.socket.send(string.encode("utf-8"))
        #  Get the reply.
        message = self.socket.recv()
        print("Received reply %s " %  message)

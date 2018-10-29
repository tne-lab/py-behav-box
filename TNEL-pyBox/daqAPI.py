#Python 3.7.1rc2 (v3.7.1rc2:6c06ef7dc3, Oct 13 2018, 15:44:37) [MSC v.1914 64 bit (AMD64)] on win32
#WType "help", "copyright", "credits" or "license()" for more information.
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 13:13:48 2018
@author: Ephys
"""
import nidaqmx
from nidaqmx.constants import (LineGrouping)
import time
dev = 'Dev2'

'''
Creates a new Interface class that can be sent bits
and holds task information
'''
class Interface:
    def __init__(self, address):
        self.task = nidaqmx.Task()
        self.task = task.do_channels.add_do_chan(
                address,
                line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
        self.task.start()
        self.address = address

    def sendDbit(self,TF):
        self.task.write(TF)
        enablePulse()

    def sendDByte(self,bits):
        self.task.write(bits)
        enablePulse()

    def rcvDI(self):
        return self.task.read()

    def end(self):
        self.task.stop()

'''
Sets up box with output address and service request lines
'''
def startUpBox():
    address = dev + '/port0/line0:3'
    request = dev +'/port9/line0:7'
    serviceRequest = Interface(request)
    outAddress = Interface(address)
    print('Setting Up')
    outAddress.sendDByte(address,0)
    serviceRequest.sendDByte(serviceRequest,1)
    return [outAddress,serviceRequest]

'''
Ends setup tasks for box
'''
def closeBox(outAddress,serviceRequest):
    outAddress.end()
    serviceRequest.end()

'''
Returns a new lever output task
'''
def leverOutputSetup():
    leverAddress = dev + '/port1/line0:1'
    levers = Interface(leverAddress)
    return levers

'''
Returns a new lever input tasks
'''
def leverInputSetup():
    leftAddress = dev + '/port6/line0'
    checkPressLeft = Interface(leftAddress)
    rightAddress = dev + '/port6/line1'
    checkPressRight = Interface(rightAddress)

    return [checkPressLeft, checkPressRight]

'''
Returns a new food tasks
'''
def giveFoodSetup():
    foodAddress = dev + '/port1/line4'
    food = Interface(foodAddress)
    return food

'''
Returns a new food light tasks
'''
def foodLightSetup():
    foodLightAddress = dev + '/port1/line5'
    foodLight = Interface(foodLightAddress)
    return foodLight

'''
Enable pulse for when sending bits/bytes
(Doesn't need a task because its just a pulse)
'''
def enablePulse():
    enable = dev + '/port0/line4'
    print('Enable Pulse')
    sendDByte(enable,True)

'''
Use to check presses on Levers
Needs Interface class as inputs
'''
def detectPress(checkPressLeft,checkPressRight):
    while True:
        leftPress = checkPressLeft.rcvDI()
        rightPress = checkPressRight.rcvDI()

        if rightPress:
            print('right')
            return 'Right'
        elif leftPress:
            print('left')
            return 'Left'
        else:
            continue


# Not using, just want port/bit numbers still
def giveFood():
     food = dev + '/port1/line4:5'
     print('Give food')
     sendDByte(food,96)
     enablePulse()

def turnLeftLightOn():
    LLight = dev + '/port1/line2'
    print("Lft Light On")
    sendDBit(Llight,True)

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 13:13:48 2018

@author: Ephys
"""
import nidaqmx
dev = 'Dev3'

def sendDOut(address,bits):
     with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(
            address,
            line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

        print(task.write(bits))

def rcvDI(address):
    with nidaqmx.Task() as task:
        task.di_channels.add_di_chan(address,
                                     line_grouping=LineGrouping.CHAN_PER_LINE)

        return task.read()

def enablePulse():
    enable = dev + '/port0/line4'
    print('Enable Pulse')
    sendDOut(enable,True)
    sendDOut(enable,False)
    sendDOut(enable,True)


def startUpBox():
    address = dev + '/port0/line0:3'
    print('Setting Up')
    sendDOut(address,0)
    enablePulse()

def pushOutLevers():
    levers = dev + '/port1/line0:1'

    print('Levers Out')
    sendDOut(levers,3)
    '''
    Might need enable pulse here
    '''

def detectPress():
    '''
    Dont know ports and such..
    '''
    while True:
        checkPressLeft = dev + '/port6/line0'
        checkPressRight = dev + '/port6/line1'
        leftPress = rcvDI(checkPressLeft)
        rightPress = rcvDI(checkPressRight)

        if rightPress:
            print('right')
            return 'Right'
        elif leftPress:
            print('left')
            return 'Left'
        else:
            continue


def pullInLevers():
    levers = dev + '/port1/line0:1'
    print('Levers In')
    sendDOut(levers,0)



def giveFood():
    food = dev + '/port1/line5:6'
    print('Give food')
    sendDOut(food,48)

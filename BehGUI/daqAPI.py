#Python 3.7.1rc2 (v3.7.1rc2:6c06ef7dc3, Oct 13 2018, 15:44:37) [MSC v.1914 64 bit (AMD64)] on win32
#WType "help", "copyright", "credits" or "license()" for more information.
# -*- coding: utf-8 -*-
"""
Created on Nov. 30, 2018 by Mark Schatza
Communicates with layafette instruments DAQ 41510-NL
to control a behavioral box

NOTE: 1. Please Start Whisker server first
      2. Check daqAPI.py on this directory.
         be sure Devices are named properly:

         on Ephis-1 'Dev1' runs behavior box
                    'pciDAQ' runs open ephys

         on Ephis-2 'Dev2' runs behavior box
                    'Dev1' runs open ephis
"""
import nidaqmx
from nidaqmx.constants import (LineGrouping)
from nidaqmx import stream_writers
import time
import os
dev = 'Dev2'
computer = os.environ['COMPUTERNAME']
print("USING COMPUTER: ",computer)
if 'EPHYS-2' in computer:
        dev = 'Dev2'
elif 'EPHYS-1' in computer:
        dev = 'Dev2'
elif 'ABETUSER-PC' == computer:
        dev = 'Dev1'

#dev = 'Dev2' #Flav's PC ephys-2
#dev = 'Dev1' #Jean's PC ephys-1

'''
Class for Digital Outputs. Can send (and maybe see what has been written. Hasn't been tested)
Also holds task information.
Must Call exampleclass.end() to correctly reset DAQ.

If using mult. lines use sendDByte function to send info sendDByte(3)
If using 1 line use sendDBit function to send info sendDBit(True)
'''
class InterfaceOut:
    def __init__(self, address):
        self.task = nidaqmx.Task()
        self.task.do_channels.add_do_chan(address,
            line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
        self.address = address

    def startTask(self):
        self.task.start()

    def sendDBit(self,TF):
        self.task.write(TF)
        enablePulse()

    def sendDByte(self,bits):
        self.task.write(bits)
        enablePulse()

    def rcvDI(self):
        return self.task.read()

    def end(self):
        self.task.close()




def enableSetup():
    enableAddress = dev + '/port0/line4'
    enableTask = InterfaceOut(enableAddress)
    enableTask.startTask()
    return enableTask

def enablePulse():
    enable = dev + '/port0/line4'
    #print('Enable Pulse')
    sendPulse(enable,True)

def sendPulse(address,bits):
     while True:
         try:
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan(address,
                     line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

                #print(task.write(bits))
            break
         except:
            print('trying')

####################################################
##      OUTPUTS
####################################################
'''
Returns a new lever output task
'''
def leverOutputSetup():
    leverAddress = dev + '/port1/line0:1'
    if 'ABETUSER-PC' == computer:
        leverAddress = dev + '/port3/line0:1'
    levers = InterfaceOut(leverAddress)
    levers.startTask()
    return levers

'''
Returns a new left conditioning light task
'''
def conditioningLightsLeftSetup():
    conditioningLightAddress = dev + '/port1/line2'
    if 'ABETUSER-PC' == computer:
        conditioningLightAddress = dev +'/port3/line2'
    conditioningLight = InterfaceOut(conditioningLightAddress)
    conditioningLight.startTask()
    return conditioningLight

'''

'''
def conditioningLightsRightSetup():
    conditioningLightAddress = dev + '/port1/line3'
    if 'ABETUSER-PC' == computer:
        conditioningLightAddress = dev + '/port3/line3'
    conditioningLight = InterfaceOut(conditioningLightAddress)
    conditioningLight.startTask()
    return conditioningLight

'''
Returns a new food task
'''
def giveFoodSetup():
    foodAddress = dev + '/port1/line4' #Output line 5
    if 'ABETUSER-PC' == computer:
        foodAddress = dev + '/port3/line4'
    food = InterfaceOut(foodAddress)
    food.startTask()
    return food

'''
Returns a new food light task
'''
def foodLightSetup():
    if 'EPHYS-2' in computer:
        foodLightAddress = dev + '/port3/line6' #Output line 7
    if 'ABETUSER-PC' == computer:
        foodLightAddress = dev + '/port3/line5'
    try:
        foodLight = InterfaceOut(foodLightAddress)
        foodLight.startTask()
        return foodLight
    except:
        return False
'''
Returns a SHOCKER task
'''
def shockerSetup():
    computer = os.environ['COMPUTERNAME']
    print("USING ", computer, " Computer. ")
    if 'EPHYS-2' in computer:
        shockerAddress = dev + '/port3/line5'  # Flav's PC #Output line 6
        print ("Be sure shocker connected to port1/Line6")
    elif 'EPHYS-1' in computer:
        shockerAddress = dev + '/port1/line5'  # Jean's PC
        print ("Be sure shocker connected to port1/Line6") #Output line 6
    elif 'ABETUSER-PC' == computer:
        shockerAddress = dev + '/port1/line6'
    else:
        print("Unregistered computer!!!!!!!!!!  See daqAPI.py in current working directory.")


    shocker = InterfaceOut(shockerAddress)
    shocker.startTask()
    return shocker

'''
Returns a new fan task
'''
def fanSetup():
    computer = os.environ['COMPUTERNAME']
    if 'EPHYS-2' in computer:
        fanAddress = dev + '/port4/line2'#
    if 'EPHYS-1' in computer:
        fanAddress = dev + '/port2/line2'#
    elif 'ABETUSER-PC' == computer:
        fanAddress = dev + '/port4/line2'
    fan = InterfaceOut(fanAddress)
    fan.startTask()
    return fan

'''
Returns a new cabin light task
'''
def cabinLightSetup():
    cabinLightAddress = dev + '/port2/line1'
    if 'ABETUSER-PC' == computer:
        cabinLightAddress = dev + '/port3/line7'
    cabinLight = InterfaceOut(cabinLightAddress)
    cabinLight.startTask()
    return cabinLight


'''
Returns a new low tone task
'''
def lowToneSetup():
    lowToneAddress = dev + '/port1/line6'#For 2Khz.  Note: #8 on Beh Box
    if 'ABETUSER-PC' == computer:
        lowToneAddress = dev + '/port3/line7'
    lowTone = InterfaceOut(lowToneAddress)
    lowTone.startTask()
    return lowTone

'''
Returns a new high tone Task
'''
#def highToneSetup():
#    highToneAddress = dev + '/port2/line1' #For 6Khz.  Note: #9 on Beh Box
#    highTone = InterfaceOut(highToneAddress)
#    highTone.startTask()
#    return highTone

####################################################
##   Analog Out
####################################################
class AnalogOut:
    def __init__(self, address):
        self.task = nidaqmx.Task()
        self.task.ao_channels.add_ao_voltage_chan(address)
        self.address = address
        self.stream = stream_writers.AnalogSingleChannelWriter(self.task.out_stream, auto_start = True)

    def setClock(self, sr, samples):
        self.task.timing.cfg_samp_clk_timing(sr, samps_per_chan = samples)

    def startTask(self):
        self.task.start()

    def sendWaveform(self,data):
        self.stream.write_many_sample(data)

    def end(self):
        self.task.close()

####################################################
##   Inputs
####################################################

'''
Class for Digital Inputs. Can only use receive.
Also holds Task information.
Must Call exampleclass.end() to correctly reset DAQ.
'''
class InterfaceIn:
    def __init__(self, address):
        self.task = nidaqmx.Task()
        self.task.di_channels.add_di_chan(
            address,
            line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
        self.address = address

    def startTask(self):
        self.task.start()

    # Use to receive data, increase 1 to make a larger buffer size
    # Check READ_ALL_AVAILABLE in documentation for nidaqmx. Might be useful
    def rcvDI(self):
        return self.task.read()

    def end(self):
        self.task.stop()
        self.task.close()

class InterfaceInNEW:
    def __init__(self, address):
        self.task = nidaqmx.Task()
        self.task.di_channels.add_di_chan(
            address,
            line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
        self.address = address

    def startTask(self):
        self.task.start()

    # Use to receive data, increase 1 to make a larger buffer size
    # Check READ_ALL_AVAILABLE in documentation for nidaqmx. Might be useful
    def rcvDI(self):
        return self.task.read()

    def end(self):
        self.task.stop()
        self.task.close()

class debounce:
    def __init__(self, inputTask):
        self.REPEAT = False
        self.prev_signal = False

'''
Returns a new lever input task
'''
def leverInputSetup():
    leftAddress = dev + '/port6/line0'
    rightAddress = dev + '/port6/line1'
    checkPressLeft = InterfaceIn(leftAddress)
    checkPressRight = InterfaceIn(rightAddress)
    checkPressLeft.startTask()
    checkPressRight.startTask()
    return checkPressLeft, checkPressRight


'''
Returns a new input task for when rat eats food
'''
def foodEatInputSetup():
    foodEatAddress = dev + '/port7/line2'
    foodEat = InterfaceIn(foodEatAddress)
    foodEat.startTask()
    return foodEat

'''
Returns left nose poke input Task
'''
def leftNoseInputSetup(): # 3
    leftNoseInputAddress = dev + '/port6/line3'
    leftNose = InterfaceIn(leftNoseInputAddress)
    leftNose.startTask()
    return leftNose

'''
Returns right nose poke input Task
'''
def rightNoseInputSetup():
    rightNoseInputAddress = dev + '/port6/line4'
    rightNose = InterfaceIn(rightNoseInputAddress)
    rightNose.startTask()
    return rightNose

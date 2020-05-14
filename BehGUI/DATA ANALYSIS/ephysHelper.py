# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 15:02:56 2019

@author: markschatza@gmail.com
TNEL Analysis code
"""
import numpy as np
from scipy import signal

class Event:
    def __init__(self, data, tsStart):
        self.eventId = data['eventId'] # Event id holds info about the event. TTL event: 1 = On, 0 = Off
        self.nodeId = data['nodeId'] # What node (Plugin) did this event come from?
        self.eventType = data['eventType']
        self.channel = data['channel'] # The event channel 1= threshold crossing, 2 = stim, 3 = sham
        
        self.ts = []
        for t in data['timestamps']:
            self.ts.append(t - tsStart) # Zero out the timestamp to correspond with continuous data


class Con:
    def __init__(self, data):
        #print("data = ", data[0:10])
        self.data = data['data'] # Volatage data
        self.fs = float(data['header']['sampleRate']) # Sample Rate
        self.interpTs(data['timestamps']) # Interpolate timestamps for all data points (Only has 1 time stamp for each buffer of 1024 data points)

    def interpTs(self, ts):
        tsStart = ts[0]
        tsEnd = ts[-1] + 1023
        self.ts = np.linspace(tsStart, tsEnd, len(ts) * 1024) # Creates the array of timestamps
        i = 0
        for t in self.ts:
            self.ts[i] = t - tsStart # Zero out the timestamps, just makes it look better when graphing/explaining
            i = i + 1
        self.tsStart = tsStart # Send the ts start to event data
        
        
import OpenEphys
        
'''
Load Data
'''
def loadCon(path):
    print("In loadCon")
    raw = OpenEphys.load(path)
    #print("RAW: ",raw[0:10])
    return Con(raw)

def loadEvents(path, tsStart):
    print("In loadEvents")
    raw = OpenEphys.load(path)
    return Event(raw, tsStart)



'''
Helper Functions
'''
def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='bandpass')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    filteredData = signal.lfilter(b, a, data)
    return filteredData

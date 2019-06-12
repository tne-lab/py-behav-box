import nidaqmx
from nidaqmx.constants import (LineGrouping)
from nidaqmx import stream_writers
import time
import os
import zmq
import math
import json
import random
import numpy as np

import zmqClasses
from libc.stdlib cimport malloc, free

# Dev3 for flavs computer
sr = 1000000 # Sampling Rate (Hz)
#amplitude = 1 # Amplitude (Volts) (change this to amps) , biphasic?
width = 0.9 # duration of pulse (ms)
ipi = 5 # inter-pulse interval (ms). output zero during this period,
# if muliple waveforms, period = width + ipi
#numPulse = 1
biphasic = True # if true, pulse is ceil(width/2) of amp followed by floow(width/2) of -amp
phaseShift = 0

class Stim:
    '''
    Class to create and send stim waveforms
    '''
    def __init__(self, stimX, q, backQ, MODE, nERPX = 0, nERPY = 0, stimY = None, INTER_ERP_WIDTH = 4, ERP_VAR = 1):
        ######## Create Waveform ######################################
        ## Change to 100micro amps for 90microsecs and biphasic!! Jeans stim
        # --------------------- INPUTS --------------------------------
        self.sr = 1000000 # Sampling Rate (Hz)
        amplitude = 1 # Amplitude (Volts) (change this to amps) , biphasic?
        self.width = 0.9 # duration of pulse (ms)
        self.ipi = 5 # inter-pulse interval (ms). output zero during this period,
        # if muliple waveforms, period = width + ipi
        numPulse = 1
        self.biphasic = True # if true, pulse is ceil(width/2) of amp followed by floow(width/2) of -amp
        self.phaseShift = 0
        # --------------------------------------------------------------
        self.createWaveform(amplitude, numPulse)
        ##################################################################

        self.npWave = np.array(self.waveform, dtype=np.float64)
        # Send back stim events
        self.q = q
        self.backQ = backQ

        self.stimX = stimX
        self.stimY = stimY

        # ERP
        if MODE == 'ERP':
            # Custom ERP Settings
            self.nERPX = int(nERPX)
            self.nERPY = int(nERPY)
            self.nXStim = 0
            self.nYStim = 0
            self.ERP_INTER_LOW = INTER_ERP_WIDTH - ERP_VAR
            self.ERP_INTER_HIGH = INTER_ERP_WIDTH + ERP_VAR
            self.ERP()
            return

        elif MODE == 'TRIGGER':
            # Create socket to listen to
            #self.rcv = zmqClasses.RCVEvent(5557, [b'ttl']) #see if same speed. may come back to this (poller/thread/q)
            context = zmq.Context()
            self.socket = context.socket(zmq.SUB)
            self.socket.connect("tcp://localhost:" + str(5557))
            #self.poller = zmq.Poller()
            #self.poller.register(self.socket, zmq.POLLIN)
            SUBSCRIBE = [b'ttl']
            for sub in SUBSCRIBE:
                self.socket.setsockopt(zmq.SUBSCRIBE, sub)

            self.waitForEvent()


    def createWaveform(self, amplitude, numPulse):
      # Now lets build it
      self.waveform = []
      negAmplitude = amplitude * -1
      widthSamp = int(self.width/1000.0*self.sr)
      ipiSamp = int(self.ipi/1000.0*self.sr)
      period = widthSamp + ipiSamp

      for num in range(numPulse):
          for i in range(int(self.phaseShift/360.0 * period)):
              self.waveform.append(0)
          for i in range(widthSamp):
              if self.biphasic:
                  if i <= math.ceil(widthSamp/2) + 1:
                      self.waveform.append(amplitude)
                  else:
                      self.waveform.append(negAmplitude)
              else:
                  self.waveform.append(amplitude)
          for i in range(int((360-self.phaseShift)/360.0 * period)):
              self.waveform.append(0)

      self.npWave = np.array(self.waveform, dtype=np.float64)

    def waitForEvent(self):
        '''
        waiting for OPEN EPHYS trigger. then tells GUI that it sent the stim
        '''
        while True:
            header, jsonMsg = self.socket.recv_multipart()
            jsonStr = json.loads(jsonMsg)
            if not self.backQ.empty():
                self.backQ.get()
                break
            if jsonStr['type'] == 'ttl' and jsonStr['data']: # ttl and data==true!
                self.stimX.sendWaveform(self.npWave)
                self.q.put('Stim pulse sent')

    def ERP(self):
        '''
        ERP stimulation paradigm
        '''
        for i in range(self.nERPX + self.nERPY):
            if not self.backQ.empty():
                self.backQ.get()
                break

            # Stim at location X or Y
            # Randomize but make sure each get specified num of pulses ( probably make this cleaner)
            XorY = random.randint(0,1)
            if XorY:
              if self.nXStim <= self.nERPX: # Make sure not all x pulses occured
                self.stimX.sendWaveform(self.npWave)
                self.q.put('ERP pulse sent , ' + self.stimX.address)
                self.nXStim += 1
              else:
                self.stimY.sendWaveform(self.npWave)
                self.q.put('ERP pulse sent , ' + self.stimY.address)
                self.nYStim += 1
            else:
              if self.nYStim <= self.nERPY:
                self.stimY.sendWaveform(self.npWave)
                self.q.put('ERP pulse sent , ' + self.stimY.address)
                self.nYStim += 1
              else:
                self.stimX.sendWaveform(self.npWave)
                self.q.put('ERP pulse sent , ' + self.stimX.address)
                self.nXStim += 1
            # Wait for brain to return to normal before stimming again
            sleepLen = random.uniform(self.PULSE_INTER_LOW, self.PULSE_INTER_HIGH)
            time.sleep(sleepLen) # 4 +- 1 second

    def openLoop(self):
      '''
      Open Loop (Jean) stimulation paradigm
      '''
      while True:
        # Check to stop
        if not self.backQ.empty():
            self.backQ.get()
            break

        self.stimX.sendWaveform(self.npWave)
        self.q.put('Open Loop stim 1 , ' + self.stimX.address)
        time.sleep(.0833)
        self.stimY.sendWaveform(self.npWave)
        self.q.put('Open Loop stim 2 , ' + self.stimY.address)
        sleepLen = random.uniform(delayLow, delayHigh) # Need to set delays here
        time.sleep(sleepLen)



    def paramSweeping(self):
      '''
      Jeans parameter sweeping paradigm
      '''
      #25,50,100ma
      # .25,.5,1 s
      #40 trials of one set, 8 seconds between pulse trains
      # Is there a pause between 40 trial sets?

      intensity = [25, 50, 100]
      pulseLength = [250, 500, 1000] # in ms
      paramSets = np.random.permutation(len(intensity) * len(pulseLength))
      setSize = 40
      delay = 8 #sec
      delayVar = 2 # sec
      delayHigh = delay + delayVar
      delayLow = delay - delayVar

      for i in range(paramSets):
        curSet = paramSets[i]
        self.createWaveform(intensity[curIntense],pulseLength[curLen] / (self.width+self.ipi))
        for i in range(setSize):
          self.stimX.sendWaveform(self.npWave)
          self.q.put('paramSweep Pulse Sent , ' + intensity[curIntense] "," + pulseLength[curLen])
          sleepLen = random.uniform(delayLow, delayHigh)
          time.sleep(sleepLen)

def createWaveform(amplitude, numPulse):
  # Now lets build it
  waveform = []
  negAmplitude = amplitude * -1
  widthSamp = int(width/1000.0*sr)
  ipiSamp = int(ipi/1000.0*sr)
  period = widthSamp + ipiSamp

  for num in range(numPulse):
      for i in range(int(phaseShift/360.0 * period)):
          waveform.append(0)
      for i in range(widthSamp):
          if biphasic:
              if i <= math.ceil(widthSamp/2) + 1:
                  waveform.append(amplitude)
              else:
                  waveform.append(negAmplitude)
          else:
              waveform.append(amplitude)
      for i in range(int((360-phaseShift)/360.0 * period)):
          waveform.append(0)

  return np.array(self.waveform, dtype=np.float64)

def waitForEvent(stimX, q, backQ):
  '''
  waiting for OPEN EPHYS trigger. then tells GUI that it sent the stim
  '''
  # Create socket to listen to
  rcv = zmqClasses.RCVEvent(5557, [b'ttl'])
  npWave = createWaveform(100, 1)
  while True:
      if(jsonMsg = rcv.rcv()):
        jsonStr = json.loads(jsonMsg)
        if not backQ.empty():
            backQ.get()
            break
        if jsonStr['type'] == 'ttl' and jsonStr['data']: # ttl and data==true!
            stimX.sendWaveform(npWave)
            q.put('Stim pulse sent')

def ERP(stimX, stimY, q, backQ, nERPX, nERPY, ERP_INTER_LOW, ERP_INTER_HIGH):
    '''
    ERP stimulation paradigm
    '''
    # Custom ERP Settings
    npWave = createWaveform(100,1)

    nXStim = 0
    nYStim = 0

    for i in range(nERPX + nERPY):
        if not backQ.empty():
            backQ.get()
            break

        # Stim at location X or Y
        # Randomize but make sure each get specified num of pulses ( probably make this cleaner)
        XorY = random.randint(0,1)
        if XorY:
          if nXStim <= nERPX: # Make sure not all x pulses occured
            stimX.sendWaveform(npWave)
            q.put('ERP pulse sent , ' + stimX.address)
            nXStim += 1
          else:
            stimY.sendWaveform(npWave)
            q.put('ERP pulse sent , ' + stimY.address)
            nYStim += 1
        else:
          if nYStim <= nERPY:
            stimY.sendWaveform(npWave)
            q.put('ERP pulse sent , ' + stimY.address)
            nYStim += 1
          else:
            stimX.sendWaveform(npWave)
            q.put('ERP pulse sent , ' + stimX.address)
            nXStim += 1
        # Wait for brain to return to normal before stimming again
        sleepLen = random.uniform(ERP_INTER_LOW, ERP_INTER_HIGH)
        time.sleep(sleepLen) # 4 +- 1 second

def openLoop(stimX, stimY, q, backQ, delayLow, delayHigh):
  '''
  Open Loop (Jean) stimulation paradigm
  '''
  npWave = createWaveform(100,1)

  while True:
    # Check to stop
    if not backQ.empty():
        backQ.get()
        break

    stimX.sendWaveform(npWave)
    q.put('Open Loop stim 1 , ' + stimX.address)
    time.sleep(.0833)
    stimY.sendWaveform(npWave)
    q.put('Open Loop stim 2 , ' + stimY.address)
    sleepLen = random.uniform(delayLow, delayHigh) # Need to set delays here
    time.sleep(sleepLen)

  def paramSweeping(stimX, stimY, q, backQ, intensity, pulseLength, setSize, delayLow, delayHigh):
    '''
    Jeans parameter sweeping paradigm
    '''
    #25,50,100ma
    # .25,.5,1 s
    #40 trials of one set, 8 seconds between pulse trains
    # Is there a pause between 40 trial sets?
    #### Inputs
    #intensity = [25, 50, 100]
    #pulseLength = [250, 500, 1000] # in ms
    #paramSets = np.random.permutation(len(intensity) * len(pulseLength))
    #setSize = 40
    #delay = 8 #sec
    #delayVar = 2 # sec
    #delayHigh = delay + delayVar
    #delayLow = delay - delayVar

    for i in range(paramSets):
      curSet = paramSets[i]
      createWaveform(intensity[curIntense],pulseLength[curLen] / (self.width+self.ipi))
      for i in range(setSize):
        if not backQ.empty():
            backQ.get()
            break
        stimX.sendWaveform(npWave)
        q.put('paramSweep Pulse Sent , ' + intensity[curIntense] "," + pulseLength[curLen])
        sleepLen = random.uniform(delayLow, delayHigh)
        time.sleep(sleepLen)

def main():
  stimQ = 1
  stim = Stim('Dev3/ao1', stimQ, "TRIGGER") #'Dev3/ao1'

if __name__ == "__main__":
  main()

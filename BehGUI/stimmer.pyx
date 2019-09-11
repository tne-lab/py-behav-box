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
width = 20 # duration of pulse (ms)
ipi = 5 # inter-pulse interval (ms). output zero during this period,
# if muliple waveforms, period = width + ipi
#numPulse = 1
biphasic = True # if true, pulse is ceil(width/2) of amp followed by floow(width/2) of -amp
phaseShift = 0

'''
Not class stimmer. Makes things a little smaller
'''
def createWaveform(amplitude, numPulse):
  # Now lets build it
  waveform = []
  negAmplitude = amplitude * -1
  widthSamp = int(width/1000.0*sr)
  ipiSamp = int(ipi/1000.0*sr)
  period = widthSamp + ipiSamp

  for num in range(int(numPulse)):
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

  return np.array(waveform, dtype=np.float64)

def waitForEvent(stimX, stimY, q, backQ):
  '''
  waiting for OPEN EPHYS trigger. then tells GUI that it sent the stim
  '''
  # Create socket to listen to
  print('in closed loop')
  rcv = zmqClasses.RCVEvent(5557, [b'ttl', b'event'])
  npWave = createWaveform(1, 1)
  stimSent = 0
  stimTime = time.perf_counter()
  while True:
    if not backQ.empty():
        backQ.get()
        break
    jsonStr = rcv.rcv()
    if jsonStr:
      if time.perf_counter() - stimTime > 1: # wait one second
        if jsonStr['type'] == 'ttl' and jsonStr['channel'] == 0 and jsonStr['data'] == True: # ttl and data==true! and only cd channel 0
          if stimSent == 0: # last was sham, send stim now
            stimX.sendWaveform(npWave)
            q.put('Closed loop pulse sent,' + stimX.address)
            stimTime = time.perf_counter()
            stimSent = 1
          else:
            stimY.sendWaveform(npWave)
            q.put('Closed loop sham pulse sent,' + stimY.address)
            stimTime = time.perf_counter()
            stimSent = 0

def ERP(stimX, stimY, q, backQ, nERPX, nERPY, ERP_INTER_LOW, ERP_INTER_HIGH):
    '''
    ERP stimulation paradigm
    '''
    # Custom ERP Settings
    npWave = createWaveform(1,1)

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
            q.put('ERP pulse sent X, ' + stimX.address)
            nXStim += 1
          else:
            stimY.sendWaveform(npWave)
            q.put('ERP pulse sent Y, ' + stimY.address)
            nYStim += 1
        else:
          if nYStim <= nERPY:
            stimY.sendWaveform(npWave)
            q.put('ERP pulse sent Y, ' + stimY.address)
            nYStim += 1
          else:
            stimX.sendWaveform(npWave)
            q.put('ERP pulse sent X, ' + stimX.address)
            nXStim += 1
        # Wait for brain to return to normal before stimming again
        sleepLen = random.uniform(ERP_INTER_LOW, ERP_INTER_HIGH)
        time.sleep(sleepLen) # 4 +- 1 second


def openLoop(stimX, stimY, q, backQ, phaseDelay, delayLow, delayHigh):
  '''
  Open Loop (Jean) stimulation paradigm
  '''
  npWave = createWaveform(1,1)

  while True:
    # Check to stop
    if not backQ.empty():
        backQ.get()
        break

    stimX.sendWaveform(npWave)
    q.put('Open Loop stim X , ' + stimX.address)
    time.sleep(phaseDelay)
    stimY.sendWaveform(npWave)
    q.put('Open Loop stim Y , ' + stimY.address)
    sleepLen = random.uniform(delayLow, delayHigh)
    time.sleep(sleepLen)

def paramSweeping(stimX, stimY, q, backQ, intensity, pulseLength, setSize, phaseDelay, delayLow, delayHigh):
    '''
    Jeans parameter sweeping paradigm
    '''
    randIntense = np.random.permutation(len(intensity))
    randLen = np.random.permutation(len(pulseLength))

    for i in randIntense:
      curIntense = intensity[i]
      for j in randLen:
        curLen = pulseLength[j]
        npWave = createWaveform(curIntense,curLen / (width+ipi))
        for x in range(setSize):
          if not backQ.empty():
              backQ.get()
              break
          stimX.sendWaveform(npWave)
          q.put('paramSweep Pulse Sent X, ' +  stimX.address + ',' + str(curIntense) + "," + str(curLen))
          time.sleep(phaseDelay)
          stimY.sendWaveform(npWave)
          q.put('paramSweep Pulse Sent Y, ' +  stimY.address + ',' + str(curIntense) + ',' + str(curLen))
          sleepLen = random.uniform(delayLow, delayHigh)
          time.sleep(sleepLen)

def main():
  stimQ = 1
  #stim = Stim('Dev3/ao1', stimQ, "TRIGGER") #'Dev3/ao1'

if __name__ == "__main__":
  main()

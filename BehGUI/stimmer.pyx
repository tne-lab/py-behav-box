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
from mttkinter.mtTkinter import *
from tkinter import *

import zmqClasses
from libc.stdlib cimport malloc, free

# Dev3 for flavs computer
sr = 3000000 # Sampling Rate (Hz)
#amplitude = 1 # Amplitude (Volts) (change this to amps) , biphasic?
width = 0.09 # duration of pulse (ms) # duration of pulse (ms) .9
ipi = 5 # inter-pulse interval (ms). output zero during this period,
# if muliple waveforms, period = width + ipi
#numPulse = 1
biphasic = True # if true, pulse is ceil(width/2) of amp followed by floow(width/2) of -amp
phaseShift = 0
'''
Not class stimmer. Makes things a little smaller
'''
def createWaveform(amplitude, numPulse = 1):
  # Now lets build it
  waveform = []
  negAmplitude = amplitude * -1
  widthSamp = int(width/1000.0*sr)
  ipiSamp = int(ipi/1000.0*sr)
  period = widthSamp + ipiSamp

  for num in range(int(numPulse)):
      for i in range(int(phaseShift/360.0 * ipiSamp)):
          waveform.append(0)
      for i in range(widthSamp):
          if biphasic:
              if i <= math.ceil(widthSamp/2) + 1:
                  waveform.append(amplitude)
              else:
                  waveform.append(negAmplitude)
          else:
              waveform.append(amplitude)
      for i in range(int((360-phaseShift)/360.0 * ipiSamp)):
          waveform.append(0)

  return np.array(waveform, dtype=np.float64)

def waitForEvent(stimX, stimY, q, backQ, channel, microamps, stimLag, timer, timeout, timeoutVar, oeAddress):
  '''
  waiting for OPEN EPHYS trigger. then tells GUI that it sent the stim
  '''
  while not backQ.empty():
      msg = backQ.get()
  # Create socket to listen to
  rcv = zmqClasses.RCVEvent(oeAddress, 5557, [b'ttl', b'event'])
  voltage = microamps / 100
  npWave = createWaveform(voltage)
  window = Tk()
  winText = "Change to location for Closed Loop"
  lbl = Label(window, text=winText, font=("Arial Bold", 100))
  lbl.grid(column=0, row=0)
  window.mainloop()
  q.put('CONTINUE')
  timer = timer
  stimSent = 0
  pause = False
  stimTime = time.perf_counter()
  startTime = stimTime
  timeoutHigh = timeout + timeoutVar # Set high and low timeout variables (so we don't stim at 1hz)
  timeoutLow = timeout - timeoutVar
  curTimeout = random.uniform(timeoutHigh, timeoutLow)

  while True:
    if not backQ.empty():
        msg = backQ.get()
        print(msg)
        if msg == 'STOP':
          break
        elif msg == 'PAUSE':
          pause = True
          pauseTime = time.perf_counter()
        elif msg == 'CONTINUE':
          pause = False
          startTime += time.perf_counter() - pauseTime
    jsonStr = rcv.rcv()
    curTime = time.perf_counter()
    if curTime - startTime > timer and not pause: # Closed loop is over!
      print('returned from closed loop')
      return
    if pause:
      print('pausing')
      time.sleep(0.1)
      continue
    if jsonStr:
      if curTime - stimTime > curTimeout: # wait timeout
        if jsonStr['type'] == 'ttl' and int(jsonStr['channel']) == int(channel)-1 and jsonStr['data'] == True: # ttl and data==true! and only cd channel 0
          if stimSent == 0: # last was sham, send stim now
            if stimLag > 0:
                time.sleep(stimLag)
            stimX.sendWaveform(npWave)
            q.put('Closed loop pulse sent,' + stimX.address)
            stimTime = time.perf_counter()
            stimSent = 1
            curTimeout = random.uniform(timeoutHigh, timeoutLow)
          else:
            if stimLag > 0:
                time.sleep(stimLag)
            stimY.sendWaveform(npWave)
            q.put('Closed loop sham pulse sent,' + stimY.address)
            stimTime = time.perf_counter()
            stimSent = 0
            curTimeout = random.uniform(timeoutHigh, timeoutLow)

def ERP(stimX, stimY, q, backQ, nERP, ERP_INTER_LOW, ERP_INTER_HIGH, NUM_LOCATIONS, snd, suffix):
    '''
    ERP stimulation paradigm
    '''
    while not backQ.empty():
        msg = backQ.get()
        print(msg)
    # Custom ERP Settings
    npWave = createWaveform(1)
    randint = np.random.permutation(NUM_LOCATIONS)
    for i in randint:
      optText = ''
      if i == 0:
        optText = 'CH_1_8'
      elif i == 1:
        optText = 'CH_9_16'
      window = Tk()
      winText = "Change to location #" + str(i) + ' ' + ',(' + optText + ')'
      lbl = Label(window, text=winText, font=("Arial Bold", 100))
      lbl.grid(column=0, row=0)
      window.mainloop()
      pause = False
      j = 0
      snd.send(snd.STOP_REC)
      snd.changeVars(prependText = 'ERP_'   + suffix + '_' + optText)
      snd.send(snd.START_REC)
      while j < nERP:
        if not backQ.empty():
            msg = backQ.get()
            if msg == 'STOP':
              return
            elif msg == 'PAUSE':
              pause = True
            elif msg == 'CONTINUE':
              pause = False
        if pause:
            time.sleep(0.1)
            continue
        stimX.sendWaveform(npWave)
        q.put('ERP stim, ' + str(i) + optText)
        # Wait for brain to return to normal before stimming again
        sleepLen = random.uniform(ERP_INTER_LOW, ERP_INTER_HIGH)
        time.sleep(sleepLen) # 4 +- 1 second
        j+=1


def openLoop(stimX, stimY, q, backQ, phaseDelay, delayLow, delayHigh):
  '''
  Open Loop (Jean) stimulation paradigm
  '''
  while not backQ.empty():
      msg = backQ.get()
  npWave = createWaveform(1,1)
  pause = False
  while True:
    # Check to stop
    if not backQ.empty():
        msg = backQ.get()
        if msg == 'STOP':
          break
        elif msg == 'PAUSE':
          pause = True
        elif msg == 'CONTINUE':
          pause = False
    if pause:
      time.sleep(0.1)
      continue

    stimX.sendWaveform(npWave)
    q.put('Open Loop stim X , ' + stimX.address)
    time.sleep(phaseDelay)
    stimY.sendWaveform(npWave)
    q.put('Open Loop stim Y , ' + stimY.address)
    sleepLen = random.uniform(delayLow, delayHigh)
    time.sleep(1)

def paramSweeping(stimX, stimY, q, backQ, intensity, pulseLength, setSize, phaseDelay, delayLow, delayHigh):
    '''
    Jeans parameter sweeping paradigm
    '''
    while not backQ.empty():
        msg = backQ.get()
    randIntense = np.random.permutation(len(intensity))
    randLen = np.random.permutation(len(pulseLength))
    pause = False
    for i in randIntense:
      curIntense = intensity[i]
      for j in randLen:
        curLen = pulseLength[j]
        npWave = createWaveform(curIntense,curLen / (width+ipi))
        x = 0
        while x < setSize:
          if not backQ.empty():
              msg = backQ.get()
              if msg == 'STOP':
                return
              elif msg == 'PAUSE':
                pause = True
              elif msg == 'CONTINUE':
                pause = False
          if pause:
            time.sleep(0.1)
            continue
          stimX.sendWaveform(npWave)
          q.put('paramSweep Pulse Sent X, ' +  stimX.address + ',' + str(curIntense) + "," + str(curLen))
          time.sleep(phaseDelay)
          stimY.sendWaveform(npWave)
          q.put('paramSweep Pulse Sent Y, ' +  stimY.address + ',' + str(curIntense) + ',' + str(curLen))
          sleepLen = random.uniform(delayLow, delayHigh)
          time.sleep(sleepLen)
          x+=1

def main():
  stimQ = 1
  #stim = Stim('Dev3/ao1', stimQ, "TRIGGER") #'Dev3/ao1'

if __name__ == "__main__":
  main()

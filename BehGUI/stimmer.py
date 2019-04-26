import nidaqmx
from nidaqmx.constants import (LineGrouping)
import time
import os
import zmq
import math

import zmqClasses

# Dev3 for flavs computer

class Stim:
    '''
    Class to create and send stim waveforms
    '''
    def __init__(self, address, q):
        ######## Create Waveform ######################################
        # --------------------- INPUTS --------------------------------
        sr = 10000 # Sampling Rate (Hz)
        amplitude = 1 # Amplitude (Volts)
        width = 500 # duration of pulse (ms)
        ipi = 500 # inter-pulse interval (ms). output zero during this period,
        # if muliple waveforms, period = width + ipi
        numPulse = 3
        biphasic = True # if true, pulse is ceil(width/2) of amp followed by floow(width/2) of -amp
        phaseShift = 270
        # --------------------------------------------------------------

        # Now lets build it
        self.waveform = []
        negAmplitude = amplitude * -1
        widthSamp = int(width/1000.0*sr)
        ipiSamp = int(ipi/1000.0*sr)
        period = widthSamp + ipiSamp

        for num in range(numPulse):
            for i in range(int(phaseShift/360.0 * period)):
                self.waveform.append(0)
            for i in range(widthSamp):
                if biphasic:
                    if i <= math.ceil(widthSamp/2) + 1:
                        self.waveform.append(amplitude)
                    else:
                        self.waveform.append(negAmplitude)
                else:
                    self.waveform.append(amplitude)
            for i in range(int((360-phaseShift)/360.0 * period)):
                self.waveform.append(0)
        ##################################################################

        # From parent to get quit
        self.q = q

        # Create socket to listen to
        self.rcv = zmqClasses.RCVEvent(5557, [b'ttl'])



        # Create Task
        self.task = nidaqmx.Task()
        self.task.ao_channels.add_ao_voltage_chan(address) # Change max_val to max voltage used
        # Set timing
        self.task.timing.cfg_samp_clk_timing(sr, samps_per_chan = period * numPulse) # rate , can also change active_edge,
                                #continuous or finite number of samples

        self.waitForEvent()


    def sendStim(self):
        self.task.write(self.waveform, auto_start = True)
        self.task.wait_until_done() # Waits until done or timeouts after 10 seconds
        self.task.stop()
        print('stim done')

    def waitForEvent(self): # waiting for OPEN EPHYS. then tells GUI and open ephys that it sent the stim
        while True:
            json = self.rcv.rcv()
            if json:
                self.sendStim()
                json = False

    def close(self):
        self.task.close()


if __name__ == "__main__":
    q = 1
    #print(nidaqmx.system._collection
    stim = Stim('Dev3/ao1', q)

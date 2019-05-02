import nidaqmx
from nidaqmx.constants import (LineGrouping)
import time
import os
import zmq
import math

import zmqClasses
from libc.stdlib cimport malloc, free

# Dev3 for flavs computer

cdef class Stim:
    '''
    Class to create and send stim waveforms
    '''
    #cdef int* waveform
    cdef int waveform[10000] #numPulse * Period (hard code for speed!) Hopefully update
    def __init__(self, address, q):
        ######## Create Waveform ######################################
        # --------------------- INPUTS --------------------------------
        sr = 1000000 # Sampling Rate (Hz)
        amplitude = 1 # Amplitude (Volts) (change this to amps) , biphasic?
        width = 5 # duration of pulse (ms)
        ipi = 5 # inter-pulse interval (ms). output zero during this period,
        # if muliple waveforms, period = width + ipi
        numPulse = 1
        biphasic = True # if true, pulse is ceil(width/2) of amp followed by floow(width/2) of -amp
        phaseShift = 0
        # --------------------------------------------------------------

        # Now lets build it
        negAmplitude = amplitude * -1
        widthSamp = int(width/1000.0*sr)
        ipiSamp = int(ipi/1000.0*sr)
        period = widthSamp + ipiSamp
        #self.waveform = <int *> malloc(period*numPulse * sizeof(int)) Possible option

        for num in range(numPulse):
            for i in range(int(phaseShift/360.0 * period)):
                self.waveform[i*num] = 0
            for i in range(widthSamp):
                if biphasic:
                    if i <= math.ceil(widthSamp/2) + 1:
                        self.waveform[i*num] = amplitude
                    else:
                        self.waveform[i * num] = negAmplitude
                else:
                    self.waveform[i * num] = amplitude
            for i in range(int((360-phaseShift)/360.0 * period)):
                self.waveform[i * num] = 0
        ##################################################################

        # From parent to get quit
        self.q = q

        # Create socket to listen to
        #self.rcv = zmqClasses.RCVEvent(5557, [b'ttl'])
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:" + str(5557))
        #self.poller = zmq.Poller()
        #self.poller.register(self.socket, zmq.POLLIN)
        SUBSCRIBE = [b'ttl']
        for sub in SUBSCRIBE:
            self.socket.setsockopt(zmq.SUBSCRIBE, sub)


        # Create Task
        self.task = nidaqmx.Task()
        self.task.ao_channels.add_ao_voltage_chan(address) # Change this eventually
        #self.task.ao_channels.add_ao_current_chan(address) # check max amps
        # Set timing
        self.task.timing.cfg_samp_clk_timing(sr, samps_per_chan = period * numPulse) # rate , can also change active_edge,
                                #continuous or finite number of samples

        self.waitForEvent()


    cdef sendStim(self):
        self.task.write(self.waveform, auto_start = True)
        self.task.wait_until_done() # Waits until done or timeouts after 10 seconds
        self.task.stop()

    cdef waitForEvent(self): # waiting for OPEN EPHYS. then tells GUI and open ephys that it sent the stim
        while True:
            self.socket.recv_multipart()
            self.sendStim()


    def close(self):
        self.task.close()

def main(address, q):
  stim = Stim(address, q) #'Dev3/ao1'

if __name__ == "__main__":
  main()

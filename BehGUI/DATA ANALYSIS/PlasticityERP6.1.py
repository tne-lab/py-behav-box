
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 15:07:33 2019

@author: ephys-2
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import ephysHelper # Has helper functions to load data into pretty classes
import tkinter as Tk
from tkinter.filedialog import askopenfilename,asksaveasfile
from scipy import signal, stats, mean

#import csv
#initialDIR = r'E:\DATA BACKUP 1-23-2020\ '  # BACKUP DRIVE
initialDIR = r'E:\py-behav-box\BehGUI\DATA\ '
date = '0/0/0'
time = '0:0'
ERP_TYPE = "PRE_ERP"
####################
def choose_file(msg,DIR = "NONE"):
    print("DIR1: ", DIR)
    root = Tk.Tk()
    root.lift()

    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    if DIR == "NONE":
        #full_path = askopenfilename(title = msg, initialdir = r"D:\Plasticity Data")
        #full_path =  askopenfilename(title = msg, initialdir = r"E:\py-behav-box\BehGUI\DATA\ "  ) # show an 'Open' dialog box and return the path to the selected file
        full_path =  askopenfilename(title = msg, initialdir = initialDIR  )
        directory_only = os.path.split(full_path)[0]
    else: 
        full_path = askopenfilename(title = msg, initialdir = DIR) # show an "Open" dialog box and return the path to the selected file
        directory_only = DIR
    file_name = os.path.split(full_path)[1]
    root.destroy()
    if "9TO16" in full_path: direction_of_treatment = "IL->BLA"
    elif "1TO8" in full_path: direction_of_treatment = "BLA->IL"
    print(full_path)
    idx_of_rat = full_path.find("STIM/")+5 #E:/DATA BACKUP 1-23-2020/PLASTICITY_9TO16_STIM/OB32M/Jan_21_20/12-14/ERP_PRE_20
    #print("idx_of_rat: ",idx_of_rat)
    rat_portionto_end = full_path[idx_of_rat:len(full_path)-1]
    #print(full_path[idx_of_rat:len(full_path)-1])
    #print(rat_portionto_end)                             
    idx_end_of_rat = rat_portionto_end.find("/")
    #print(idx_end_of_rat)
    RAT = full_path[idx_of_rat:idx_of_rat+idx_end_of_rat]
    print(direction_of_treatment)
    print("RAT: ",RAT)
                                
    return full_path, directory_only, file_name,direction_of_treatment,RAT

def get_uAmps_and_lag(full_path):
    print("FULL PATH", full_path)
    dir1 = os.path.split(full_path)[0]
    dir2 = os.path.split(dir1)[0]
    dir3 = os.path.split(dir2)[0]
    dir4 = os.path.split(dir3)[0]
    dir5 = os.path.split(dir4)[0]
    dir6 = os.path.split(dir5)[1]
    print("DIR1: ",dir1)
    print("DIR2: ",dir2)
    print("DIR3: ",dir3)
    print("DIR4: ",dir4)
    print("DIR5: ",dir5)
    print("DIR6: ",dir6)
    date = os.path.split(dir3)[1]
    time = os.path.split(dir2)[1]
    if "PLASTICITY_9TO16_STIM" == dir6:
        protofile = "PLASTICITY_9to16STIM_COPY.txt"
    elif "PLASTICITY_1TO8_STIM" == dir6:
        protofile = "PLASTICITY_1to8STIM_COPY.txt"
    else: print("path not found")

    protofilename = str(dir2+"/"+protofile)
    print("PROTO FILE: ",protofilename)
    
    #protodatafile =  open(protofilename,"r")
        ###XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    with open(protofilename) as f:
        GOT_AMPS = False
        GOT_LAG = False
        for line in f:
            print(line)
            if 'MICROAMPS' in line:
                try:
                    uAmpStr = line.split('=')[1]
                    uAmpStr = uAmpStr.split('#')[0]
                    microamps = int(uAmpStr.strip()[:4])
                    print("microamps: ",microamps)
                    GOT_AMPS = True
                except: pass
            if 'STIM_LAG' in line:
                try:
                    lag = line.split('=')[1]
                    lag = lag.split('#')[0]
                    stim_lag = int(lag.strip()[:4])
                    GOT_LAG =True
                except: pass
            if GOT_AMPS and GOT_LAG:
                return microamps, stim_lag,date,time

##################################################################################
# PRINT INSTRUCTIONS:
##print(" 1.) Load the High Gamma channel ((CAR) data for the DRIVING channel) we were looking at")
##print("     IL = 104 Chan 1 - 8 (use 2 if looking at Magnitude,")
##print("     BLA = 105 Chan 9 - 16 (use 9 if looking at Magnitude.")                                    
##print(" 2.) Load a channel from the TARGET region.")
##print("     NOTE:  104_CH1-16 and 105_CH1-16 files are Common Avg Rectified (CAR) files ")
##print("            112_CH1-16 are RAW data files. \n\n")
##
#usr_response = input("Press any key to continue...")
                                    
######################
### 1.) Load the data for the raw Common Average Reference (CAR) data for the DRIVING channel we were looking at
###      IL = 104 Chan 1 - 8 (use 2 if looking at Magnitude,
###      BLA = 105 Chan 9 - 16 (use 9 if looking at Magnitude.
##print("load CAR data in the DRIVING (1st) region where thresholds are derived from \n(BLA 105_CH9.continuous when IL is stimmed, or IL 104_CH2.continuous when BLA stimmed)")
##full_path, directory_only, drv_file_name = choose_file("load CAR data in the DRIVING (1st) region where thresholds are derived from (BLA 105_CH9.continuous when IL is stimmed, or IL 104_CH2.continuous when BLA stimmed)")

print("Select folder data is in (ERP PRE, ERP POST 5, or ERP POST 30)")
full_path, directory_only, drv_file_name,direction_of_treatment,RAT = \
          choose_file("Select folder data is in (ERP PRE, ERP POST 5, or ERP POST 30)")

print(full_path, directory_only, drv_file_name,direction_of_treatment,RAT)
microamps, stim_lag, date,time  = get_uAmps_and_lag(full_path)
print (microamps, stim_lag, date, time)
# WHICH AREA WAS STIMULATED FIRST FOR ERPS?
print("\n\n\n\n\n")
area_stimulated_1st = input("Which area did you stimulate first for ERPs? 1 = IL (1-8), 2 = BLA (9-16)\n    ")
user_response = input("did you use channels 2, and 9 for high gamma signals? (y/n)")

if user_response == 'n' or user_response == 'N':
    IL_chan = input("Enter high gamma IL channel number (1-8): ")
    BLA_chan = input("Enter high gamma BLA channel number (9-16): ")
    
else:
    BLA_chan = 9
    IL_chan = 2

if area_stimulated_1st == 2: # BLA STIMULATED FIRST, LOOKING FOR BLA RESPONSES
    drv_file_name = "112_CH"+str(IL_chan)+".continuous"
    full_path = os.path.join(directory_only,drv_file_name)
    print("Loading: ",drv_file_name)
    il = ephysHelper.loadCon(full_path) # Load high gamma driving data

    tar_file_name = "112_CH"+str(BLA_chan)+".continuous"
    full_path = os.path.join(directory_only,tar_file_name)
    print("loading ", tar_file_name)
    bla = ephysHelper.loadCon(full_path) # Target data
    
else: #IL stimulated first
    drv_file_name = "112_CH"+str(BLA_chan)+".continuous"
    full_path = os.path.join(directory_only,drv_file_name)
    print("Loading: ",drv_file_name)
    il = ephysHelper.loadCon(full_path) # Load high gamma driving data

    tar_file_name = "112_CH"+str(IL_chan)+".continuous"
    full_path = os.path.join(directory_only,tar_file_name)
    print("loading ", tar_file_name)
    bla = ephysHelper.loadCon(full_path) # Target data
    
##print("Loading: ",drv_file_name)
##il = ephysHelper.loadCon(full_path) # Load high gamma driving data


######################
### 2.) Load the data for the raw CAR data for the channel we were looking at in the TARGET region
##print("load RAW for channel in TARGET (2nd) region (When IL STIMMED 112_CH1-8, When BLA STIMed 112_CH9-16)")
##print("        NOTE:  104_CH1-16 and 105_CH1-16 files are Common Avg Rectified (CAR) files ")
##print("               112_CH1-16 are RAW data files. \n")
##
###usr_response = input("Press any key to continue...")
#### full_path, directory_only, tar_file_name = choose_file("load RAW CAR data for channel in TARGET (2nd) region (When IL STIMMED 104_CH1-8, When BLA STIMed 105_CH9-16)",directory_only)
##full_path, directory_only, tar_file_name = choose_file("load RAW for channel in TARGET (2nd) region (When IL STIMMED 112_CH1-8, When BLA STIMed 112_CH9-16)",directory_only)
##
##print("\nLoading: ",tar_file_name)
##bla = ephysHelper.loadCon(full_path) # Target data


####################
# 3.) Load the event data
print("\nloading all_channels.events")  
full_path = os.path.join(directory_only,"all_channels.events") ##file_name = "all_channels.events")
events = ephysHelper.loadEvents(full_path, il.tsStart)##  all_channels.events...\n")

####################
# Remove 60hz Noise
w0 = 60/(bla.fs/2)
b,a  = signal.iirnotch(w0, 30)

blaData = signal.filtfilt(b,a, bla.data)
ilData = signal.filtfilt(b,a, il.data)
#######################################################
#
# Bandpass con data
# Delta 1-4 Hz
# Theta 4-8 Hz
# Alpha 8-12 Hz
# Beta  12 - 25 Hz
# Gamma > 25 Hz
# High Gamma 60 - 200 Hz
#
##########################################################
#ilData = ephysHelper.butter_bandpass_filter(il.data,0.1,20, il.fs)
#blaData = ephysHelper.butter_bandpass_filter(bla.data,0.1,20, bla.fs)
#BAND_PASSED = True
###########################################################

'''
# Side by side graph of power vs data.
fig, ax = plt.subplots(1,2)
nSampesToPlot = 10000
ax[0].plot(BandPassData[:10000])
#ax[1].plot(magcon.data[:10000])
'''
# Plot with events at the center (going to start later (halfway) for now because it took us awhile to decide on a threshold)
plotsIL = []
plotsBLA = []

BandPassIL = []
event_time_stamps = []
ERP_sums = []
ERP_valid_BLA_sums = []
ERP_valid_IL_sums = []
num_ERP_events = 0
windowLength = 3000  # Note: sample at 30 kHz.  10000 samples/30000 samples/s = 0.333 sec
                      # 100 ms = 0.1s = x samples/30000 samples/s ======> x = 3000 
for n in range(0,len(events.ts)): # For each time stamp (ts) in events file
    #print("event node:", events.nodeId[n], "event id: ", events.eventId)
    if events.nodeId[n] == 102 and events.eventId[n] == 1: # This was and ERP stim (These envets are found in Event class in Open Ephys Helper)
                                                           # channel 1 = threshold crossing, channel 2 = stim, (3 = sham, but not in ERP files)
        event_time_stamps.append(int(events.ts[n]))
        num_ERP_events +=1
        print(num_ERP_events)
        # if num >= 50 then switch ERP locations (30 now in prelim testing) 
        plotsIL.append(ilData[int(events.ts[n]-windowLength):int(events.ts[n]+windowLength*5)]) # For 3 sec after stim: (10k * 3) for 1 sec, *3)
    
        #BandPassIL.append(BandPassData[int(events.ts[n]-windowLength):int(events.ts[n]+windowLength)])
        plotsBLA.append(blaData[int(events.ts[n]-windowLength):int(events.ts[n]+windowLength*5)])
##        ERPsum = sum(abs(ilData[int(events.ts[n]+windowLength):int(events.ts[n]+windowLength*6)])) # For 3 sec after stim: (10k * 3) for 1 sec, *3)
##        print ("IL ERP SUM: ",ERPsum)  # ERP sums wait for 100 ms, then sum for another 500 ms
##        ERP_sums.append(ERPsum)

plotsILsum = [0] * len(plotsIL[0])
plotsBLAsum = [0] * len(plotsBLA[0])
plotsBLAavg = [0] * len(plotsBLA[0])
plotsILavg = [0] * len(plotsIL[0])
        
curr_pos = 0
good_curr_pos = 0

# WHICH AREA WAS STIMULATED FIRST FOR ERPS?
#print("\n\n\n\n\n")
#area_stimulated_1st = input("Which area did you stimulate first for ERPs? 1 = IL, 2 = BLA, any other ke = ?\n    ")
#usr_response = input("Use ARROW keys to go to next stim.  Up to include in summary. Press 'q' to quit\save")

# Left plot is bandpass filtered down to the high gamma. Use this to look for high amplitudes peaks that would cause the magnitude to go up.
# Right plot is the raw data (I was looking for artifacts that might cause thresholds)
#   And using it to look for stim artifacts after the threshold is crossed.
def key_event(e):
    global curr_pos, good_curr_pos, plotsBLAsum, plotsILsum, plotsBLAavg, plotsILavg, area_stimulated_1st
    ILDONE = False
    BLADONE = False
    if e.key == "right":
        curr_pos = curr_pos + 1
    elif e.key == "left":
        curr_pos = curr_pos - 1
    elif e.key == "up":  #Append ERP data
        if curr_pos < num_ERP_events:
            good_curr_pos = curr_pos
            if area_stimulated_1st == 1: # IL STIMULATED FIRST, LOOKING FOR BLA RESPONSES
                print ("num erp events: ",num_ERP_events)
                if curr_pos >= num_ERP_events/2 : #2nd
                    print("SAVING BLA ERP data")
                    ERP_valid_BLA_sums.append(sum(abs(plotsBLA[curr_pos][windowLength:windowLength*10]))) #windowLength = 100ms. * 5 = 500 ms
                    lis = [plotsBLA[curr_pos], plotsBLAsum]
                    plotsBLAsum = list(map(sum, zip(*lis)))
                    plotsBLAavg = [x/good_curr_pos for x in plotsBLAsum]
                    BLADONE = True
                    
                elif curr_pos < num_ERP_events/2: #ist
                    print("SAVING IL ERP data")
                    ERP_valid_IL_sums.append(sum(abs(plotsIL[curr_pos][windowLength:windowLength*10])))
                    lis = [plotsIL[curr_pos], plotsILsum]
                    plotsILsum = list(map(sum, zip(*lis)))
                    plotsILavg = [x/good_curr_pos for x in plotsILsum]
                    
                    
            else: # BLA stimmed first LOOKING FOR IL RESPONSES
                if curr_pos < num_ERP_events/2: #ist
                    print("SAVING BLA ERP data.  Cur pos: ",curr_pos)
                    ERP_valid_BLA_sums.append(sum(abs(plotsBLA[curr_pos][windowLength:windowLength*10])))
                    lis = [plotsBLA[curr_pos], plotsBLAsum]
                    plotsBLAsum = list(map(sum, zip(*lis))) # MARK???? Running sum
                    plotsBLAavg = [x/good_curr_pos for x in plotsBLAsum]
                    
                elif curr_pos >= num_ERP_events/2: #2nd
                    print("SAVING IL ERP data. Cur pos: ",curr_pos)
                    ERP_valid_IL_sums.append(sum(abs(plotsIL[curr_pos][windowLength:windowLength*10])))
                    lis = [plotsIL[curr_pos], plotsILsum]
                    plotsILsum = list(map(sum, zip(*lis)))
                    plotsILavg = [x/good_curr_pos for x in plotsILsum]
                    plotsILavg = [x/good_curr_pos for x in plotsILsum]
                    ILDONE = True
            good_curr_pos = curr_pos            
            curr_pos = curr_pos + 1
        else:
            print("DONE! Press 'Q' to save.  Cur pos: ",curr_pos)
    elif e.key == "dn":  #POP ERP data

        if area_stimulated_1st == 1: # IL STIMULATED FIRST, LOOKING FOR BLA RESPONSES
            if curr_pos < num_ERP_events/2: 
                print("REMOVING BLA ERP data")
                ERP_valid_BLA_sums.pop(sum(abs(plotsBLA[curr_pos][windowLength:windowLength*10]))) #windowLength = 100ms. * 5 = 500 ms
                lis = [plotsBLA[curr_pos], plotsBLAsum]
                plotsBLAsum = list(map(sum, zip(*lis)))
                plotsBLAavg = [x/good_curr_pos for x in plotsBLAsum]
                
            else:
                print("REMOVING IL ERP data")
                ERP_valid_IL_sums.pop(sum(abs(plotsIL[curr_pos][windowLength:windowLength*10])))
                lis = [plotsIL[curr_pos], plotsILsum]
                plotsILsum = list(map(sum, zip(*lis)))
                plotsILavg = [x/good_curr_pos for x in plotsILsum]
        else: # BLA stimmed first or dont know
            if curr_pos >= num_ERP_events/2: 
                print("REMOVING BLA ERP data")
                ERP_valid_BLA_sums.pop(sum(abs(plotsBLA[curr_pos][windowLength:windowLength*10])))
                lis = [plotsBLA[curr_pos], plotsBLAsum]
                plotsBLAsum = list(map(sum, zip(*lis)))
                plotsBLAavg = [x/good_curr_pos for x in plotsBLAsum]
                
            else:
                print("REMOVING IL ERP data")
                ERP_valid_IL_sums.pop(sum(abs(plotsIL[curr_pos][windowLength:windowLength*10])))
                lis = [plotsIL[curr_pos], plotsILsum]
                plotsILsum = list(map(sum, zip(*lis)))
                plotsILavg = [x/good_curr_pos for x in plotsILsum]                
         
        curr_pos = curr_pos - 1
        good_curr_pos = curr_pos 

    elif e.key == "q":
        if "ERP_PRE" in directory_only:
            ERP_TYPE = "PRE_ERP"
            idx_of_dot_in_name = drv_file_name.find(".")
            drv_chan = drv_file_name[0:idx_of_dot_in_name]
            idx_of_dot_in_name = tar_file_name.find(".")
            tar_chan = tar_file_name[0:idx_of_dot_in_name]            
            saveFile = "ERP_PRE_STIM_RESPONSES_" + drv_chan + "_and_" + tar_chan + ".txt"
            ERPs =  open(os.path.join(directory_only,saveFile), mode='a') #
        elif "ERP_5" in directory_only:
            ERP_TYPE = "POST__5"
            idx_of_dot_in_name = drv_file_name.find(".")
            drv_chan = drv_file_name[0:idx_of_dot_in_name]
            idx_of_dot_in_name = tar_file_name.find(".")
            tar_chan = tar_file_name[0:idx_of_dot_in_name]            
            saveFile = "ERP_5_MIN_POST_RESPONSES_" + drv_chan + "_and_" + tar_chan + ".txt"
            ERPs =  open(os.path.join(directory_only,saveFile), mode='a') #
        elif "ERP_30" in directory_only:
            ERP_TYPE = "POST_30"
            idx_of_dot_in_name = drv_file_name.find(".")
            drv_chan = drv_file_name[0:idx_of_dot_in_name]
            idx_of_dot_in_name = tar_file_name.find(".")
            tar_chan = tar_file_name[0:idx_of_dot_in_name]            
            saveFile = "ERP_30_MIN_POST_STIM_RESPONSES_" + drv_chan + "_and_" + tar_chan + ".txt"
            ERPs =  open(os.path.join(directory_only,saveFile), mode='a') #


        ERPs.write("ERPs on Channels: " + drv_file_name + "and" + tar_file_name + "\n")  #HEADER
        ERPs.write("Date, Time, RAT, direction_of_treatment, ERP_direction, MEAN, STDERRofMn, " + \
                                                "ERP_direction, MEAN, STDERRofMn\n ") #HEADER
                   
        meanIL_BLA = mean(ERP_valid_BLA_sums)
        meanBLA_IL = mean(ERP_valid_IL_sums)
                   
        std_error_of_meanIL_BLA = stats.sem(ERP_valid_BLA_sums)
        std_error_of_meanBLA_IL = stats.sem(ERP_valid_IL_sums)
                   
        #ERPs.write(str(round(BLA_ERP,2)) + "\n")

        ERPs.write(date +', ' + time +', '+RAT+", "+direction_of_treatment+ \
                   ", ERP IL->BLA, "+str(round(meanIL_BLA,3))+", " +\
                   str(round(std_error_of_meanIL_BLA,3))+\
                   ", ERP BLA->IL, "+  str(round(meanBLA_IL,3))+", " + \
                   str(round(std_error_of_meanBLA_IL,3))+"\n ")
##        ERPs.write(drv_file_name + "," + tar_file_name + "\n")
##        for IL_ERP in ERP_valid_IL_sums:
##            ERPs.write(str(round(IL_ERP,3)) + "\n")    
        ERPs.close()
        
        summary_file_path = initialDIR.strip()+"SUMMARY_ERPs_RAW.csv"
        if not os.path.exists(summary_file_path):
            SumaryFile =  open(summary_file_path, mode='a')
            SumaryFile.write("ERPs on Channels: " + drv_file_name + "and" + tar_file_name + "\n")  #HEADER
            SumaryFile.write("Date, Time, RAT, uAps, Lag_ms, Treatment, ERP_TIMING, ERP_IL-BLA, STDERRofMn_IL-BLA, + \
                              ERP_BLA-IL, STDERRofMn_BLA-IL\n ") #HEADER
            SumaryFile.write(date +', ' + time +', '+ RAT + ", " +  str(microamps) + ", " + str(stim_lag) + ", " + \
                   direction_of_treatment + "," + ERP_TYPE + ", " + str(round(meanIL_BLA,3))+", " +\
                   str(round(std_error_of_meanIL_BLA,3)) + ", "+  str(round(meanBLA_IL,3))+", " + \
                   str(round(std_error_of_meanBLA_IL,3))+",\n ")
            
        else:
            SumaryFile =  open(summary_file_path, mode='a')
            SumaryFile.write(date +', ' + time +', '+ RAT + ", " +  str(microamps) + ", " + str(stim_lag) + ", " + \
                   direction_of_treatment + "," + ERP_TYPE + ", " + str(round(meanIL_BLA,3))+", " +\
                   str(round(std_error_of_meanIL_BLA,3)) + ", "+  str(round(meanBLA_IL,3))+", " + \
                   str(round(std_error_of_meanBLA_IL,3))+",\n ")

        print("DONE!")
        SumaryFile.close()



        
        return
           
    else:
        return
    print("curr pos: ",curr_pos, "len(plotsIL: ", len(plotsIL))
    curr_pos = curr_pos % len(plotsIL) #### ????? Always curr_pos???
    
    ax0.cla()
    ax1.cla()
    ax2.cla()
    ax3.cla()
    #ax[2].cla()
    #####################################
    #  PLOTS
    #####################################
    #   0   |  |   2
    # ______|  |_______
    # ______    _______
    #       |  |
    #   1   |  |   3
    #
    #################
    # PLOT 0
    ax0.plot(plotsIL[curr_pos])
    #ax0.set_ylim(-1000,2000)
    ax0.axvline(windowLength, color='r')
    ax0.axvline(windowLength, color='b')
    ax0.axvline(windowLength*5, color='b')
    ax0.axhline(0, color = 'b')
    ax0.set_ylabel('Magnitude (mV)',fontsize = 12)
    ax0.set_ylim(-6000,6000)
    if curr_pos < num_ERP_events/2: 
            ax0.set_title('RAW (CAR) DATA from STIMULATED Area (IL)' + drv_file_name + ")", fontsize= 12)
    else:
            ax0.set_title('RAW (CAR) DATA from TARGET Area (IL)' + drv_file_name + ")", fontsize = 12)

    #################
    # PLOT 1
    ax1.plot(plotsBLA[curr_pos])
    #ax1.set_ylim(-1000,2000)
    ax1.axvline(windowLength, color = 'r')
    ax1.axvline(windowLength, color='b')
    ax1.axvline(windowLength*5, color='b')
    ax1.axhline(0, color = 'b')
    ax1.set_ylabel('Magnitude (mV)', fontsize=12)
    ax1.set_ylim(-6000,6000)
    if curr_pos < num_ERP_events/2: 
        ax1.set_title('RAW (CAR)  DATA from TARGET Area (BLA)' + tar_file_name + ")", fontsize=12)
    else:
        ax1.set_title('RAW (CAR)  DATA from STIMULATED Area (BLA)' + tar_file_name + ")", fontsize = 12)
        
    ax1.set_xlabel('Event time (s): ' + str(round(event_time_stamps[curr_pos]/30000,3))) # 30,000 samples per sec

    ######################
    # PLOT 2
    # PLOT ONLY GOOD CASES
    ax2.plot(plotsILavg)
    ax2.set_ylim(-6000,6000)
    ax2.axvline(windowLength, color='r')
    #ax2.axvline(windowLength, color='b')
    ax2.axvline(windowLength*5, color='g')
    ax2.axhline(0, color = 'b')
    ax2.set_ylabel('Magnitude (mV)',fontsize = 12)
    if curr_pos < num_ERP_events/2: 
        ax2.set_title('Low passed CAR (<20Hz)DATA of STIMULATED Area (IL)' + drv_file_name + ")", fontsize= 12)
    else:
        ax2.set_title('Low passedCAR (<20Hz) of TARGET Area (IL)' + drv_file_name + ")", fontsize = 12)
    x = range(windowLength,windowLength*5)   #### range(int(events.ts[n]+windowLength),int(events.ts[n]+windowLength*5))
    print(windowLength)
    print(len(plotsILavg))
    ax2.fill_between(x, 0, plotsILavg[windowLength:windowLength*5])

    ######################
    # PLOT 3   
    ax3.plot(plotsBLAavg)
    ax3.set_ylim(-6000,6000)
    ax3.axvline(windowLength, color = 'r')
    #ax3.axvline(windowLength, color='g')
    ax3.axvline(windowLength*5, color='g')
    ax3.axhline(0, color = 'b')
    ax3.set_ylabel('Magnitude (mV)', fontsize=12)
    if curr_pos < num_ERP_events/2: 
        #ax3.set_title('RAW (CAR)  DATA from Target Area (BLA)' + tar_file_name + ")", fontsize=18)
        ax3.set_title('Avg low passed CAR (<20Hz)DATA of TARGET Area (BLA)' , fontsize=12)
    else:
        #ax3.set_title('RAW (CAR)  DATA from Driving Area (BLA)' + tar_file_name + ")", fontsize = 18)
        ax3.set_title('Avg low passed CAR(<20Hz)DATA from STIMULATED Area (BLA)', fontsize = 12)
        
    #ax3.set_xlabel('Event time (s): ' + str(round(event_time_stamps[good_curr_pos]/30000,3))) # 30,000 samples per sec
    ax3.set_xlabel('Samples ('+ str(curr_pos)+")") ### + str(round(event_time_stamps[good_curr_pos]/30000,3)))
    x = range(windowLength,windowLength*5)   #### range(int(events.ts[n]+windowLength),int(events.ts[n]+windowLength*5))
    ax3.fill_between(x, 0, plotsBLAavg[windowLength:windowLength*5])
    fig.canvas.draw()

print('IL size : ' , len(plotsIL))
#fig, ax = plt.subplots(2,2)
fig, ((ax0, ax2), (ax1, ax3)) = plt.subplots(2, 2, sharex='col') ##, sharey='row')




fig.canvas.mpl_connect('key_press_event', key_event) #Starts a separate process which waits for key events
ax0.plot()
ax1.plot()
ax2.plot()
ax3.plot()
#ax[2].plot()
fig.tight_layout()
plt.show()




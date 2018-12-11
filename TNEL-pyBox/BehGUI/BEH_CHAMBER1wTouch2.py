#
"""
NOTE: 1. Please Start Whisker server first
      2. Check daqAPI.py on this directory.
         be sure Devices are named properly:

         on Ephis-1 'Dev1' runs behavior box
                    'pciDAQ' runs open ephys

         on Ephis-2 'Dev2' runs behavior box
                    'Dev1' runs open ephis
Developed by Flavio J.K. da Silva and  Mark Schatza Nov. 31, 2018


"""

from win32api import GetSystemMetrics
import os
import sys, errno, time, calendar
import pygame
import math, random
import numpy as np
import zmq
import json
import pickle
#import pylab
from NIDAQ_GUI_elements import *
from RESOURCES.GUI_elements_by_flav import play_sound

##from helperFunc import *
##import daqAPI
##NIDAQ_AVAILABLE = True
try:
    from helperFunc import *
    import daqAPI
    NIDAQ_AVAILABLE = True
except:
    NIDAQ_AVAILABLE = False

from collections import deque

from multiprocessing import Process, Queue
import threading
import childVid
import whiskerTouchZMQ
import zmqClasses
import eventRECV

#import BEHTouchscreen
# Reading an excel file using Python
#import openpyxl, xlrd, xlwt
#from xlwt import Workbook
#from openpyxl import load_workbook
################################################################
# GUI GLOBALS
################################################################
SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)
print("SCREEN WIDTH: ", SCREEN_WIDTH)
print("SCREEN HEIGHT: ", SCREEN_HEIGHT)
WINDOW_WIDTH = SCREEN_WIDTH - 100
WINDOW_WCENTER = WINDOW_WIDTH/2
WINDOW_HEIGHT = SCREEN_HEIGHT -100
WINDOW_HCENTER = WINDOW_HEIGHT/2
GAME_AREA = pygame.Rect(20, 10, WINDOW_WIDTH, WINDOW_HEIGHT)
random.seed()

################################################################
# NIDAQ GLOBALS
################################################################
# OUTPUTS
if NIDAQ_AVAILABLE:
    fan = daqAPI.fanSetup()
    cabin_light = daqAPI.cabinLightSetup()
    leverOut = daqAPI.leverOutputSetup()
    food_light = daqAPI.foodLightSetup()
    give_food = daqAPI.giveFoodSetup()
    apply_shock = daqAPI.shockerSetup()
    high_tone = daqAPI.highToneSetup()

    L_condition_Lt = daqAPI.conditioningLightsLeftSetup()
    R_condition_Lt = daqAPI.conditioningLightsRightSetup()

    #high_tone.sendDBit(False)
    #low_tone = daqAPI.lowToneSetup()
    #low_tone.sendDByte(0)


    #INPUTS
    L_nose_poke = daqAPI.leftNoseInputSetup()
    R_nose_poke = daqAPI.rightNoseInputSetup()
    checkPressLeft, checkPressRight = daqAPI.leverInputSetup()
    eaten = daqAPI.foodEatInputSetup()

##################
# DATA
##################
cwd = os.getcwd()
print(cwd)
datapath = os.path.join(cwd,'DATA' )
print("....")
print (datapath)

expt_file_name = 'protocol_habituation_and_conditioning.txt'
expt_file_path_name = os.path.join(datapath,expt_file_name )
print("EXPT FILE TO LOAD: ",expt_file_path_name)

date = time.strftime("%b_%d_%y")#month-day-Year-H:M
dateTm = time.strftime("%b_%d_%y-%H_%M")#month-day-Year-H:M
print(date)

##
log_file_name = ''
log_file_path_name = ''
video_file_name = ''
video_file_path_name = ''
data_file_name = ''
data_file_path_name = ''
TOUCH_IMG_PATH = ''
touch_img_files = []
VIs_file_path = ''
habituation_vi_times = []
conditioning_vi_times = []
extinction_vi_times = []
recall_vi_times = []
################################################################
# VIDEO GLOBALS
################################################################
vidDict = {}
q = deque(maxlen = 1) # Most recent
back_q = Queue()

################################################################
# TOUCH GLOBALS
################################################################
TSq = Queue()
#TSback_q =  Queue() # FIFO
whiskerBack_q = Queue()
TOUCH_TRHEAD_STARTED = False


################################################################
# GENERAL GLOBALS
################################################################
Tone1_Duration = 1.0 # sec
Tone1_Freq = 450.0
Tone1_Vol = 1.0
Tone2_Duration = 1.0 # sec
Tone2_Freq = 1800.0
Tone2_Vol = 0.5
TONE_ON = False
Shock_Duration = 1.0
Shock_V = 9.0
Shock_Amp = 0.5

Expt_Name = '1'
Subject ='1'
trial_num = 0
num_pellets = 0
EXPT_FILE_LOADED = False

setup = []
protocol = []
conditions = []

L_LEVER_EXTENDED = False
R_LEVER_EXTENDED = False
LEVERS_EXTENDED = False
TOUCHSCREEN_USED = False
var_interval_reward = 0.0
BAR_PRESS_INDEPENDENT_PROTOCOL = False
################################################################

def FAN_ON_OFF(events,FAN_ON,cur_time):
    global fan, NIDAQ_AVAILABLE
    if FAN_ON:
        log_event(events,"Fan_ON",cur_time)
        if NIDAQ_AVAILABLE:    fan.sendDBit(True)
    else:
        log_event(events,"Fan_OFF",cur_time)
        if NIDAQ_AVAILABLE:    fan.sendDBit(False)
        #fan.end()

def PLAY_TONE(events,TONE_ID,cur_time):
    global Tone1_Duration, Tone1_Freq, Tone1_Vol,  Tone2_Duration, Tone2_Freq, Tone2_Vol, TONE_TIME,TONE_ON
    # NOTE: Tone_OFF logged while drawing speeker above in main loop
    if TONE_ID == 'TONE1':
        log_event(events,"Tone_ON",cur_time,("Freq(Hz)", str(Tone1_Freq), "Vol(0-1)",str(Tone1_Vol), "Duration(S)",str(Tone1_Duration)))

        newThread = threading.Thread(target=play_sound, args=(Tone1_Freq, Tone1_Vol,Tone1_Duration))

    elif TONE_ID == 'TONE2':
        log_event(events,"Tone_ON",cur_time,("Freq(Hz)", str(Tone2_Freq), "Vol(0-1)",str(Tone2_Vol), "Duration(S)",str(Tone2_Duration)))
        newThread = threading.Thread(target=play_sound, args=(Tone2_Freq, Tone2_Vol,Tone2_Duration))

    newThread.start()
    TONE_TIME = cur_time
    TONE_ON = True

def CAB_LIGHT(events,ON_OFF,cur_time):
    global cabin_light, NIDAQ_AVAILABLE
    gray        = (100,100,100)
    darkgray    = (50,50,50)
    if ON_OFF: # ON
       log_event(events,"Cabin Light ON",cur_time)
       Background_color = gray
       #cabin_light = daqAPI.cabinLightSetup()
       if NIDAQ_AVAILABLE:  cabin_light.sendDBit(True)

    else: # ON_OFF = False
       log_event(events,"Cabin Light OFF",cur_time)
       Background_color = darkgray
       if NIDAQ_AVAILABLE: cabin_light.sendDBit(False)
       #cabin_light.end()
    return Background_color


def EXTEND_LEVERS(events,text, L_LVR,R_LVR,cur_time):
    global leverOut, NIDAQ_AVAILABLE,L_LEVER_EXTENDED,R_LEVER_EXTENDED,LEVERS_EXTENDED
    if L_LVR and R_LVR: # Extend both levers
        if NIDAQ_AVAILABLE:  leverOut.sendDByte(3)
        log_event(events,text ,cur_time)
        LEVERS_EXTENDED = True
        R_LEVER_EXTENDED = True
        L_LEVER_EXTENDED = True

    elif L_LVR:  # Extend L lever only
        if NIDAQ_AVAILABLE:  leverOut.sendDByte(1)
        log_event(events,text ,cur_time)
        LEVERS_EXTENDED = False
        R_LEVER_EXTENDED = False
        L_LEVER_EXTENDED = True
    elif R_LVR:  # Extend R lever only
        if NIDAQ_AVAILABLE:  leverOut.sendDByte(2)
        log_event(events,text,cur_time)
        LEVERS_EXTENDED = False
        R_LEVER_EXTENDED = True
        L_LEVER_EXTENDED = False
    else: # Retract both
        if NIDAQ_AVAILABLE:  leverOut.sendDByte(0)
        log_event(events,text ,cur_time)
        LEVERS_EXTENDED = False
        R_LEVER_EXTENDED = False
        L_LEVER_EXTENDED = False

def L_CONDITIONING_LIGHT(events,ON_OFF,cur_time):
    global L_condition_Lt, NIDAQ_AVAILABLE
    if ON_OFF : # ON
       log_event(events,"Left_Light_ON",cur_time)
       if NIDAQ_AVAILABLE:  L_condition_Lt.sendDBit(True)

    else: # ON_OFF = False
       log_event(events,"Left_Light_OFF",cur_time)
       if NIDAQ_AVAILABLE:  L_condition_Lt.sendDBit(False)

def R_CONDITIONING_LIGHT(events,ON_OFF,cur_time):
    global R_condition_Lt,NIDAQ_AVAILABLE
    if ON_OFF: # ON
       log_event(events,"Right_Light_ON",cur_time)
       if NIDAQ_AVAILABLE:   R_condition_Lt.sendDBit(True)

    else: # ON_OFF = False
       log_event(events,"Right_Light_OFF",cur_time)
       if NIDAQ_AVAILABLE:   R_condition_Lt.sendDBit(False)

def Food_Light_ONOFF (events,ON_OFF,cur_time):
    global food_light, NIDAQ_AVAILABLE
    gray = (100,100,100)
    black = (0,0,0)
    if ON_OFF: # ON
          fill_color = gray
          LEDsONOFF = "ON"
          log_event(events,"Feeder_Light_ON",cur_time)
          if NIDAQ_AVAILABLE:  food_light.sendDBit(True)

    else:
          fill_color = black
          LEDsONOFF = "OFF"
          if NIDAQ_AVAILABLE:  food_light.sendDBit(False)
          log_event(events,"Feeder_Light_OFF",cur_time)

    return fill_color,LEDsONOFF


def FOOD_REWARD(events, text,cur_time):
    global give_food, num_pellets, NIDAQ_AVAILABLE
    log_event(events,text,cur_time)
    num_pellets +=1
    if NIDAQ_AVAILABLE:
        give_food.sendDBit(True)
        give_food.sendDBit(False)

def log_event(event_lst, event, cur_time, other=''):
    global log_file_path_name
    time = str(cur_time)
    print("time: ",time)
    print("Log file: ", log_file_path_name, cur_time)
    event_string = time + ',  ' + event
    #print (event_string, other)
    event_other = ''
    for item in other:
        #print (item)
        event_other = event_other + ",  " +  str(item)

    event_lst.append(event_string+event_other) # To Display on GUI
    try:
        #print(log_file_path_name)
        log_file = open(log_file_path_name,'a')         # OPEN LOG FILE
        log_file.write(event_string + event_other + '\n')   # To WRITE TO FILE
        log_file.close()                                #CLOSE LOG FILE
    except:
        print ('Log file not created yet. Check EXPT PATH, then Press "LOAD EXPT FILE BUTTON"')


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def StartTouchScreen():
    global TOUCH_TRHEAD_STARTED, TOUCH_IMG_PATH, whiskerBack_q, TSq
    '''
    Generates a bandit task. NO SPACES IN FILENAMES!

    '''

    global TOUCH_IMG_PATH,touch_img_files

    if not TOUCH_TRHEAD_STARTED:
        whiskerThread = threading.Thread(target = whiskerTouchZMQ.main, args=(whiskerBack_q,TSq))#, kwargs=({'media_dir' : TOUCH_IMG_PATH}))

        whiskerThread.start()
        TOUCH_TRHEAD_STARTED = True


##    for p in range(num_loops):
##        TSq.put({'end' : False, 'next' : True, 'pics': touch_img_files})
##
##    TSq.put({'end' : True})

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def MyVideo():
    global vidDict, q , back_q
    if vidDict['STATE'] == 'ON':
          print("STATE: ",vidDict['STATE'])
          p = threading.Thread(target=childVid.vidCapture, args=(q,back_q,))
          print (p)
          p.start()
          q.append(vidDict)
          while True:
              if not back_q.empty():
                  msg = back_q.get()
                  if msg == 'vid ready':
                      return


def exit_game():
    global NIDAQ_AVAILABLE
    #DataFile.close()
    if NIDAQ_AVAILABLE:
      fan.end()
      cabin_light.end()
      food_light.end()
      give_food.end()
      eaten.end()

      leverOut.end()

      L_condition_Lt.end()
      R_condition_Lt.end()
      high_tone.end()
      L_nose_poke.end()
      R_nose_poke.end()
      checkPressLeft.end()
      checkPressRight.end()

    pygame.quit()
    sys.exit()

def load_expt_file(expt_file_path_name):
    global protocol, conditions
    global Expt_Name, Subject
    global Tone1_Duration, Tone1_Freq, Tone1_Vol,Tone2_Duration, Tone2_Freq, Tone2_Vol
    global Shock_Duration,Shock_V,Shock_Amp
    global datapath, log_file_path_name, data_file_path_name, video_file_path_name, VIs_file_path
    global TOUCH_IMG_PATH, touch_img_files, TOUCHSCREEN_USED
    global var_interval_reward,     BAR_PRESS_INDEPENDENT_PROTOCOL
    global habituation_vi_times, conditioning_vi_times, extinction_vi_times, recall_vi_times

    print("LOADING: ", expt_file_path_name)
    protocol = []
    conditions = []
    lines = []


    try:
        f = open(expt_file_path_name,'r')
        # Read Line by line

        for line in f:
            line = line.strip() # Remove leading and trailoing blanks and \n
            line = line.upper()
            print(line)
            lines.append(line)
            if line != "":
                condition={}

                if '[EXPERIMENT' in line:
                    EXPERIMENT = True
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False
                elif '[TONE1' in line:
                    EXPERIMENT = False
                    TONE1 = True
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False
                elif '[TONE2' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = True
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False
                elif '[SHOCK]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = True
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False
                elif '[FREEZE]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = True
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False

                elif '[TOUCHSCREEN]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = True
                    BAR_PRESS = False
                    SETUP = False
                elif '[BAR_PRESS]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = True
                    SETUP = False

                elif '[PROTOCOL' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = True
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False

                elif '[CONDITIONS' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = True
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False

                elif '[SETUP' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = True
                    
                elif '[END' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False


                if EXPERIMENT:
                    if 'EXPT_NAME' in line:
                        words = line.split('=')
                        Expt_Name = words[1].strip()
                        Expt_Name = Expt_Name.strip()
                        print(Expt_Name)

                    elif 'SUBJECT' in line:
                        words = line.split('=')
                        Subject = words[1].strip()
                        Subject = Subject.strip()
                        print(Subject)

                    elif 'EXPT_PATH' in line:
                        words = line.split('=')
                        datapath = words[1].strip()
                        datapath = datapath.strip()
                        print(datapath)
                    elif 'LOG_FILE_PATH' in line:
                        words = line.split('=')
                        log_file_path = words[1].strip()
                        log_file_path = log_file_path.strip()
                        print("LFP",log_file_path)
                    elif 'VIDEO_FILE_PATH' in line:
                        words = line.split('=')
                        video_file_path = words[1].strip()
                        video_file_path = video_file_path.strip()
                        print(video_file_path)
                    elif 'OPEN_EPHYS_PATH' in line:
                        print('opening ephys')
                        words = line.split('=')
                        open_ephys_path = words[1].strip()
                        print(open_ephys_path)
                        open_ephys_thread = threading.Thread(target=os.system, args=(open_ephys_path,))
                        open_ephys_thread.start()
                        
                    elif 'VI_TIMES_LIST_PATH' in line:
                        words = line.split('=')
                        VIs_file_path = words[1].strip()
                        print(VIs_file_path)

                elif TONE1:#TONE1
                    if 'DURATION' in line:
                        words = line.split('=')
                        Tone1_Duration = float(words[1].strip())
                        print("Tone1_Duration",Tone1_Duration)
                    if 'FREQ' in line:
                        words = line.split('=')
                        Tone1_Freq = float(words[1].strip())
                        print("Tone1_Freq: ",Tone1_Freq)
                    if 'VOL' in line:
                        words = line.split('=')
                        Tone1_Vol = float(words[1].strip())
                        print("Tone1_Vol: ",Tone1_Vol)

                elif TONE2:#TONE2
                    if 'DURATION' in line:
                        words = line.split('=')
                        Tone2_Duration = words[1].strip()
                        print("Tone2_Duration",Tone2_Duration)
                    if 'FREQ' in line:
                        words = line.split('=')
                        Tone2_Freq = float(words[1].strip())
                        print("Tone2_Freq: ",Tone2_Freq)
                    if 'VOL' in line:
                        words = line.split('=')
                        Tone2_Vol = float(words[1].strip())
                        print("Tone2_Vol: ",Tone2_Vol)

                elif TOUCH:
                    touch_image_dict={}
                    if 'IMAGES_PATH' in line:
                        words = line.split('=')
                        TOUCH_IMG_PATH = words[1].strip()
                        print("\n\nTOUCH_IMG_PATH: ",TOUCH_IMG_PATH)
                        TOUCHSCREEN_USED = True
                    elif 'IMG' in line:
                        words = line.split('=')
                        image_name = words[0].strip()
                        image_file_name_coord = words[1].split(",")
                        img_file_name = image_file_name_coord[0].strip()
                        x = image_file_name_coord[1].strip()
                        x = x.strip("(")
                        y = image_file_name_coord[2].strip()
                        y = y.strip(")")
                        touch_image_dict[img_file_name] = (int(x),int(y))
                        touch_img_files.append(touch_image_dict)

                elif BAR_PRESS:
                    BAR_PRESS_INDEPENDENT_PROTOCOL = True
                    if "VI" in line:
                        words = line.split('=')
                        VI = words[1].strip()
                        try:
                            var_interval_reward = int(VI)
                            print("var_interval_reward: ",var_interval_reward)
                        except:
                            print ("!!!!!!!!!!!VI must = a number in EXP file!!!!!!!!!!!!!!", )

                elif SHOCK:
                    if 'DURATION' in line:
                        words = line.split('=')
                        SDuration = words[1].strip()
                        Shock_Duration = float(SDuration.strip())
                        print(Shock_Duration)
                    if 'VOLTS' in line:
                        words = line.split('=')
                        V = words[1].strip()
                        Shock_V = float(V.strip())
                        print(Shock_V)
                    if 'AMPS' in line:
                        words = line.split('=')
                        amps = words[1].strip()
                        Shock_Amp = float(amps.strip())
                        print(Shock_Amp)

                elif FREEZE:
                    if 'DURATION' in line:
                        words = line.split('=')
                        Freeze_Duration = words[1].strip()
                        Freeze_Duration = Freeze_Duration.strip()
                        #print(Freeze_Duration)
                    if 'PIX' in line:
                        words = line.split('=')
                        Min_Pixels = words[1].strip()
                        Min_Pixels = Min_Pixels.strip()
                        #print(Min_Pixels)

                elif SETUP:
                    if "SETUP" not in line:
                        #print(line)
                        try:
                            words = line.split('=')
                            word1 = words[0].strip()
                            word1 = word1.upper()
                            word2 = words[1].strip() #Do NOT make this an upper() to retain True and False
                            word2 = word2.split("#") #IGNORES "#" FOLLOWED BY COMMENTS
                            word2 = word2[0].strip()
                            setup.append({word1:word2})
                        except:
                            setup.append({line:True}) # For lines without an '=' in them
                            #if line == 'END': PROTOCOL = False

                elif PROTOCOL:
                    if "PROTOCOL" not in line:
                        #print(line)
                        try:
                            words = line.split('=')
                            word1 = words[0].strip()
                            word1 = word1.upper()
                            word2 = words[1].strip() #Do NOT make this an upper() to retain True and False
                            word2 = word2.split("#") #IGNORES "#" FOLLOWED BY COMMENTS
                            word2 = word2[0].strip()
                            protocol.append({word1:word2})
                        except:
                            protocol.append({line:True}) # For lines without an '=' in them
                            #if line == 'END': PROTOCOL = False

                elif CONDITIONS:
                    print("CONDITIONS: ",line)
                    if "[CONDITIONS]" in line:
                        KEY_LINE = True

                    elif KEY_LINE: # CONDITION HEADING (i.e. all the KEYS)
                        keys = line.split(',') #list of condtions but need to be stripped of blanks and tabs
                        #print ("KEYS: ", keys)
                        KEY_LINE = False
                    else: # Not a CONDITION heading line, (i.e. all the VALUES)
                        values = line.split(',')
                        #print ("VALUES: ",values)

                        i=0
                        for val in values:
                            val = val.strip()
                            val = val.upper()
                            val = convertString(val)
                            condition[keys[i].strip()] = val #This strips keys, assigns a val to the key and creates condition dict

                            i+=1
                        conditions.append(condition)
                        #print (condition)
                else:
                    END_PROTOCOL = True
            else:# line == ""
                print("BLANK LINE")

        f.close()
        print(".......\n")
        print(touch_img_files)
    except:
        print("NO SUCH FILE!!!!",expt_file_path_name)
        return False

    # DATA PATH + FILES
    try:
        expt_file_name_COPY = Expt_Name + "-" + Subject + '-' +  dateTm + '-EXPT_file'  + '.txt'
        expt_file_path_name_COPY = os.path.join(datapath,expt_file_name_COPY)
        print(expt_file_path_name_COPY)

        log_file_name = Expt_Name + "-" + Subject + '-' +  dateTm + '-LOG_file'  + '.txt'
        log_file_path_name = os.path.join(log_file_path,log_file_name)
        print(log_file_path_name)

        video_file_name = Expt_Name + "-" + Subject + '-' +  dateTm + '-VIDEO_file' + '.avi'
        video_file_path_name = os.path.join(video_file_path,video_file_name)
        print(video_file_path_name)
    except:
        print("Could not create data file names")
    try:
        exf = open(expt_file_path_name_COPY,'w')
        for l in lines:
            #print(l)
            exf.write(l+"\n")
        exf.close()
    except:
        print("could not write copy of EXPT file",expt_file_path_name_COPY)

    print("[PROTOCOL LOADED]")
    print (protocol)
    for dct in protocol:
        for k,v in dct.items():
            print(str(k)+" = " + str(v))


    if VIs_file_path != "":
        try:
            f = open(VIs_file_path,'r')
                # Read Line by line

            for line in f:
                line = line.strip() # Remove leading and trailoing blanks and \n
                line = line.upper()        
                print(line)
                if "HABITUATION" in line:
                    words = line.split(':')
                    words = words[1].strip()
                    words = words.split(',')
                    print("length of words: ",len(words))
                    for items in words:
                        num = items.strip()
                        print(num)
                        habituation_vi_times.append(int(num))
                if "CONDITIONING" in line:
                    words = line.split(':')
                    words = words[1].strip()
                    words = words.split(',')
                    print("length of words: ",len(words))
                    for items in words:
                        num = items.strip()
                        print(num)
                        conditioning_vi_times.append(int(num))
                if "EXTINCTION" in line:
                    words = line.split(':')
                    words = words[1].strip()
                    words = words.split(',')
                    print("length of words: ",len(words))
                    for items in words:
                        num = items.strip()
                        print(num)
                        extinction_vi_times.append(int(num))
                if "RECALL" in line:
                    words = line.split(':')
                    words = words[1].strip()
                    words = words.split(',')
                    print("length of words: ",len(words))
                    for items in words:
                        num = items.strip()
                        print(num)
                        recall_vi_times.append(int(num))
        except:
            print("Could not open ",VIs_file_path)
            return False
    return True

##       whiskerThread = threading.Thread(target = whiskerTouchZMQ.main, args=(whiskerBack_q), kwargs=({'media_dir' : TOUCH_IMG_PATH}))
##       print("STARTING TOUCH THREAD")

#######################################################################################XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def draw_speeker(myscreen, x, y, TONE_ON):
        if TONE_ON: col = (0,255,0)
        else:       col = (0,0,0)
        speeker = pygame.draw.circle(myscreen,col,(x, y),40,2)
        #speeker = pygame.draw.circle(myscreen,col,(230,70),40,2)
        incr = 0
        for c in range (4):
              pygame.draw.circle(myscreen,col,(x-23+incr,y-15),5,1)
              #pygame.draw.circle(myscreen,col,(207+incr,55),5,1)
              incr += 15
        incr = 0
        for c in range (5):
              pygame.draw.circle(myscreen,col,(x-30+incr,y),5,1)
              #pygame.draw.circle(myscreen,col,(200+incr,70),5,1)
              incr += 15
        incr = 0
        for c in range (4):
              pygame.draw.circle(myscreen,col,(x-23+incr,y+15),5,1)
              incr += 15

        return speeker # Returns a Rect object.  Neede to see if mouse clicked on icon

def draw_camera(myscreen,fill_color, CAMERA_ON, REC, x, y, w,h, linew):
        half_h = h/2
        pt1 = (x + w,y+half_h)
        pt2 = (x+w+20,y)
        pt3 = (x+w+20,y+h)
        ptlist = [pt1,pt2,pt3]
        pygame.draw.polygon(myscreen, fill_color, ptlist, 0)#
        camera = pygame.draw.rect(myscreen,fill_color, (x, y, w,h), 0)
        if REC:       col = (255,0,0)
        elif CAMERA_ON: col = (0,255,0)
        else:           col = (0,0,0)
        pygame.draw.polygon(myscreen, col, ptlist, linew)#
        pygame.draw.rect(myscreen,col, (x, y, w,h), linew)
        return camera

def draw_lighting(surface, SHOCK_ON, x,y,scale,color,width):
        if SHOCK_ON: col = (255,0,0)
        else: col = (0,0,0)
        pt1 = (x,y)
        pt2 = (x-4,y+10)
        pt3 = (x-1, y+10)
        pt4 = (x-6,y+20)
        pt5 = (x-3,y+20)
        pt6 = (x-8,y+30)

        pt7 = (x+2,y+20)
        pt8 = (x,y+20)
        pt9 = (x+7,y+10)
        pt10 = (x+4,y+10)
        pt11 = (x+11,y)
        ptlist = [pt1,pt2,pt3,pt4,pt5,pt6,pt7,pt8,pt9,pt10,pt11]
        pygame.draw.polygon(surface, color, ptlist, 0)#top white line
        pygame.draw.polygon(surface, (0,0,0), ptlist, 1)#top white line
        lightning = pygame.draw.circle(surface,col,(x+2,y+15),23,2)
        return lightning # Returns a Rect object.  Neede to see if mouse clicked on icon

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
################################################################################
#  MAIN PROGRAM
################################################################################
def BehavioralChamber():
    global vidDict, q, back_q, num_pellets
    global Expt_Name, Subject, EXPT_FILE_LOADED
    global datapath, expt_file_name, expt_file_path_name,log_file_path_name,video_file_path_name,data_file_path_name,TOUCH_IMG_PATH
    global Tone1_Duration, Tone1_Freq, Tone1_Vol,  Tone2_Duration, Tone2_Freq, Tone2_Vol
    global Shock_Duration,Shock_V,Shock_Amp, trial_num
    global L_LEVER_EXTENDED,R_LEVER_EXTENDED,LEVERS_EXTENDED, TONE_ON, TOUCHSCREEN_USED, BAR_PRESS_INDEPENDENT_PROTOCOL

#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20,40)
    myscreen = pygame.display.set_mode((460,990),pygame.RESIZABLE,32)
    UMNlogo = pygame.image.load(r'.\RESOURCES\UMNlogo.png')
    pygame.display.set_icon(UMNlogo)
    TNElogo = pygame.image.load(r'.\RESOURCES\TNE logo.jpg')
    TNElogo = pygame.transform.scale(TNElogo, (70, 50))
    pygame.display.set_caption('Behavioral Chamber Control 1.0 by F. da Silva and M. Shatza Oct. 30, 2018') # Enter your window caption here
    #by Flavio J.K. da Silva and Mark Shatza Oct. 30, 2018') #
    pygame.init()

    #############
    #
    #  Create Menu GUI elements
    #
    #############

    red         = (255,0,0)
    green       = (0,255,0)
    blue        = (0,0,255)
    gray        = (100,100,100)
    darkgray    = (50,50,50)
    lightgray   = (200,200,200)
    black       = (0,0,0)
    white       = (255,255,255)
    yellow      = (255,255,0)
    lightpurple  = (160,12,75)
    darkpurple  = (51,5,25)


    # FLAGS
    NEW_BUTTON = False
    LEFT_MOUSE_DOWN = False
    BUTTON_SELECTED = False
    LBL_SELECTED = False
    LED_SELECTED = False
    BOX_SELECTED = False
    CIRC_SELECTED = False
    SLIDER_SELECTED = False

    CORNER_SET = False
    DELETE_ITEM = False

    buttons = []
    levers = []
    boxes = []
    circles = []
    LEDs = []
    toggles = []
    sliders = []
    labels = []
    info_boxes = []
    user_inputs = []
    events = []
    buttons,levers,boxes,circles,LEDs,toggles,sliders,info_boxes,user_inputs,labels = NIDAQ_GUI_ELEMENTS(myscreen,buttons,levers,boxes,circles,LEDs,toggles,sliders,info_boxes,user_inputs,labels)
    print(len(buttons), " buttons")
    print(len(levers), " levers")
    print(len(boxes), " boxes")
    print(len(circles), " circles")
    print(len(LEDs), " LEDs")
    print(len(toggles), " toggles" )
    print(len(sliders), " sliders")
    print(len(labels), " labels")
    print(len(info_boxes), " info_boxes")
    print(len(info_boxes), " user_imputs")
    # USER INPUTS DEFAULT VALUES
    for user_input in user_inputs:
        if user_input.label == "EXPT":
             user_input.text = str(Expt_Name)
        elif user_input.label == "SUBJECT":
             user_input.text = str(Subject)
        elif user_input.label == "TRIAL":
             user_input.text  = str(trial_num)
        elif user_input.label == "EXPT PATH":
             user_input.text = str(datapath)
        elif user_input.label == "EXPT FILE NAME":
             user_input.text = str(expt_file_name)
        elif user_input.label == "Spk(S)":
             user_input.text  = str(Tone1_Duration)
        elif user_input.label == "Freq(Hz)":
             user_input.text  = str(Tone1_Freq)
        elif user_input.label == "Vol(0-1)":
             user_input.text  = str(Tone1_Vol)
        elif user_input.label == "Shck(S)":
             user_input.text = str(Shock_Duration)
        elif user_input.label == "V":
             user_input.text = str(Shock_V)
        elif "Amps" in user_input.label: # == "Amps"
             user_input.text = str(Shock_Amp)

    # MAIN LOOP
    clk_time_start = time.perf_counter()
    print (clk_time_start)
    FAN_0N = False
    CAB_LIGHT_ON = False
    Background_color = (darkgray)
    FEEDER_LT_ON = False

    START_TIME = time.perf_counter()
    LEVER_PRESS_TIME = START_TIME
    NOSE_POKE_TIME = START_TIME
    TONE_TIME = START_TIME
    SHOCK_TIME = START_TIME

    num_L_nose_pokes = 0
    num_R_nose_pokes = 0
    num_L_lever_preses = 0
    num_R_lever_preses = 0

    num_eaten = 0
    NOSE_POKED_L = False
    NOSE_POKED_R = False
    LEVER_PRESSED_L = False
    LEVER_PRESSED_R = False
    ACTION_TAKEN = False
    SHOCK_ON = False
    CAMERA_ON = False
    RECORDING = False

    events.append(("StartTime: " + str(START_TIME)))

    PREVIOUSLY_FROZEN = False #Used to prevent 'unfrozen' from being logged prior to first 'frozen' event
    FROZEN_ALREADY_LOGGED = False #Used for "DEBOUNCING" Frozen msg from video
    UNFROZEN_ALREADY_LOGGED = False #Used for "DEBOUNCING" Frozen msg from video
    cur_time =  time.perf_counter()

    START_EXPT = False
    PAUSE_STARTED = False

    Protocol_ln_num = 0
    loop = 0
    Protocol_loops = 0
    LOOP_FIRST_PASS = True
    CONDITONS_NOT_SET = True
    CONDITION_STARTED = False
    RUN_SETUP = False
    VI_index = 0

    
    Expt_Count = 0

    TOUCH_IMAGES_SENT = False

    # Open ephys stuff
    snd = zmqClasses.SNDEvent(5556, recordingDir = 'C:\\Users\\Ephys\\Desktop\\RecDir', prependText = 'CHANGE ME') # subject number or something

    openEphysBack_q = Queue()
    # Start thread
    open_ephys_rcv = threading.Thread(target=eventRECV.rcv, args=(openEphysBack_q,), kwargs={'flags' : [b'event']})
    open_ephys_rcv.start()

    ################################################################################
    #  MAIN LOOP
    ################################################################################
    while True: # main game loop
        cur_time =  time.perf_counter()

        if not back_q.empty():
            backDict = back_q.get()
            if backDict['FROZEN']: # FROZEN
                  # NOTE: this must be "debounced"
                  if not FROZEN_ALREADY_LOGGED:
                      print("LOGGING FROZEN")
                      log_event(events,"Frozen",cur_time,("Orig_NIDAQ_t",backDict['NIDAQ_time'],"video_time",backDict['vid_time'],"time_diff",backDict['Vid-NIDAQ']))
                      FROZEN_ALREADY_LOGGED = True
                      UNFROZEN_ALREADY_LOGGED = False

            else:  # UN FROZEN
                if PREVIOUSLY_FROZEN:
                   # NOTE: this must be "debounced"
                   if not UNFROZEN_ALREADY_LOGGED:
                        log_event(events,"Unfrozen",cur_time)
                        FROZEN_ALREADY_LOGGED = False
                        UNFROZEN_ALREADY_LOGGED = True

            #print('problem with back_queue')
        if not openEphysBack_q.empty():
            OEMsg = openEphysBack_q.get()
            print(OEMsg)
        #######################
        # DRAW SCREEN AND GUI ELEMENTS
        #######################
        myscreen.fill((Background_color))
        myscreen.blit(TNElogo,(380,5))
        for button in buttons:
            button.draw()

        for box in boxes: # Must draw before items that go on top
            box.draw()


        for lever in levers:
            #lever.state = "IN"
            # Delay displaying lever state for visual purposes only (NOTE: PROGRAM IS NOT PAUSED!)
            if lever.index == 0: # LEFT LEVER
               if  lever.STATE == "OUT":
                   if LEVER_PRESSED_L:
                      if (cur_time - LEVER_PRESS_TIME) > 0.5: #Leaves on for 0.5 sec
                         lever.STATE = "OUT"
                         LEVER_PRESSED_L = False
                      else:
                         lever.STATE = "DN"
               # else lever.state == "IN" or "DN"

            if lever.index == 1: # RIGHT LEVER
               if  lever.STATE == "OUT":
                   if LEVER_PRESSED_R:
                      if (cur_time - LEVER_PRESS_TIME) > 0.5: #Leaves on for 0.5 sec
                         lever.STATE= "OUT"
                         LEVER_PRESSED_R = False
                      else:
                         lever.STATE = "DN"
               # else lever.state == "IN" or "DN"

            lever.draw()

        for LED in LEDs:
            # Leaves nose poke LED ON for 1 sec so user can see it (NOTE: PROGRAM IS NOT PAUSED!)
            if LED.index == 2: #Left NOSE POKE
               if NOSE_POKED_L:
                   if (cur_time - NOSE_POKE_TIME) > 0.25: #Leaves on for 0.25 sec
                         LED.ONOFF = "OFF"  # NOW OFF
                         NOSE_POKED_L = False
                   else:
                         LED.ONOFF = "ON"

            elif LED.index == 3: #Right NOSE POKE
                if NOSE_POKED_R:
                   if (cur_time - NOSE_POKE_TIME) > 1.0:
                         LED.ONOFF = "OFF"  # NOW OFF
                         NOSE_POKED_R = False
                   else:
                         LED.ONOFF = "ON"

            LED.draw()

        for tog in toggles:
            tog.draw()

        for sld in sliders:
            sld.draw()

        for lbl in labels: # Last so on top
            lbl.draw()

        for info in info_boxes: # Last so on top
            if info.label == "L NOSE POKES":
                  info.text = [str(num_L_nose_pokes)]
            elif info.label == "R NOSE POKES":
                  info.text = [str(num_R_nose_pokes)]
            elif info.label == "L PRESSES":
                  info.text = [str(num_L_lever_preses)]
            elif info.label == "R PRESSES":
                  info.text = [str(num_R_lever_preses) ]
            elif info.label == "PELLETS":
                  info.text = [str(num_pellets)]
            elif info.label == "EATEN":
                  info.text = [str(num_eaten)]
            elif info.label == "DATE":
                  info.text = [str(date)]
            elif info.label == "EVENT LOG":
                  lines_in_txt = len(events)
                  if lines_in_txt > 14:
                      info.text = events[-14:]
                  else: info.text = events

            info.draw()

        # USER INPUTS
        for user_input in user_inputs:
            if user_input.label == "EXPT":
                 user_input.text = str(Expt_Name)
            elif user_input.label == "SUBJECT":
                 user_input.text = str(Subject)
            elif user_input.label == "TRIAL":
                 user_input.text  = str(trial_num)
            elif user_input.label == "EXPT PATH":
                 user_input.text = str(datapath)
            elif user_input.label == "EXPT FILE NAME":
                 user_input.text = str(expt_file_name)
            elif user_input.label == "Spk(S)":
                 user_input.text  = str(Tone1_Duration)
            elif user_input.label == "Freq(Hz)":
                 user_input.text  = str(Tone1_Freq)
            elif user_input.label == "Vol(0-1)":
                 user_input.text  = str(Tone1_Vol)
            elif user_input.label == "Shck(S)":
                 user_input.text = str(Shock_Duration)
            elif user_input.label == "V":
                 user_input.text = str(Shock_V)
            elif user_input.label == "Amps":
                 user_input.text = str(Shock_Amp)

            user_input.draw()


        # DRAW SPEEKER
        speeker = draw_speeker(myscreen,230,85,TONE_ON) #TONE_ON is T/F

        if TONE_ON:
              if (cur_time - TONE_TIME) > float(Tone1_Duration): # seconds
                  print("TONE OFF")
                  TONE_ON = False
                  log_event(events,"Tone_OFF",cur_time)

        # DRAW LIGHTNING SHOCK
        shock = draw_lighting(myscreen, SHOCK_ON, 228,150,1,(255,255,0),2) #--> returns a Rect Object used for mouse click
        if SHOCK_ON:
              if (cur_time - SHOCK_TIME) <= Shock_Duration: # seconds
                  apply_shock.sendDBit(True) # NOTE: THIS IS DONE ON MOUSE CLICK OR IN PROTOCOL OR CONDITION
                  #Event Logged at mouse Click event
                  pass
              else:
                  SHOCK_ON = False
                  apply_shock.sendDBit(False)
                  print("SHOCK OFF")
                  log_event(events,"Shock_OFF",cur_time) # Also logged when user turns off in mouse press event
        else: apply_shock.sendDBit(False) # SHOCK OFF


        
        # DRAW CAMERA
        # draw_camera(myscreen,fill_color, ON_OFF, REC, x, y, w,h, linew)
        camera = draw_camera(myscreen, (100,100,100),CAMERA_ON,RECORDING,215, 255, 30,20, 2)

        #########################################################
        #  SYSTEM EVENTS
        #########################################################
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            ########################################
            #  Keyboard Events
            ########################################

            #########################################################
            #  MOUSE EVENTS (always active independent of game mode)
            #########################################################
            # MOUSE MOVE
            elif (event.type == pygame.MOUSEMOTION):#
                cur_x,cur_y = pygame.mouse.get_pos()
                if SLIDER_SELECTED:
                    cur_slider.sliderX = cur_x
                    # The following limits the slider to the slot.
                    if cur_slider.sliderX < cur_slider.x:
                        cur_slider.sliderX = cur_slider.x
                    if cur_slider.sliderX > cur_slider.x + cur_slider.slotL:
                        cur_slider.sliderX = cur_slider.x + cur_slider.slotL
                    cur_slider.percent = cur_slider.x / cur_slider.slotL
            # ----------------------------------------
            # MOUSE DOWN
            elif (event.type == pygame.MOUSEBUTTONDOWN ):#Mouse Clicked
                cur_x,cur_y = pygame.mouse.get_pos()
                if event.button == 1:
                    LEFT_MOUSE_DOWN = True
                elif event.button == 3:
                    RIGHT_MOUSE_DOWN = True
                # BUTTONS
                if LEFT_MOUSE_DOWN:
                    print("MOUSE_Button ",event.button, "pressed!")
                    cur_time = time.perf_counter()
                    # BUTTONS
                    for button in buttons: # Check for collision with EXISTING buttons
                        if button.rect.collidepoint(cur_x,cur_y):
                               button.UP_DN = "DN"
                               #button.draw()
                               if button.text == "CABIN LT":
                                   if CAB_LIGHT_ON: #Toggle OFF
                                       Background_color = CAB_LIGHT(events,False,cur_time)
                                       CAB_LIGHT_ON = False
                                   else: # Toggle ON
                                       Background_color = CAB_LIGHT(events,True,cur_time)
                                       CAB_LIGHT_ON = True
                               if button.text == "FAN": #TOGGLE ON TOGGLE OFF
                                    if FAN_0N:
                                       FAN_0N = False
                                       FAN_ON_OFF(events,FAN_0N,cur_time)

                                    else:
                                       FAN_0N = True
                                       FAN_ON_OFF(events,FAN_0N,cur_time)

                               elif button.text == "FEED":
                                    button.UP_DN = "DN"
                                    FEED = True
                                    FOOD_REWARD(events,"Food_Pellet",cur_time)

                               # LEFT LEVER
                               elif button.text == "L":
                                    if L_LEVER_EXTENDED: # Was EXTENDED
                                          button.UP_DN = "UP"
                                          EXTEND_LEVERS(events,"L_Lever_Retracted",False,False,cur_time)
                                          levers[0].STATE = "IN"

                                    else: # Was not extended
                                          button.UP_DN = "DN"
                                          EXTEND_LEVERS(events,"L_Lever_Extended",True,False,cur_time)
                                          levers[0].STATE = "OUT"

                               # RIGHT LEVER
                               elif button.text == "R":
                                    if R_LEVER_EXTENDED: # Was EXTENDED
                                          button.UP_DN = "UP"
                                          EXTEND_LEVERS(events,"R_Lever_Retracted",False,False,cur_time)
                                          levers[1].STATE = "IN"

                                    else: # was not extended
                                          button.UP_DN = "DN"
                                          EXTEND_LEVERS(events,"R_Lever_Extended",False,True,cur_time)
                                          levers[1].STATE = "OUT"

                               # BOTH LEVERS AT ONCE
                               elif button.text == "EXTEND" or button.text == "RETRACT":
                                    if LEVERS_EXTENDED: #Toggle EXTEND and RETRACT
                                          button.UP_DN = "UP"
                                          #LEVERS_EXTENDED = False
                                          EXTEND_LEVERS(events,"Levers_Retracted",False,False,cur_time)
                                          button.text = "EXTEND"
                                          for lever in levers:
                                                lever.STATE = "IN"

                                    else: # not extended
                                          button.UP_DN = "DN"
                                          button.text = "RETRACT"
                                          #LEVERS_EXTENDED = True
                                          EXTEND_LEVERS(events,"Levers_Extended",True,True,cur_time)
                                          for lever in levers:
                                                lever.STATE = "OUT"

                               elif button.text == "REC":
                                    if CAMERA_ON:
                                          if RECORDING: #STOP RECORDING BUT KEEP CAMERA ON
                                                RECORDING = False
                                                log_event(events,"STOP RECORDING",cur_time)
                                                vidDict = {'cur_time':cur_time, 'STATE':'ON', 'PATH_FILE':video_file_path_name}
                                                button.UP_DN = "UP"
                                          else:
                                                RECORDING = True
                                                button.UP_DN = "DN"
                                                log_event(events,"START RECORDING",cur_time)
                                                vidDict = {'cur_time':cur_time, 'STATE':'REC', 'PATH_FILE':video_file_path_name}


                                    else:
                                          print("CAMERA NOT ON!")

                               # LOAD EXPT FILE AND RUN SETUP
                               elif button.text == "LOAD FILE":
                                    button.UP_DN = "DN"
                                    print( expt_file_path_name)
                                    if load_expt_file(expt_file_path_name):
                                        EXPT_FILE_LOADED = True
                                        log_event(events,"EXPT FILE LOADED",cur_time)
                                        RUN_SETUP = True
                                        setup_ln_num = 0
                                        
                                    else:
                                        print("HUMPH!")
                                        log_event(events,"Expt File name or path DOES NOT EXIST",cur_time)
                                        
                                        
                                        
                               elif button.text == "START EXPT":
                                    print("EXPT STARTED!")
                                    button.UP_DN = "DN"
                                    Expt_Count +=1
                                    if EXPT_FILE_LOADED:
                                        trial_num = 0
                                        if TOUCHSCREEN_USED: StartTouchScreen()
                                        for user_input in user_inputs:
                                            if user_input.label == "EXPT":
                                                user_input.text = str(Expt_Name)+str(Expt_Count)

                                        ############################################################################
                                        if  BAR_PRESS_INDEPENDENT_PROTOCOL:
                                        # NOTE: THIS IS USED IF REWARDING FOR BAR PRESS (AFTER VI) IS THE ONLY CONDITION (HABITUATION AND CONDITIONING ARE RUNNING CONCURRENTLY)
                                            VI_start = cur_time
                                            VI = random.randint(0,int(var_interval_reward*2))
                                            print("VI.......................", VI)
                                        ###############################################################################
                                        # RUN EXPERIMENT CONDITIONS DESCRIBED IN EXPT FILE
                                        log_event(events,"EXPT STARTED",cur_time)
                                        START_EXPT = True

                                    else:
                                        log_event(events,"EXPT FILE NOT LOADED!!!!",cur_time)

                                    
                               LEFT_MOUSE_DOWN = False
                               BUTTON_SELECTED = True
                               dx = cur_x - button.x
                               dy = cur_y - button.y

                    # LEVERS
                    for lever in levers:
                        if lever.rect.collidepoint(cur_x,cur_y): # Check for collision with EXISTING levers
                            #LEVER_PRESS_TIME = time.perf_counter()
                            if lever.text == "L LEVER":
                                if L_LEVER_EXTENDED:
                                      lever.STATE = "DN"
                                      #NOTE: Lever presses are not logged here, but when actually pressed in Behavioral Chamber


                            if lever.text == "R LEVER":
                                if R_LEVER_EXTENDED:
                                      lever.STATE = "DN"
                                      #NOTE: Lever presses are not logged here, but when actually pressed in Behavioral Chamber

                            # NOTE:  We are redrawing here again (instead of just in main loop)
                            #       because state will be reset ot actual machine state (which is what
                            #       really matters.  I you don't care about this, comment out next 3 lines.
                            lever.draw()
                            pygame.display.flip()
                            time.sleep(0.5) # sec
                            lever.STATE = "OUT"

                    # LEDS
                    for LED in LEDs: # Check for collision with EXISTING buttons
                        if LED.rect.collidepoint(cur_x,cur_y):
                            idx = LEDs.index(LED)
                            print ("LED ID: ",idx)
                            if LED.ONOFF == "OFF": # WAS OFF
                                LED.ONOFF = "ON"   # NOW ON
                                if   LED.index == 0: # LEFT CONDITION LIGHT
                                    L_CONDITIONING_LIGHT(events,True,cur_time)
                                elif LED.index == 1: # RIGHT CONDITION LIGHT
                                    R_CONDITIONING_LIGHT(events,True,cur_time)

                                # NOSE POKES
                                elif LED.index == 2 or LED.index == 3: # NOSE POKES
                                   NOSE_POKE_TIME = time.perf_counter()
                                   # NOTE:  We are redrawing here again (instead of just in main loop)
                                   #       because state will be reset ot actual machine state (which is what
                                   #       really matters.  I you don't care about this, comment out next 3 lines.
                                   LED.draw()
                                   pygame.display.flip()
                                   time.sleep(0.25) # sec

                                # FEEDER LEDS
                                elif LED.index == 4 or LED.index == 5: # FEEDER LIGHTS
                                    box.fill_color,LEDsONOFF = Food_Light_ONOFF (events,True,cur_time)
                                    LEDs[4].ONOFF = LEDsONOFF
                                    LEDs[5].ONOFF = LEDsONOFF

                            else:                  # WAS ON
                                LED.ONOFF = "OFF"  # NOW OFF
                                LED.draw()
                                if   LED.index == 0: # LEFT CONDITION LIGHT
                                    L_CONDITIONING_LIGHT(events,False,cur_time)
                                elif LED.index == 1: # RIGHT CONDITION LIGHT
                                    R_CONDITIONING_LIGHT(events,False,cur_time)

                                # FEEDER LEDS
                                elif LED.index == 4 or LED.index == 5: # FEEDER LIGHTS
                                    box.fill_color,LEDsONOFF = Food_Light_ONOFF (events,False,cur_time)
                                    LEDs[4].ONOFF = LEDsONOFF
                                    LEDs[5].ONOFF = LEDsONOFF


                    # FEEDER BOXES
                    for box in boxes: # Check for collision with EXISTING buttons
                        if box.rect.collidepoint(cur_x,cur_y):
                           if FEEDER_LT_ON: #Toggle OFF
                              box.fill_color,LEDsONOFF = Food_Light_ONOFF (events,False,cur_time)
                              LEDs[4].ONOFF = LEDsONOFF
                              LEDs[5].ONOFF = LEDsONOFF
                           else: # Toggle ON
                              box.fill_color,LEDsONOFF = Food_Light_ONOFF (events,True,cur_time)
                              FEEDER_LT_ON = True

                    # SPEEKER PRESSED
                    if speeker.collidepoint(cur_x,cur_y):
                          # NOTE: Tone_OFF logged while drawing speeker above in main loop
                          PLAY_TONE(events,"TONE1",cur_time)


                    # SHOCK PRESSED (TOGGLE)
                    if shock.collidepoint(cur_x,cur_y):
                          SHOCK_TIME = cur_time
                          if SHOCK_ON:
                                SHOCK_ON = False
                                log_event(events,"Shock_OFF",cur_time)
                                # NOTE: SHOCK ALSO TURNED OFF IN GAME LOOP AFTER Shock_Duration (s)
                          else:
                                SHOCK_ON = True
                                print("SHOCKING!!!")
                                log_event(events,"Shock_ON",cur_time,("Voltage", str(Shock_V),"Amps",str(Shock_Amp),"Duration(S)",str(Shock_Duration)))
                                # NOTE: SHOCK TURNED OFF IN GAME LOOP AFTER Shock_Duration (s)

                          print("SHOCK PRESSED")

                    # CAMERA PRESSED
                    if camera.collidepoint(cur_x,cur_y):
                          if CAMERA_ON: #CAMERAL ALREWADY ON, TURN CAMERA OFF
                                CAMERA_ON = False
                                RECORDING = False
                                log_event(events,"Camera_OFF",cur_time)
                                print("CAMERA OFF")
                                vidDict = {'cur_time':cur_time, 'STATE':'STOP', 'PATH_FILE':video_file_path_name}

                          else: #TURN CAMERA ON
                                CAMERA_ON = True
                                log_event(events,"Camera_ON",cur_time)
                                print("CAMERA ON")
                                vidDict = {'cur_time':cur_time, 'STATE':'ON', 'PATH_FILE':video_file_path_name}
                                MyVideo()


##                    # TOGGLE BUTTONS

##                    for tog in toggles: # Check for collision with toggles
##                        if tog.rect.collidepoint(cur_x,cur_y):
##                            idx = toggles.index(tog)
##
##                            if tog.LEFT_RIGHT == "LEFT":    # WAS INPUT
##                               tog.LEFT_RIGHT = "RIGHT"     # NOW OUTPUT
##                               tog.draw()
##
##                            elif tog.LEFT_RIGHT == "RIGHT": # WAS OUTPUT
##                               tog.LEFT_RIGHT = "LEFT"      # NOW INPUT
##                               tog.draw()
##
##                    # SLIDERS
##                    for sld in sliders: # Check for collision with SLIDERS
##                        if sld.rect.collidepoint(cur_x,cur_y):
##                            SLIDER_SELECTED = True
##                            cur_slider = sld

                    # USER KEYBOARD INPUTS
                    for user_input in user_inputs:
                        if user_input.rect.collidepoint(cur_x,cur_y):
                            user_input.get_key_input()
                            if user_input.label == "EXPT":
                                 Expt_Name=user_input.text
                            elif user_input.label == "SUBJECT":
                                 Subject = user_input.text
                            elif user_input.label == "TRIAL":
                                 trial_num =  user_input.text
                            elif user_input.label == "EXPT PATH":
                                 datapath = user_input.text
                            elif user_input.label == "EXPT FILE NAME":
                                 expt_file_name = user_input.text
                                 expt_file_path_name = os.path.join(datapath,expt_file_name )

                            elif user_input.label == "Spk(S)":
                                 Tone1_Duration = float(user_input.text)
                            elif user_input.label == "Freq(Hz)":
                                 Tone1_Freq = float(user_input.text)
                            elif user_input.label == "Vol(0-1)":
                                 Tone1_Vol = float(user_input.text)

                            elif user_input.label == "Shck(S)":
                                 Shock_Duration = float(user_input.text)
                            elif user_input.label == "V":
                                 Shock_V = float(user_input.text)
                            elif "Amps" in user_input.label: # == "Amps":
                                 Shock_Amp = float(user_input.text)


           # MOUSE UP
            elif (event.type == pygame.MOUSEBUTTONUP ):
                NEW_BUTTON = False
                LEFT_MOUSE_DOWN = False
                RIGHT_MOUSE_DOWN = False
                BUTTON_SELECTED = False
                LBL_SELECTED = False
                LED_SELECTED = False
                BOX_SELECTED = False
                CORNER_SET = False
                DELETE_ITEM = False
                CIRC_SELECTED = False
                SLIDER_SELECTED = False

                for button in buttons: # Check for collision with EXISTING buttons
                    if button.text == "REC":  # Leave REC button down while recording
                        if not RECORDING: button.UP_DN = "UP"

                    elif button.text == "R":  # Leave R button down while recording
                        if not R_LEVER_EXTENDED: button.UP_DN = "UP"
                    elif button.text == "L":  # Leave R button down while recording
                        if not L_LEVER_EXTENDED: button.UP_DN = "UP"

                    else: # ALL OTHER BUTTONS, NOT REC BUTTON
                        button.UP_DN = "UP"


        ######################################
        #   CHECK INPUTS FROM BEH CHAMBER
        ######################################
        if NIDAQ_AVAILABLE:
            #print("NIDAQ_AVAILABLE = ",NIDAQ_AVAILABLE)
            # levers
            if L_LEVER_EXTENDED or R_LEVER_EXTENDED:
                  wasleverPressed = detectPress(checkPressLeft,checkPressRight)
                  cur_time = time.perf_counter()
                  LEVER_PRESS_TIME = cur_time
                  if  wasleverPressed == 'Right':
                        log_event(events,"Lever_Pressed_R",cur_time)
                        lever.PRESSED = True
                        LEVER_PRESSED_R = True
                        print("RIGHT LEVER PRESSED")
                        num_R_lever_preses += 1
                        levers[1].STATE = "DN"
                  #else: levers[1].STATE = "OUT"

                  if  wasleverPressed == 'Left':
                        log_event(events,"Lever_Pressed_L",cur_time)
                        lever.PRESSED = True
                        LEVER_PRESSED_L = True
                        print("LEFT LEVER PRESSED")
                        num_L_lever_preses += 1
                        levers[0].STATE = "DN"
                  #else: levers[0].STATE = "OUT"

            # nose pokes
            cur_time = time.perf_counter()
            was_nose_poked_L = checkLeftNosePoke(L_nose_poke)

            if was_nose_poked_L:
                print("LEFT Nose Poked")
                NOSE_POKE_TIME = cur_time
                #events.append("LEFT Nose Poke: " + str(cur_time))
                log_event(events,"Nose_Poke_L",cur_time)
                NOSE_POKED_L = True
                num_L_nose_pokes += 1
                for LED in LEDs:
                    if LED.index == 2: # R NOSE POKES
                          LED.ONOFF = "ON"
            else:
                for LED in LEDs:
                    if LED.index == 2: # R NOSE POKES
                          LED.ONOFF = "OFF"

            was_nose_poked_R = checkRightNosePoke(R_nose_poke)
            if was_nose_poked_R:
                print("Right Nose Poked")
                #events.append("RIGHT Nose Poke: " + str(cur_time))
                log_event(events,"Nose_Poke_R",cur_time)
                NOSE_POKE_TIME = time.perf_counter()
                NOSE_POKED_R = True
                num_R_nose_pokes += 1
                for LED in LEDs:
                    if LED.index == 3: # R NOSE POKES
                      LED.ONOFF = "ON"
            else:
                for LED in LEDs:
                    if LED.index == 3: # R NOSE POKES
                          LED.ONOFF = "OFF"

            # food eaten
            cur_time = time.perf_counter()
            foodEaten = checkFoodEaten(eaten)

            if foodEaten:
                print("Yum!")
                num_eaten +=1
                #events.append("Food Eaten: " + str(cur_time))
                log_event(events,"Food_Eaten",cur_time)

        ######################################
        #   UPDATE SCREEN
        ######################################
        pygame.display.flip()

        ######################################
        #   UPDATE VIDEO
        ######################################
        vidDict['cur_time'] = cur_time
        q.append(vidDict)


########################################################################################################################
        ################################################################
        # SETUP EXPERIMENTAL WHEN START EXPT BUTTON PRESSED
        ################################################################
        if RUN_SETUP:
            print("SETUPDICT:....................",setup,"length: ",len(setup),"linenum: ",setup_ln_num)
            setupDict = setup[setup_ln_num]
            key = list(setupDict.keys())[0] # First key in protocolDict
            print ("KEY:.....................",key)
            if key == "":
                setup_ln_num +=1
            elif key == "FAN_ON":
               val = str2bool(setupDict[key])
               print("FAN")
               FAN_ON_OFF(events,val,cur_time) # {'FAN_ON': True} or {'FAN_ON': False}
               setup_ln_num +=1

            elif key == "CAB_LIGHT":
               val = str2bool(setupDict[key])
               print("CAB_LIGHT")
               Background_color = CAB_LIGHT(events,val,cur_time)
               #CAB_LIGHT(events,val,cur_time)
               setup_ln_num +=1

            elif key == "FOOD_LIGHT":
                print("FOOD LIGHT: ",setupDict["FOOD_LIGHT"])
                val = str2bool(setupDict[key])
                setup_ln_num +=1
                box.fill_color,LEDsONOFF = Food_Light_ONOFF (events,val,cur_time)
                LEDs[4].ONOFF = LEDsONOFF
                LEDs[5].ONOFF = LEDsONOFF

            elif key == "CAMERA":
                print("CAMERA")
                val = str2bool(setupDict[key])
                setup_ln_num +=1
                if val:  # TURN CAMERA ON
                    if not CAMERA_ON: # CAMERA WAS OFF
                        CAMERA_ON = True
                        log_event(events,"Camera_ON",cur_time)
                        vidDict = {'cur_time':cur_time, 'STATE':'ON', 'PATH_FILE':video_file_path_name}
                        MyVideo()
                    else: # CAMERA IS ALREADY ON
                        log_event(events,"Camera is ALREADY ON",cur_time)
                else: # TURN CAMERA OFF
                    if CAMERA_ON: # CAMERA CURRENTLY ON
                        CAMERA_ON = False
                        RECORDING = False
                        log_event(events,"Camera_OFF",cur_time)
                        vidDict = {'cur_time':cur_time, 'STATE':'STOP', 'PATH_FILE':video_file_path_name}


            elif key == "REC":
                print ("recording")
                val = str2bool(setupDict[key])
                setup_ln_num +=1
                if val:  # REC == TRUE.  Remember Camera STATE = (ON,OFF,REC)
                    vidDict = {'cur_time':cur_time, 'STATE':'REC', 'PATH_FILE':video_file_path_name}
                else:
                    vidDict = {'cur_time':cur_time, 'STATE':'ON', 'PATH_FILE':video_file_path_name}

            if setup_ln_num >= len(setup):
                RUN_SETUP = False


        ################################################################
        # RUN EXPERIMENTAL PROTOCOL IF START EXPT BUTTON PRESSED
        ################################################################

        if START_EXPT:

            protocolDict = protocol[Protocol_ln_num]
            key = list(protocolDict.keys())[0] # First key in protocolDict

            # Tell open ephys to start acquisiton and recording?
            #snd.send(snd.START_ACQ)
            #snd.send(snd.START_REC)


            if key == "":
                Protocol_ln_num +=1
            elif key == "FAN_ON":
               val = str2bool(protocolDict[key])
               print("FAN")
               FAN_ON_OFF(events,val,cur_time) # {'FAN_ON': True} or {'FAN_ON': False}
               Protocol_ln_num +=1

            elif key == "CAB_LIGHT":
               val = str2bool(protocolDict[key])
               print("CAB_LIGHT")
               Background_color = CAB_LIGHT(events,val,cur_time)
               #CAB_LIGHT(events,val,cur_time)
               Protocol_ln_num +=1

            elif "TONE" in key:
                Protocol_ln_num +=1
                idx = key[4:]
                print("TONE idx: ",idx)
                if idx == '1':
                     PLAY_TONE(events,"TONE1",cur_time)
                     TONE_TIME = cur_time
                elif idx == '2':
                     PLAY_TONE(events,"TONE2",cur_time)
                     TONE_TIME = cur_time
                TONE_ON = True

            elif key == "FOOD_LIGHT":
                print("FOOD LIGHT: ",protocolDict["FOOD_LIGHT"])
                val = str2bool(protocolDict[key])
                Protocol_ln_num +=1
                box.fill_color,LEDsONOFF = Food_Light_ONOFF (events,val,cur_time)
                LEDs[4].ONOFF = LEDsONOFF
                LEDs[5].ONOFF = LEDsONOFF

            elif key  == 'SHOCK':
                 log_event(events,"Shock_ON",cur_time,("Voltage", str(Shock_V),"Amps",str(Shock_Amp),"Duration(S)",str(Shock_Duration)))
                 SHOCK_ON = True


            elif key == "L_CONDITIONING_LIGHT":
                val = str2bool(protocolDict[key])
                Protocol_ln_num +=1
                if val:
                    L_CONDITIONING_LIGHT(events,True,cur_time)
                    LEDs[0].ONOFF = "ON"
                else:
                    L_CONDITIONING_LIGHT(events,False,cur_time)
                    LEDs[0].ONOFF = "OFF"

            elif key == "R_CONDITIONING_LIGHT":
                val = str2bool(protocolDict[key])
                Protocol_ln_num +=1

                if val:
                    R_CONDITIONING_LIGHT(events,True,cur_time)
                    LEDs[1].ONOFF = "ON"
                else:
                    R_CONDITIONING_LIGHT(events,False,cur_time)
                    LEDs[1].ONOFF = "OFF"

            elif key == "CAMERA":
                print("CAMERA")
                val = str2bool(protocolDict[key])
                Protocol_ln_num +=1
                if val:  # TURN CAMERA ON
                    if not CAMERA_ON: # CAMERA WAS OFF
                        CAMERA_ON = True
                        log_event(events,"Camera_ON",cur_time)
                        vidDict = {'cur_time':cur_time, 'STATE':'ON', 'PATH_FILE':video_file_path_name}
                        MyVideo()
                    else: # CAMERA IS ALREADY ON
                        log_event(events,"Camera is ALREADY ON",cur_time)
                else: # TURN CAMERA OFF
                    if CAMERA_ON: # CAMERA CURRENTLY ON
                        CAMERA_ON = False
                        RECORDING = False
                        log_event(events,"Camera_OFF",cur_time)
                        vidDict = {'cur_time':cur_time, 'STATE':'STOP', 'PATH_FILE':video_file_path_name}


            elif key == "REC":
                print ("recording")
                val = str2bool(protocolDict[key])
                Protocol_ln_num +=1
                if val:  # REC == TRUE.  Remember Camera STATE = (ON,OFF,REC)
                    vidDict = {'cur_time':cur_time, 'STATE':'REC', 'PATH_FILE':video_file_path_name}
                else:
                    vidDict = {'cur_time':cur_time, 'STATE':'ON', 'PATH_FILE':video_file_path_name}

            elif "EXTEND_LEVERS" in key:
                if protocolDict[key] == "L_LVR":
                   EXTEND_LEVERS(events,"Levers Extended",True,False,cur_time)
                elif protocolDict[key] == "R_LVR":
                   EXTEND_LEVERS(events,"Levers Extended",False,True,cur_time)
                else:
                    val = str2bool(protocolDict[key])
                    Protocol_ln_num +=1
                    if val: # EXTEND_LEVERS == True
                       print ("EXTEND LEVERS")
                       EXTEND_LEVERS(events,"Levers Extended",True,True,cur_time)
                       for lever in levers:
                             lever.STATE = "OUT"

                       for button in buttons:
                            if button.text == "EXTEND": button.text = "RETRACT"


                    else: # RETRACT LEVERS (EXTEND_LEVERS == False)
                       print ("RETRACT LEVERS")
                       EXTEND_LEVERS(events,"Levers_Retracted",False,False,cur_time)
                       for lever in levers:
                            lever.STATE = "IN"
                       for button in buttons:
                            if button.text == "RETRACT": button.text = "EXTEND"
            elif "DRAW_IMAGES" in key:
                if TOUCHSCREEN_USED:
                    print("\n\nSENDING MSG TO WHISPER TOUCH ZMQ: ")
                    print("TOUCH IMG FILES: ",touch_img_files)
                    print(type(touch_img_files))
                    #pair_client(touch_img_files,socket)
                    TSq.put(touch_img_files)
                    #print("WHISKER MSG",whisker_msg )
                    #socket.send_string("%s %s" % (topic,json_string))
                    #print(" MSG SENT from GUI ")
                    Protocol_ln_num +=1




            elif "START_LOOP" in key:
                print("\n.............TRIAL = ",trial_num, "LOOP: ", loop,"..................")
                loop +=1
                
                trial_num +=1
                for user_input in user_inputs:
                    if user_input.label == "TRIAL":
                            user_input.text = str(trial_num)


                CONDITONS_NOT_SET = True

                loop_start_line_num = Protocol_ln_num
                print("XXXXXXXX POTOCOL LINE NUM: ",Protocol_ln_num, protocolDict[key])
                Protocol_ln_num +=1
                if "RANDOM" in protocolDict[key]:
                    if LOOP_FIRST_PASS:
                        intrange = protocolDict[key][7:len(protocolDict[key])-1]
                        print("intrange: ", intrange)
                        a,b = intrange.split(",")
                        print("a,b: ", a,b)
                        NUM_LOOPS = random.randint(int(a), int(b))
                        LOOP_FIRST_PASS = False
                else:
                    print ('NUM_LOOPS:..............................................',protocolDict[key])
                    NUM_LOOPS = int(protocolDict[key])
                log_event(events,"LOOPING "+ str(NUM_LOOPS)+ " times, TRIAL "+str(trial_num),cur_time)

            elif "END_LOOP" in key:
                VI_index = 0
                num_lines_in_loop = Protocol_ln_num - loop_start_line_num
                if loop  < int(NUM_LOOPS):
                    Protocol_ln_num = Protocol_ln_num - num_lines_in_loop
                else:
                    Protocol_ln_num +=1
                    log_event(events,"END_OF_LOOP",cur_time)
                    loop = 0
                    LOOP_FIRST_PASS = True
                #trial = 0 Do not set here in case there are more than 1 loops
                    
############################################################################################
            elif key == "PAUSE":
                try: # WAS A NUMBER
                    PAUSE_TIME = float(protocolDict["PAUSE"])
                except: # NOT A NUMBER. MUST BE VI_TIMES
                    #print(protocolDict["PAUSE"])
                    #print(habituation_vi_times)
                    if "HABITUATION" in protocolDict["PAUSE"]:
                        PAUSE_TIME = habituation_vi_times[VI_index]
                    if "CONDITIONING" in protocolDict["PAUSE"]:
                        PAUSE_TIME = conditioning_vi_times[VI_index]
                #print("PAUSE_TIME:.....................................",PAUSE_TIME)        
                if not PAUSE_STARTED:
                    log_event(events,"PAUSEING FOR "+str(PAUSE_TIME)+" sec",cur_time)
                    PAUSE_STARTED = True
                    pause_start_time = cur_time
                else: #PAUSE_STARTED
                    time_elapsed = cur_time - pause_start_time
                    if time_elapsed >= PAUSE_TIME:
                        VI_index +=1
                        Protocol_ln_num +=1 #Go to next protocol item
                        PAUSE_STARTED = False
                
##############################################################################################


            elif key == "CONDITIONS":
                 num_conditions = len(conditions)
                 if protocolDict["CONDITIONS"] == "RANDOM": #Or SEQUENTIAL or a particular condition number
                     choose_cond = random.randint(0,num_conditions-1)
                 elif  protocolDict["CONDITIONS"] == "SEQUENTIAL":
                     condition_idx += 1
                     choose_cond = condition_idx
                 else: # a particual sequence number
                     cond_num = int(protocolDict["CONDITIONS"])
                     choose_cond = cond_num


                 ###############################
                 # SET CONDITONS HERE
                 ###############################
                 if CONDITONS_NOT_SET:
                     HAS_ALREADY_RESPONDED = False
                     CONDITONS_NOT_SET = False
                     cond = conditions[choose_cond]
                     log_event(events,"CONDITION["+str(choose_cond)+"]",cur_time)
                     COND_MAX_TIME = float(cond["MAX_TIME"])
                     reset = cond["RESET"]

                     print("\n\nCONDTION")
                     print(cond)
                     #condkey = list(condDict.keys())[0] # First key in condDict


                     # SET CONDITIONS
                     # SET LEVERS WHEN IN CONDITIONS
                     try:
                         if cond['EXTEND_L_LEVER'] and cond['EXTEND_R_LEVER']:
                             EXTEND_LEVERS(events,"Levers Extended",True,True,cur_time)

                         elif cond['EXTEND_L_LEVER']:
                             EXTEND_LEVERS(events,"L Lever Extended",True,False,cur_time)

                         elif cond['EXTEND_R_LEVER']:
                             EXTEND_LEVERS(events,"R Lever Extended",False,True,cur_time)

                         else:
                             EXTEND_LEVERS(events,"Levers Retracted",False,False,cur_time)

                     except:
                         pass
                     # SET CONDITIONING LIGHTS
                     try: # if conditionaing lights are used
                         if cond['L_CONDITION_LT']: # Left_Conditioning lit 1/0
                             L_CONDITIONING_LIGHT(events,True,cur_time)
                             LEDs[0].ONOFF = "ON"
                         else:
                             L_CONDITIONING_LIGHT(events,False,cur_time)
                             LEDs[0].ONOFF = "OFF"


                         if cond['R_CONDITION_LT']: # Left_Conditioning lit 1/0
                             R_CONDITIONING_LIGHT(events,True,cur_time)
                             LEDs[1].ONOFF = "ON"
                         else:
                             R_CONDITIONING_LIGHT(events,False,cur_time)
                             LEDs[1].ONOFF = "OFF"
                     except: # Conditionaing lights not used, Use Touch screen instead
                         pass


                 # Wait for response
                 if not CONDITION_STARTED: #
                    condition_start_time = cur_time
                    CONDITION_STARTED = True
                    TIME_IS_UP = False
                    CORRECT = False
                    WRONG = False
                    NO_ACTION_TAKEN = False

                 else: # CONDITION STARTED
                    cond_time_elapsed = cur_time - condition_start_time

                    if levers[0].PRESSED: # LEFT LEVER
                        log_event(events,"Left_Lever_Pressed",cur_time)
                        levers[0].PRESSED = False
                        if not HAS_ALREADY_RESPONDED:# Prevents rewarding for multiple presses
                            if cond['DES_L_LEVER_PRESS']:
                                log_event(events,"CORRECT Response",cur_time)
                                CORRECT = True
                                if cond["RESET"] == "ON_RESPONSE":
                                   CONDITION_STARTED = False
                            else:
                                WRONG = True
                                log_event(events,"WRONG Response",cur_time)
                            HAS_ALREADY_RESPONDED = True
                            L_CONDITIONING_LIGHT(events,False,cur_time)
                            R_CONDITIONING_LIGHT(events,False,cur_time)
                            LEDs[0].ONOFF = "OFF"
                            LEDs[1].ONOFF = "OFF"

                    if levers[1].PRESSED: # RIGHT LEVER
                        log_event(events,"Right_Lever_Pressed",cur_time)
                        levers[1].PRESSED = False
                        if not HAS_ALREADY_RESPONDED:# Prevents rewarding for multiple presses
                            print("cond['DES_R_LEVER_PRESS']",cond['DES_R_LEVER_PRESS'])
                            if cond['DES_R_LEVER_PRESS']:
                                log_event(events,"CORRECT Response",cur_time)
                                CORRECT = True
                                if cond["RESET"] == "ON_RESPONSE":
                                   CONDITION_STARTED = False
                            else:
                                WRONG = True
                                log_event(events,"WRONG Response",cur_time)
                            HAS_ALREADY_RESPONDED = True
                            LEDs[0].ONOFF = "OFF"
                            LEDs[1].ONOFF = "OFF"
                            L_CONDITIONING_LIGHT(events,False,cur_time)
                            R_CONDITIONING_LIGHT(events,False,cur_time)

                    if TOUCHSCREEN_USED:
                        if not whiskerBack_q.empty():
                            touchMsg = whiskerBack_q.get()
                            log_event(events,touchMsg['picture'] + " Pressed " + str(touchMsg['XY']) , cur_time)
                            if touchMsg['picture'] == 'missed':
                                print('missed')
                            elif not HAS_ALREADY_RESPONDED:
                                HAS_ALREADY_RESPONDED = True
                                for i in range(len(touch_img_files)):
                                    for key in touch_img_files[i].keys():
                                        if key in touchMsg['picture']:
                                            if i == 0 and cond["DES_IMG1_PRESSP"]:
                                                log_event(events,"CORRECT Response",cur_time)
                                                CORRECT = True
                                                break
                                            elif i == 1 and cond["DES_IMG2_PRESSP"]:
                                                log_event(events,"CORRECT Response",cur_time)
                                                CORRECT = True
                                                break
                                            elif not CORRECT:
                                                WRONG = True
                                if WRONG:
                                    log_event(events,"WRONG Response",cur_time)

                    if cond["RESET"] == "FIXED":
                        if cond_time_elapsed >= float(cond["MAX_TIME"]): # Time is up
                           CONDITION_STARTED = False
                           if not WRONG and not CORRECT:
                               NO_ACTION_TAKEN = True
                               log_event(events,"END_OF_TRIAL: NO_ACTION_TAKEN",cur_time)
                           TIME_IS_UP = True

                    if cond["RESET"] == "ON_RESPONSE":
                        #print (cond["Reset"])
                        if WRONG or CORRECT: # A response was given
                            CONDITION_STARTED = False  # Time is up
                            log_event(events,"END_OF_TRIAL",cur_time)
                            TIME_IS_UP = True
                        if cond_time_elapsed >= float(cond["MAX_TIME"]): # Time is up
                           CONDITION_STARTED = False
                           if not WRONG and not CORRECT:
                               NO_ACTION_TAKEN = True
                               log_event(events,"END_OF_TRIAL: NO_ACTION_TAKEN",cur_time)
                           TIME_IS_UP = True

                    if cond["RESET"] == "VI":
                        pass  # TBD

                    if TIME_IS_UP:
                        # SET OUTCOMES
                        if CORRECT:
                           outcome = cond['CORRECT'].upper()  # Outcome for correct response(in Expt File)
                           print("Correct")
                        elif WRONG:
                           outcome = cond['WRONG'].upper()    # Outcome for wrong response(in Expt File)
                           print("Wrong")
                        else:
                           print("No Action Taken")
                           outcome = cond['NO_ACTION'].upper()# Outcome for No_Action taken(in Expt File)

                        # OUTCOMES

                        if 'PELLET' in outcome:
                            print("OUTCOME",type(outcome),len(outcome),outcome)
                            if len(outcome)<=6: # Just 'PELLET'
                                FOOD_REWARD(events,"Food_Pellet",cur_time)
                            else: #"PELLET##"
                                probability_of_reward = float(outcome[6:])
                                print("probability_of_reward: ",probability_of_reward)
                                if random.random()*100 <= probability_of_reward:
                                    FOOD_REWARD(events,"Food_Pellet w"+str(probability_of_reward)+ "% probability", cur_time)
                                else:
                                    log_event(events,"Reward NOT given w " + str(probability_of_reward)+"% probability", cur_time)


                        elif 'TONE' in outcome:
                            idx = outcome[4:]
                            if idx == '1':
                               PLAY_TONE(events,"TONE1",cur_time)
                               TONE_TIME = cur_time
                            elif idx == '2':
                               PLAY_TONE(events,"TONE2",cur_time)
                               TONE_TIME = cur_time

                        elif outcome == 'SHOCK':
                             log_event(events,"Shock_ON",cur_time,("Voltage", str(Shock_V),"Amps",str(Shock_Amp),"Duration(S)",str(Shock_Duration)))
                             SHOCK_ON = True
                             #shock.sendDBit(True)
                             #print("SHOCK ON")
                             #log_event(events,"Shock_ON",cur_time) # Also logged when user turns off in mouse press event
                             # NOTE: THIS IS A LATCH. TURNED OFF WHEN shock.sendDBit(False)
                             
                        else: #outcome == 'NONE'
                            log_event(events,"NONE",cur_time)
                            print("Outcome = NONE")
                        TIME_IS_UP = False
                        CONDITION_STARTED = False
                        Protocol_ln_num +=1
                    #print("CONDITIONS",conditions[choose_cond])
            else:
               print("PROTOCOL ITEM NOT RECOGNIZED",key)
               
########################################################################################################                        
            if BAR_PRESS_INDEPENDENT_PROTOCOL: #Running independently of CONDITIONS. Used for conditioning, habituation, extinction, and recall
               #print (cur_time,"VI................", VI, (VI_start + VI))
               if cur_time > (VI_start + VI):
                  #print("REWARD IS NOW POSSIBLE")
                  if levers[1].PRESSED: # RIGHT LEVER
                     levers[1].PRESSED = False
                     VI_start = cur_time
                     FOOD_REWARD(events,"Food_Pellet",cur_time)
##########################################################################################################


            if Protocol_ln_num >= len(protocol):
               #print("Protocol_ln_num: ",Protocol_ln_num,"plength: ", len(protocol),"\n")
               print("PROTOCOL ENDED")
               print(".................")
               log_event(events,"PROTOCOL ENDED",cur_time)
               START_EXPT = False
               Protocol_ln_num = 0
               LEDs[0].ONOFF = "OFF"
               LEDs[1].ONOFF = "OFF"
               L_CONDITIONING_LIGHT(events,False,cur_time)
               R_CONDITIONING_LIGHT(events,False,cur_time)

               # TEll open ephys to stop acquistion and recording?
              # snd.send(snd.STOP_ACQ)
               #snd.send(snd.STOP_REC)

               if TOUCHSCREEN_USED:
                   TSq.put('')
                   TOUCHSCREEN_USED = False

        # end of if START_EXPT:
################################################################################
#
################################################################################
def main():
    for arg in sys.argv[1:]:
        print (arg)
    BehavioralChamber()



if __name__ =='__main__':

       main()























       

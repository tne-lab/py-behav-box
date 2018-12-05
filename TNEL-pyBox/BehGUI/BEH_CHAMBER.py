"""
NOTE: 1. Please Start Whisker server first
      2. Check daqAPI.py on this directory.
         be sure Devices are named properly:

         on Ephis-1 'Dev1' runs behavior box
                    'pciDAQ' runs open ephys

         on Ephis-2 'Dev2' runs behavior box
                    'Dev1' runs open ephis
Developed by Flavio J.K. da Silva Nov. 31, 2018


"""
import json
import socket
from win32api import GetSystemMetrics
import os
import sys, errno, time, calendar
import pygame
import math
import numpy as np
import pylab
from NIDAQ_GUI_elements import *
from helperFunc import *
import daqAPI
from collections import deque

from multiprocessing import Process, Queue
import threading
#import subprocess # Subprocesses start new processes that are independent 
#import childVid #, parentVid3
##from datetime import datetime
################################################################
# GUI GLOBALS
################################################################
print ("Width ="), GetSystemMetrics(0)
print ("Height ="), GetSystemMetrics(1)

SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)
print("SCREEN WIDTH: ", SCREEN_WIDTH)
print("SCREEN HEIGHT: ", SCREEN_HEIGHT)
WINDOW_WIDTH = SCREEN_WIDTH - 100
WINDOW_WCENTER = WINDOW_WIDTH/2
WINDOW_HEIGHT = SCREEN_HEIGHT -100
WINDOW_HCENTER = WINDOW_HEIGHT/2
GAME_AREA = pygame.Rect(20, 10, WINDOW_WIDTH, WINDOW_HEIGHT)

################################################################
# NIDAQ GLOBALS
################################################################
# OUTPUTS
#fan = daqAPI.fanSetup()
#cabin_light = daqAPI.cabinLightSetup()
leverOut = daqAPI.leverOutputSetup()
food_light = daqAPI.foodLightSetup()
give_food = daqAPI.giveFoodSetup()
L_condition_Lt = daqAPI.conditioningLightsLeftSetup()
R_condition_Lt = daqAPI.conditioningLightsRightSetup()

#high_tone = daqAPI.highToneSetup()
#high_tone.sendDBit(False)
#low_tone = daqAPI.lowToneSetup()
#low_tone.sendDByte(0)
high_tone = daqAPI.lowToneSetup()
high_tone.sendDBit(False)
vidDict = {}

#INPUTS
L_nose_poke = daqAPI.leftNoseInputSetup()
R_nose_poke = daqAPI.rightNoseInputSetup()
checkPressLeft, checkPressRight = daqAPI.leverInputSetup()
eaten = daqAPI.foodEatInputSetup()

##################
# DATA
##################
cwd = os.getcwd()
datapath = os.path.join(cwd,"DATA")
date = time.strftime("%b-%d-%y")#month, day,Year, 
log_file_name = 'log_file-' + date + '.txt'
log_file_path_name = os.path.join(datapath,log_file_name)
print (log_file_name)


expt_file_name = 'expt_file-' + date + '.txt'
expt_file_path_name = os.path.join(datapath,expt_file_name )
#DataFile = open(data_file_name,'a')
#DataFile.write("date,\t\ttime,\t\tT(F)out,  T(F)in, T(F)soil, Rel_humidity, watering(T/F), OVERRIDE,\t INFO\n")
#DataFile.close()

import childVid #, parentVid3

def MyVideo():
    global vidDict  
    #myDict = {'cur_time':'0', 'STATE' = STATE}
    q = deque(maxlen = 1)
    if vidDict['STATE'] == 'START':
          print("STATE: ",vidDict['STATE'])
          p = threading.Thread(target=childVid.vidCapture, args=(q,))
          print (p)
          p.start()
          for i in range(0,1000):
              cur_time = time.perf_counter()
              #print('cur_time from Parent: ',cur_time)
              #myDict['cur_time'] = cur_time
              #x = input('Type to video: ')
              q.append(vidDict)
          #print("argv[1] = ",STATE)
          #vidDict['STATE'] = "STOP"
          q.append(vidDict)       
            

def exit_game():

      #DataFile.close()
      #fan.end()
      #cabin_light.end()
      leverOut.end()
      food_light.end()
      give_food.end()
      L_condition_Lt.end()
      R_condition_Lt.end()

      pygame.quit()
      sys.exit()


      
def log_event(event_lst,event,cur_time):
    global log_file_path_name
    log_file = open(log_file_path_name,'a')
    log_file.write(event+": "+str(cur_time)+'\n')
    event_lst.append(event+":" + str(cur_time))
    log_file.close()
    
def draw_speeker(myscreen, TONE_ON):
        if TONE_ON: col = (0,255,0)
        else:       col = (0,0,0)
        speeker = pygame.draw.circle(myscreen,col,(200,40),40,2)
        incr = 0
        for c in range (4):
              pygame.draw.circle(myscreen,col,(177+incr,25),5,1)
              incr += 15
        incr = 0
        for c in range (5):
              pygame.draw.circle(myscreen,col,(170+incr,40),5,1)
              incr += 15
        incr = 0      
        for c in range (4):
              pygame.draw.circle(myscreen,col,(177+incr,55),5,1)
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
        if CAMERA_ON: col = (0,255,0)
        elif REC:       col = (255,0,0)
        else:         col = (0,0,0)
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
      
def BehavioralChamber():
    global vidDict
    myscreen = pygame.display.set_mode((400,800),pygame.RESIZABLE,32)
    pygame.display.set_caption('Behavioral Chamber Control 1.0 by Flavio J.K. da Silva Oct. 30, 2018') # Enter your window caption here

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
    buttons,levers,boxes,circles,LEDs,toggles,sliders,info_boxes,user_inputs,labels = NIDAQ_GUI_ELEMENTS(myscreen,buttons,levers,boxes,circles,LEDs,toggles,sliders,info_boxes,labels)
    print(len(buttons), " buttons")
    print(len(levers), " buttons")
    print(len(boxes), " boxes")
    print(len(circles), " circles")
    print(len(LEDs), " LEDs")
    print(len(toggles), " toggles" )
    print(len(sliders), " sliders")
    print(len(labels), " labels")
    print(len(info_boxes), " info boxes")


    # MAIN LOOP
    clk_time_start = time.perf_counter()
    print (clk_time_start)
    FAN_0N = False
    BACKGROUND_LIT = False
    Background_color = (darkgray)
    FEEDER_LT_ON = False
    LEVERS_EXTENDED = False
    START_TIME = time.perf_counter()
    LEVER_PRESS_TIME = START_TIME
    NOSE_POKE_TIME = START_TIME
    TONE_TIME = START_TIME
    SHOCK_TIME = START_TIME
    
    num_L_nose_pokes = 0
    num_R_nose_pokes = 0
    num_L_lever_preses = 0
    num_R_lever_preses = 0
    num_pellets = 0
    num_eaten = 0
    NOSE_POKED_L = False
    NOSE_POKED_R = False
    LEVER_PRESSED_L = False
    LEVER_PRESSED_R = False
    SOUND_ON = False
    SHOCK_ON = False
    CAMERA_ON = False
    RECORDING = False
    #cam = video()
    events = []
    events.append(("StartTime: " + str(START_TIME)))

    #events=["test line1","test line2","test line3","test line4","test line5","test line6","test line7","test line8"]
    while True: # main game loop
        cur_time =  time.perf_counter()
        #startT = time.time()
        # Note Indents let the inperpreter know the following code is a subset of the current command.
        myscreen.fill((Background_color))
        #draw_rimmed_box(myscreen, Rect(WINDOW_WCENTER-100, 20,200, 560), (70,70,70), rim_width=5, rim_color=Color('black'))

        for button in buttons:
            button.draw()
            
        for box in boxes: # Must draw before items that go on top
            box.draw()

            
        for lever in levers:
            # Delay displaying lever state for visual purposes only (NOTE: PROGRAM IS NOT PAUSED!)
            if lever.index == 0: # LEFT LEVER
               if LEVER_PRESSED_L:
                  if (cur_time - LEVER_PRESS_TIME) > 0.5: #Leaves on for 0.5 sec
                     lever.STATE = "OUT" 
                     LEVER_PRESSED_L = False
                  else:
                     lever.STATE = "DN"
                   
            if lever.index == 1: # RIGHT LEVER
               if LEVER_PRESSED_R:
                  if (cur_time - LEVER_PRESS_TIME) > 0.5: #Leaves on for 0.5 sec
                     lever.STATE= "OUT"  
                     LEVER_PRESSED_R = False
                  else:
                     lever.STATE = "DN"
                     
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
            if info.label == "R NOSE POKES":
                  info.text = [str(num_R_nose_pokes)]
            if info.label == "L PRESSES":
                  info.text = [str(num_L_lever_preses)]
            if info.label == "R PRESSES":
                  info.text = [str(num_R_lever_preses) ]                                                    
            if info.label == "PELLETS":
                  info.text = [str(num_pellets)]
            if info.label == "EATEN":
                  info.text = [str(num_eaten)]
                  
            if info.label == "EXPT PATH":
                  info.text = [expt_file_path_name]
            if info.label == "LOG FILE DATA PATH":
                  info.text = [log_file_path_name]
                  
            if info.label == "EVENTS":
                  lines_in_txt = len(events)
                  if lines_in_txt > 6:
                      info.text = events[-6:]
                  else: info.text = events
            info.draw()

##        for event in user_inputs:
##            event.draw()
            
        # DRAW SPEEKER
        speeker = draw_speeker(myscreen,SOUND_ON)
        if SOUND_ON:
              if (cur_time - TONE_TIME) > 5:
                  SOUND_ON = False
                  high_tone.sendDBit(False)
                  #low_tone.sendDByte(0)
                  print("SOUND OFF")
                  
                  log_event(events,"Tone_OFF",cur_time)
              else:
                  high_tone.sendDBit(False)  
        
        # DRAW LIGHTNING
        shock = draw_lighting(myscreen, SHOCK_ON, 198,95,1,(255,255,0),2)
        if SHOCK_ON:
              if (cur_time - SHOCK_TIME) > 5: # 5 seconds
                  SHOCK_ON = False
                  #high_tone.sendDBit(False)
                  #low_tone.sendDByte(0)
                  print("SHOCK OFF")
                  log_event(events,"Shock_OFF",cur_time)
              else:
                  pass
                  #high_tone.sendDBit(False)               


        # DRAW CAMERA
        # draw_camera(myscreen,fill_color, ON_OFF, REC, x, y, w,h, linew) 
        camera = draw_camera(myscreen, (100,100,100),CAMERA_ON,RECORDING,185, 140, 30,20, 2)

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
                                    
                                    if BACKGROUND_LIT:
                                       events.append("Cabin Light OFF: " + str(cur_time))
                                       BACKGROUND_LIT = False
                                       Background_color = darkgray
                                       cabin_light.sendDBit(False)
                                       cabin_light.end()
                                    else:
                                       events.append("Cabin Light ON: " + str(cur_time))
                                       BACKGROUND_LIT = True
                                       Background_color = gray
                                       cabin_light = daqAPI.cabinLightSetup()
                                       cabin_light.sendDBit(True)
                               if button.text == "FAN":
                                    if FAN_0N:
                                       FAN_0N = False
                                       log_event(events,"Fan_OFF",cur_time)
                                       #events.append("Fan OFF: " + str(cur_time))                                       FAN_0N = False
                                       fan.sendDBit(False)
                                       fan.end()
                                    else:
                                       log_event(events,"Fan_ON",cur_time)
                                       #events.append("Fan ON: " + str(cur_time))
                                       FAN_0N = True
                                       fan = daqAPI.fanSetup()
                                       fan.sendDBit(True)
                                       
                               elif button.text == "FEED":
                                    button.UP_DN = "DN"
                                    FEED = True
                                    log_event(events,"Food_Pellet",cur_time)
                                    #events.append("Food Pellet: " + str(cur_time))
                                    num_pellets +=1
                                    give_food.sendDBit(True)
                                    give_food.sendDBit(False)
                                    
                               elif button.text == "EXTEND" or button.text == "RETRACT":
                                    if LEVERS_EXTENDED: #Toggle
                                          button.UP_DN = "UP"
                                          LEVERS_EXTENDED = False
                                          log_event(events,"Levers_Retracted",cur_time)
                                          #events.append("Levers Retracted: " + str(cur_time))
                                          button.text = "EXTEND"
                                          for lever in levers:
                                                lever.STATE = "IN"
                                          leverOut.sendDByte(0)
                                          
                                    else: # not extended
                                          button.UP_DN = "DN"
                                          button.text = "RETRACT"
                                          log_event(events,"Levers_Extended",cur_time)
                                          #events.append("Levers Extended: " + str(cur_time))
                                          LEVERS_EXTENDED = True
                                          for lever in levers:
                                                lever.STATE = "OUT"
                                          leverOut.sendDByte(3)

                                          
                               LEFT_MOUSE_DOWN = False
                               BUTTON_SELECTED = True
                               dx = cur_x - button.x
                               dy = cur_y - button.y

                    # LEVERS
                    for lever in levers: # Check for collision with EXISTING buttons
                        if LEVERS_EXTENDED:
                              if lever.rect.collidepoint(cur_x,cur_y):
                                    if lever.text == "L LEVER":
                                          lever.STATE = "DN"
                                          #events.append("Left Lever Pressed: " + str(cur_time))
                                    elif lever.text == "R LEVER":
                                          lever.STATE = "DN"
                                          #events.append("Right Lever Pressed: " + str(cur_time))
                                    # NOTE:  We are redrawing here again (instead of just in main loop)
                                    #       because state will be reset ot actual machine state (which is what
                                    #       really matters.  I you don't care about this, comment out next 3 lines.
                                    lever.draw() 
                                    pygame.display.flip()
                                    time.sleep(0.25) # sec

                    # LEDS        
                    for LED in LEDs: # Check for collision with EXISTING buttons
                        if LED.rect.collidepoint(cur_x,cur_y):
                            idx = LEDs.index(LED)
                            print ("LED ID: ",idx)
                            if LED.ONOFF == "OFF": # WAS OFF
                                LED.ONOFF = "ON"   # NOW ON
                                # STIM LIGHTS
                                if   LED.index == 0: # LEFT CONDITION LIGHT
                                    L_condition_Lt.sendDBit(True)
                                    log_event(events,"Left_Light_ON",cur_time)
                                    #events.append("Left Light ON: " + str(cur_time))
                                elif LED.index == 1: # RIGHT CONDITION LIGHT
                                    R_condition_Lt.sendDBit(True)
                                    #events.append("Right Light ON: " + str(cur_time))
                                    log_event(events,"Right_Light_ON",cur_time)
                                    
                                # NOSE POKES    
                                elif LED.index == 2 or LED.index == 3: # NOSE POKES
                                   NOSE_POKE_TIME = time.perf_counter()
                                   # NOTE:  We are redrawing here again (instead of just in main loop)
                                   #       because state will be reset ot actual machine state (which is what
                                   #       really matters.  I you don't care about this, comment out next 3 lines.
                                   LED.draw() 
                                   pygame.display.flip()
                                   time.sleep(0.25) # sec

                                   
                            else:                  # WAS ON
                                LED.ONOFF = "OFF"  # NOW OFF
                                LED.draw()
                                if   LED.index == 0: # LEFT CONDITION LIGHT
                                    L_condition_Lt.sendDBit(False)
                                    log_event(events,"Left_Light_OFF",cur_time)
                                    #events.append("Left Light OFF: " + str(cur_time))
                                elif LED.index == 1: # RIGHT CONDITION LIGHT
                                    R_condition_Lt.sendDBit(False)   
                                    #events.append("Right Light OFF: " + str(cur_time))
                                    log_event(events,"Right_Light_OFF",cur_time)
                                    
                    for box in boxes: # Check for collision with EXISTING buttons
                        if box.rect.collidepoint(cur_x,cur_y):
                              if FEEDER_LT_ON:
                                  FEEDER_LT_ON = False
                                  box.fill_color = black
                                  LEDs[4].ONOFF = "OFF"
                                  LEDs[5].ONOFF = "OFF"
                                  food_light.sendDBit(False)
                                  #events.append("Feeder Linght OFF: " + str(cur_time))
                                  log_event(events,"Feeder_Light_OFF",cur_time)
                              else:
                                  FEEDER_LT_ON = True
                                  box.fill_color = gray
                                  LEDs[4].ONOFF = "ON"
                                  LEDs[5].ONOFF = "ON"
                                  #events.append("Feeder Linght ON: " + str(cur_time))
                                  log_event(events,"Feeder_Light_ON",cur_time)
                                  food_light.sendDBit(True)
                                  print("FEEDER PRESSED")
                                  
                    # SPEEKER PRESSED
                    if speeker.collidepoint(cur_x,cur_y):
                          TONE_TIME = cur_time
                          if SOUND_ON:
                                SOUND_ON = False
                                #events.append("Sound OFF: " + str(cur_time))
                                log_event(events,"Tone_OFF",cur_time)
                          else: 
                                SOUND_ON = True
                                # TONE TRUNED OFF IN GAME LOOP AFTER HALF A SEC
                                #high_tone.sendDBit(True)
                                #low_tone.sendDBit(True)
                                #low_tone.sendDByte(128)
                                high_tone.sendDBit(True)
                                print("TONE PRESSED")
                                #events.append("Sound ON: " + str(cur_time))
                                log_event(events,"Tone_ON",cur_time)
                    # SHOCK PRESSED
                    if shock.collidepoint(cur_x,cur_y):
                          SHOCK_TIME = cur_time
                          if SHOCK_ON:
                                SHOCK_ON = False
                                #events.append("Shock OFF: " + str(cur_time))
                                log_event(events,"Shock_OFF",cur_time)
                          else: 
                                SHOCK_ON = True
                                #events.append("Shock ON: " + str(cur_time))
                                log_event(events,"Shock_ON",cur_time)
                          # TONE TRUNED OFF IN GAME LOOP AFTER HALF A SEC
                          #high_tone.sendDBit(True)
                          #low_tone.sendDBit(True)
                          #low_tone.sendDByte(128)
                          #high_tone.sendDBit(True)
                          print("SHOCK PRESSED")
                          
                    # CAMERA PRESSED
                    if camera.collidepoint(cur_x,cur_y):
                          if CAMERA_ON:
                                CAMERA_ON = False
                                #events.append("Camera OFF: " + str(cur_time))
                                log_event(events,"Camera_OFF",cur_time)
                                print("CAMERA OFF")
                                vidDict = {'cur_time':cur_time, 'STATE' : 'START'}
                                
                          else:
                                
                                CAMERA_ON = True
                                #events.append("Camera ON: " + str(cur_time))
                                log_event(events,"Camera_ON",cur_time)
                                print("CAMERA ON")
                                vidDict = {'cur_time':cur_time, 'STATE' : 'START'}
                                #q = Queue(1)
                                #vid = os.system('python parentVid.py') #Works but does not do in parallel
                                MyVideo()
                                #print(vid)
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
                               
                    # SLIDERS
                    for sld in sliders: # Check for collision with SLIDERS
                        if sld.rect.collidepoint(cur_x,cur_y):
                            SLIDER_SELECTED = True
                            cur_slider = sld               
                                   
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
                    button.UP_DN = "UP"
                    #button.draw()
                    
                for lever in levers: # Check for collision with EXISTING buttons
                    if LEVERS_EXTENDED:
                          lever.STATE = "OUT"
                    else:
                          lever.STATE = "IN"
                    #lever.draw()
                 
        ######################################
        #   CHECK INPUTS
        ######################################               
        # levers
        if LEVERS_EXTENDED:
              wasleverPressed = detectPress(checkPressLeft,checkPressRight)
              cur_time = time.perf_counter()
              LEVER_PRESS_TIME = cur_time
              if  wasleverPressed == 'Right':
                    #events.append("Right Lever Pressed: " + str(cur_time))
                    log_event(events,"Lever_Pressed_R",cur_time)
                    LEVER_PRESSED_R = True
                    print("RIGHT LEVER PRESSED")
                    num_R_lever_preses += 1
                    levers[1].STATE = "DN"
              #else: levers[1].STATE = "OUT"
              
              if  wasleverPressed == 'Left':
                    #events.append("Left Lever Pressed: " + str(cur_time))
                    log_event(events,"Lever_Pressed_L",cur_time)
                    LEVER_PRESSED_L = True
                    print("LEFT LEVER PRESSED")
                    num_L_lever_preses += 1
                    levers[0].STATE = "DN"
              else: levers[0].STATE = "OUT"      

        # nose pokes              
        was_nose_poked_L = checkLeftNosePoke(L_nose_poke)
        cur_time = time.perf_counter()
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
        foodEaten = checkFoodEaten(eaten)
        cur_time = time.perf_counter()
        if foodEaten:
            print("Yum!")
            num_eaten +=1
            #events.append("Food Eaten: " + str(cur_time))
            log_event(events,"Food_Eaten",cur_time)
        
        ######################################
        #   UPDATE SCREEN
        ######################################
        
        pygame.display.flip()
        #endT = time.time()
        #print("Main Loop t = ",(endT - startT))
#########################################################################################

def main():  
    for arg in sys.argv[1:]:
        print (arg)
    BehavioralChamber()



if __name__ =='__main__':

       main()

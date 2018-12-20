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

#from win32api import GetSystemMetrics
import os
import sys, time
import pygame
import pygame
from pygame.locals import *

import math, random
import numpy as np
import zmq
import json
#from NIDAQ_GUI_elements import *
from RESOURCES.GUI_elements_by_flav import *
try:
    import daqHelper
    import daqAPI
    NIDAQ_AVAILABLE = True
except:
    NIDAQ_AVAILABLE = False

from collections import deque
from multiprocessing import Process, Queue
import threading
import whiskerTouchZMQ
import zmqClasses
import eventRECV
import GUIFunctions
import subprocess
#import win32gui, win32con


IsWhiskerRunning = False
IsOpenEphysRunning = False
# Add open ephys here possibly?
def lookForWhisker(hwnd, args):
    global IsWhiskerRunning, IsOpenEphysRunning
    #if 'WhiskerServer' in win32gui.GetWindowText(hwnd):
    #    win32gui.CloseWindow(hwnd) # Minimize Window
    #    IsWhiskerRunning = True

def openWhisker():
    global IsWhiskerRunning, IsOpenEphysRunning
    #win32gui.EnumWindows(lookForWhisker, None)
    if not IsWhiskerRunning:
        try:
            #ws = "C:\Program Files (x86)\WhiskerControl\WhiskerServer.exe"
            #window = subprocess.Popen(ws)# # doesn't capture output
            time.sleep(2)
            print("WHISKER server started", window)
            #win32gui.EnumWindows(lookForWhisker, None)
        except:
            print("Could not start WHISKER server")
    else: print("Whisker server is already RUNNING")
    print(".............................................")


class BEH_GUI():
    def __init__(self, NIDAQ_AVAILABLE):
        self.NIDAQ_AVAILABLE = NIDAQ_AVAILABLE
        self.setGlobals()
        random.seed()
        self.load_expt_file()
        self.setupGUI()

    from setGlobals import setGlobals
    from loadProtocol import load_expt_file
    import GUIFunctions
    from setupGUI import setupGUI

    def BehavioralChamber(self):
        while True:
            #cur_time =  time.perf_counter()

            if not self.VIDBack_q.empty():
                backDict = self.VIDBack_q.get()
                if backDict['FROZEN']: # FROZEN
                      # NOTE: this must be "debounced"
                      if not self.FROZEN_ALREADY_LOGGED:
                          print("LOGGING FROZEN")
                          GUIFunctions.log_event(self, self.events,"Frozen",self.cur_time,("Orig_NIDAQ_t",backDict['NIDAQ_time'],"video_time",backDict['vid_time'],"time_diff",backDict['Vid-NIDAQ']))
                          self.FROZEN_ALREADY_LOGGED = True
                          self.UNFROZEN_ALREADY_LOGGED = False

                else:  # UN FROZEN
                    if self.PREVIOUSLY_FROZEN:
                       # NOTE: this must be "debounced"
                       if not self.UNFROZEN_ALREADY_LOGGED:
                            GUIFunctions.log_event(self, self.events,"Unfrozen",self.cur_time)
                            self.FROZEN_ALREADY_LOGGED = False
                            self.UNFROZEN_ALREADY_LOGGED = True

            if not self.openEphysBack_q.empty():
                OEMsg = self.openEphysBack_q.get()
                #print(OEMsg)

            self.drawScreen()
            self.checkSystemEvents()
            self.checkNIDAQEvents()

            if self.RUN_SETUP:
                self.runSetup()
            if self.START_EXPT:
                self.runExpt()

            ######################################
            #   UPDATE SCREEN
            ######################################
            pygame.display.flip()

            ######################################
            #   UPDATE VIDEO
            ######################################
            self.vidDict['cur_time'] = self.cur_time
            self.vidDict['trial_num'] = self.trial_num
            self.VIDq.append(self.vidDict)
########################################################################################
    def drawScreen(self):
        self.cur_time = time.perf_counter()-self.Experiment_Start_time
        #print("cur_time : Experiment_Start_time-->",self.cur_time, self.Experiment_Start_time)
        #######################
        # DRAW SCREEN AND GUI ELEMENTS
        #######################
        self.myscreen.fill(self.Background_color)
        #self.myscreen.blit(self.TNElogo,(400,5))
        for button in self.buttons:
            button.draw()

        for box in self.boxes: # Must draw before items that go on top
            box.draw()


        for lever in self.levers:
            #lever.state = "IN"
            # Delay displaying lever state for visual purposes only (NOTE: PROGRAM IS NOT PAUSED!)
            if lever.index == 0: # LEFT LEVER
               if  lever.STATE == "OUT":
                   if self.LEVER_PRESSED_L:
                      if (self.cur_time - LEVER_PRESS_TIME) > 0.5: #Leaves on for 0.5 sec
                         lever.STATE = "OUT"
                         LEVER_PRESSED_L = False
                      else:
                         lever.STATE = "DN"
               # else lever.state == "IN" or "DN"

            if lever.index == 1: # RIGHT LEVER
               if  lever.STATE == "OUT":
                   if self.LEVER_PRESSED_R:
                      if (self.cur_time - self.LEVER_PRESS_TIME) > 0.5: #Leaves on for 0.5 sec
                         lever.STATE= "OUT"
                         self.LEVER_PRESSED_R = False
                      else:
                         lever.STATE = "DN"
               # else lever.state == "IN" or "DN"

            lever.draw()

        for LED in self.LEDs:
            # Leaves nose poke LED ON for 1 sec so user can see it (NOTE: PROGRAM IS NOT PAUSED!)
            if LED.index == 2: #Left NOSE POKE
               if self.NOSE_POKED_L:
                   if (self.cur_time - self.NOSE_POKE_TIME) > 0.25: #Leaves on for 0.25 sec
                         LED.ONOFF = "OFF"  # NOW OFF
                         self.NOSE_POKED_L = False
                   else:
                         LED.ONOFF = "ON"

            elif LED.index == 3: #Right NOSE POKE
                if self.NOSE_POKED_R:
                   if (self.cur_time - self.NOSE_POKE_TIME) > 0.25: #Leaves on for 0.25 sec
                         LED.ONOFF = "OFF"  # NOW OFF
                         self.NOSE_POKED_R = False
                   else:
                         LED.ONOFF = "ON"

            LED.draw()

##        for tog in self.toggles:
##            tog.draw()



        for lbl in self.labels: # Last so on top
            lbl.draw()

        for info in self.info_boxes: # Last so on top
            if info.label == "L NOSE POKES":
                  info.text = [str(self.num_L_nose_pokes)]
            elif info.label == "R NOSE POKES":
                  info.text = [str(self.num_R_nose_pokes)]
            elif info.label == "L PRESSES":
                  info.text = [str(self.num_L_lever_preses)]
            elif info.label == "R PRESSES":
                  info.text = [str(self.num_R_lever_preses) ]
            elif info.label == "PELLETS":
                  info.text = [str(self.num_pellets)]
            elif info.label == "EATEN":
                  info.text = [str(self.num_eaten)]
            elif info.label == "DATE":
                  info.text = [str(self.date)]
            elif info.label == "TIME":
                if self.START_EXPT: info.text = [str(round(self.cur_time,3))]
                else: info.text = ['0.000']
            elif info.label == "EVENT LOG":
                lines_in_txt = len(self.events)
                self.y_per_line = int(self.sliders[0].slotL / 14.0)

                if lines_in_txt > 14: # 14 lines fit in window
                    ##########################################################
                    # SLIDER:
                    #               NOTE only 14 text lines fit inside window
                    ##########################################################
                    slider_Button_ht = int((14.0/float(lines_in_txt)) * self.sliders[0].slotL) # portion of SlotL
                    if slider_Button_ht <= 14:
                        self.sliders[0].bh = 14
                    else:
                        self.sliders[0].bh = slider_Button_ht

                    self.sliders[0].sliderY = self.new_slider_y #+ self.start_line * self.y_per_line
                    #self.sliders[0].sliderY = self.new_slider_y + (self.sliders[0].slotL - self.sliders[0].bh) - self.start_line * self.y_per_line


                    if self.sliders[0].sliderY >= self.sliders[0].slotL - self.sliders[0].bh:
                       self.sliders[0].sliderY = self.sliders[0].slotL - self.sliders[0].bh
                    self.sliders[0].draw()
                    info.text = self.events[self.start_line:self.start_line+15]
                else: info.text = self.events

            info.draw()

        # USER INPUTS
        for user_input in self.user_inputs:
            if user_input.label == "EXPT":
                 user_input.text = str(self.Expt_Name)
            elif user_input.label == "SUBJECT":
                 user_input.text = str(self.Subject)
            elif user_input.label == "TRIAL":
                 user_input.text  = str(self.trial_num)
            elif user_input.label == "EXPT PATH":
                 user_input.text = str(self.datapath)
            elif user_input.label == "EXPT FILE NAME":
                 user_input.text = str(self.expt_file_name)
            elif user_input.label == "Spk(S)":
                 user_input.text  = str(self.Tone1_Duration)
            elif user_input.label == "Freq(Hz)":
                 user_input.text  = str(self.Tone1_Freq)
            elif user_input.label == "Vol(0-1)":
                 user_input.text  = str(self.Tone1_Vol)
            elif user_input.label == "Shck(S)":
                 user_input.text = str(self.Shock_Duration)
            elif user_input.label == "V":
                 user_input.text = str(self.Shock_V)
            elif "Amps" in user_input.label:
                 user_input.text = str(self.Shock_Amp)

            user_input.draw()


        # DRAW SPEEKER
        self.speeker = GUIFunctions.draw_speeker(self.myscreen,250,85,self.TONE_ON) #TONE_ON is T/F

        if self.TONE_ON:
              if (self.cur_time - self.TONE_TIME) > float(self.Tone1_Duration): # seconds
                  print("TONE OFF")
                  self.TONE_ON = False
                  GUIFunctions.log_event(self, self.events,"Tone_OFF",self.cur_time)

        # DRAW SHOCK LIGHTNING
        self.shock = GUIFunctions.draw_lighting(self.myscreen, self.SHOCK_ON, 248,150,1,(255,255,0),2)
        if self.SHOCK_ON:
              if (self.cur_time - self.SHOCK_TIME) <= self.Shock_Duration: # seconds
                  self.apply_shock.sendDBit(True)
              else:
                  self.SHOCK_ON = False
                  self.apply_shock.sendDBit(False)
                  print("SHOCK OFF")
                  GUIFunctions.log_event(self, self.events,"Shock_OFF",self.cur_time)


        # DRAW CAMERA
        #    Note:                 draw_camera(self.myscreen,fill_color, ON_OFF, REC, x, y, w,h, linew)
        self.camera = GUIFunctions.draw_camera(self.myscreen, (100,100,100),self.CAMERA_ON,self.RECORDING,235, 255, 30,20, 2)
###########################################################################################################
#  HANDLE GUI EVENTS
###########################################################################################################
    def checkSystemEvents(self):
        '''
         SYSTEM EVENTS
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                GUIFunctions.exit_game(self)

            ##############################################################
            #  MOUSE EVENTS (always active independent of game mode)
            ##############################################################
            #--------------------------------------------------
            # MOUSE MOVE
            elif (event.type == pygame.MOUSEMOTION):#
                cur_x,cur_y = pygame.mouse.get_pos()

                if self.LEFT_MOUSE_DOWN:
                    if self.SLIDER_SELECTED:
                        new_slider_y = cur_y - self.cur_Vslider.y # relative to top of slider slot
                        if new_slider_y <= 0:
                           new_slider_y = 0
                        if new_slider_y >= self.cur_Vslider.slotL - self.cur_Vslider.bh:
                           new_slider_y = self.cur_Vslider.slotL - self.cur_Vslider.bh

                        self.cur_Vslider.sliderY = new_slider_y # relative to top of slider slot
                        self.new_slider_y = new_slider_y
                        self.start_line = int(new_slider_y/self.y_per_line)


            # ----------------------------------------
            # MOUSE DOWN
            elif (event.type == pygame.MOUSEBUTTONDOWN ):#Mouse Clicked
                self.LEFT_MOUSE_DOWN = False
                self.RIGHT_MOUSE_DOWN = False
                cur_x,cur_y = pygame.mouse.get_pos()
                #print("MOUSE_Button ",event.button, "pressed!", cur_x,cur_y)
                if event.button == 1:
                    self.LEFT_MOUSE_DOWN = True
                elif event.button == 3:
                    self.RIGHT_MOUSE_DOWN = True
                # BUTTONS
                if self.LEFT_MOUSE_DOWN:

                    # SLIDERS
                    for slider in self.sliders: # Check for collision with EXISTING buttons
                        if slider.button_rect.collidepoint(cur_x,cur_y):
                            #print("SLIDER SELECTED", slider)
                            self.SLIDER_SELECTED = True
                            self.cur_Vslider = slider

                    # BUTTONS
                    for button in self.buttons: # Check for collision with EXISTING buttons
                        if button.rect.collidepoint(cur_x,cur_y):
                               button.UP_DN = "DN"
                               #button.draw()
                               if button.text == "CABIN LT":
                                   if self.CAB_LIGHT_ON: #Toggle OFF
                                       self.Background_color = GUIFunctions.CAB_LIGHT(self, self.events,False,self.cur_time)
                                       self.CAB_LIGHT_ON = False
                                   else: # Toggle ON
                                       self.Background_color = GUIFunctions.CAB_LIGHT(self, self.events,True,self.cur_time)
                                       self.CAB_LIGHT_ON = True
                               if button.text == "FAN": #TOGGLE ON TOGGLE OFF
                                    if self.FAN_0N:
                                       self.FAN_0N = False
                                       GUIFunctions.FAN_ON_OFF(self, self.events,self.FAN_0N,self.cur_time)

                                    else:
                                       self.FAN_0N = True
                                       GUIFunctions.FAN_ON_OFF(self, self.events,self.FAN_0N,self.cur_time)

                               elif button.text == "FEED":
                                    button.UP_DN = "DN"
                                    self.FEED = True
                                    GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet_by_GUI", self.cur_time)
                                    # NOTE: Food reward needs time after High bit, before low bit is sent.
                                    #       So rather than putting a sleep in the FOOD_REWARD function, a low bit
                                    #       is sent when button is released using FOOD_REWARD_RESET(self)
                               # LEFT LEVER
                               elif button.text == "L":
                                    if self.L_LEVER_EXTENDED: # Was EXTENDED
                                          button.UP_DN = "UP"
                                          GUIFunctions.EXTEND_LEVERS(self,self.events,"L_Lever_Retracted_by_GUI",False,False,self.cur_time)
                                          self.levers[0].STATE = "IN"

                                    else: # Was not extended
                                          button.UP_DN = "DN"
                                          GUIFunctions.EXTEND_LEVERS(self,self.events,"L_Lever_Extended_by_GUI",True,False,self.cur_time)
                                          self.levers[0].STATE = "OUT"

                               # RIGHT LEVER
                               elif button.text == "R":
                                    if self.R_LEVER_EXTENDED: # Was EXTENDED
                                          button.UP_DN = "UP"
                                          GUIFunctions.EXTEND_LEVERS(self,self.events,"R_Lever_Retracted_by_GUI",False,False,self.cur_time)
                                          self.levers[1].STATE = "IN"

                                    else: # was not extended
                                          button.UP_DN = "DN"
                                          GUIFunctions.EXTEND_LEVERS(self,self.events,"R_Lever_Extended_by_GUI",False,True,self.cur_time)
                                          self.levers[1].STATE = "OUT"

                               # BOTH LEVERS AT ONCE
                               elif button.text == "EXTEND" or button.text == "RETRACT":
                                    if self.LEVERS_EXTENDED: #Toggle EXTEND and RETRACT
                                          button.UP_DN = "UP"
                                          #LEVERS_EXTENDED = False
                                          GUIFunctions.EXTEND_LEVERS(self,self.events,"Levers_Retracted_by_GUI",False,False,self.cur_time)
                                          button.text = "EXTEND"
                                          for lever in self.levers:
                                                lever.STATE = "IN"

                                    else: # not extended
                                          button.UP_DN = "DN"
                                          button.text = "RETRACT"
                                          #LEVERS_EXTENDED = True
                                          GUIFunctions.EXTEND_LEVERS(self,self.events,"Levers_Extended_by_GUI",True,True,self.cur_time)
                                          for lever in self.levers:
                                                lever.STATE = "OUT"

                               elif button.text == "REC":
                                    if self.CAMERA_ON:
                                          if self.RECORDING: #STOP RECORDING BUT KEEP CAMERA ON
                                                self.RECORDING = False
                                                GUIFunctions.log_event(self, self.events,"STOP_RECORDING_by_GUI",self.cur_time)
                                                self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'ON', 'PATH_FILE':self.video_file_path_name}
                                                button.UP_DN = "UP"
                                          else:
                                                self.RECORDING = True
                                                button.UP_DN = "DN"
                                                GUIFunctions.log_event(self, self.events,"START_RECORDING_by_GUI",self.cur_time)
                                                self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'REC', 'PATH_FILE':self.video_file_path_name}


                                    else:
                                          print("CAMERA NOT ON!")

                               elif button.text == "LOAD FILE":
                                    button.UP_DN = "DN"
                                    print(self.expt_file_path_name)
                                    if self.load_expt_file():
                                        self.EXPT_FILE_LOADED = True
                                        GUIFunctions.log_event(self, self.events,"EXPT FILE LOADED",self.cur_time)
                                        if len(self.setup) > 0:
                                            self.RUN_SETUP = True
                                            self.setup_ln_num = 0
                                    for LED in self.LEDs: # Look for EXPT STARTED LED
                                          if LED.index == 6: # Expt Started light
                                              LED.ONOFF = "OFF"
                                    else:
                                        print("HUMPH!")
                                        GUIFunctions.log_event(self, self.events,"Expt File name or path DOES NOT EXIST",self.cur_time)

                               elif button.text == "START EXPT":
                                    print("EXPT STARTED!")
                                    button.UP_DN = "DN"
                                    self.Expt_Count +=1
                                    if self.EXPT_FILE_LOADED:
                                        self.trial_num = 0
                                        if self.TOUCHSCREEN_USED: GUIFunctions.StartTouchScreen(self)
                                        for user_input in self.user_inputs:
                                            if user_input.label == "EXPT":
                                                user_input.text = str(self.Expt_Name)+str(self.Expt_Count)
                                        if  self.BAR_PRESS_INDEPENDENT_PROTOCOL:
                                        # NOTE: THIS IS USED IF REWARDING FOR BAR PRESS (AFTER VI) IS THE ONLY CONDITION (HABITUATION AND CONDITIONING ARE RUNNING CONCURRENTLY)
                                            self.VI_start = 0.0 #self.cur_time
                                            self.VI = random.randint(0,int(self.var_interval_reward*2))
                                            print("VI.......................", self.VI)
                                        GUIFunctions.log_event(self, self.events,"EXPT STARTED",self.cur_time)
                                        self.START_EXPT = True
                                        #self.snd.send(self.snd.START_ACQ) # Press play on Open Ephys GUI
                                        #self.snd.send(self.snd.START_REC) # Press RECORD on Open Ephys GUI
                                        self.vidDict['STATE'] = 'START'

                                        self.Experiment_Start_time = time.perf_counter()
                                        self.cur_time = self.cur_time-self.Experiment_Start_time
                                        print("BUTTON cur_time : Experiment_Start_time-->",self.cur_time, self.Experiment_Start_time)
                                        for LED in self.LEDs: # Look for EXPT STARTED LED
                                              if LED.index == 6: # Expt Started light
                                                  LED.ONOFF = "ON"
                                        ###############################################################
                                        #
                                        # ?????????????????????????????????????????
                                        # SEND BIT TO OPEND EPHYS TO INDICATE EXPT STARTED.
                                        # CAN RECORD SIGNAL BE THE START EVENT?????
                                        #
                                        ################################################################
                                    else:
                                        GUIFunctions.log_event(self, self.events,"EXPT FILE NOT LOADED!!!!",self.cur_time)

                               self.LEFT_MOUSE_DOWN = False
                               self.BUTTON_SELECTED = True
                               dx = cur_x - button.x
                               dy = cur_y - button.y

                    # LEVERS
                    for lever in self.levers:
                        if lever.rect.collidepoint(cur_x,cur_y): # Check for collision with EXISTING levers
                            #LEVER_PRESS_TIME = time.perf_counter()
                            if lever.text == "L LEVER":
                                if self.L_LEVER_EXTENDED:
                                      lever.STATE = "DN"
                                      #NOTE: Lever presses are not logged here, but when actually pressed in Behavioral Chamber


                            if lever.text == "R LEVER":
                                if self.R_LEVER_EXTENDED:
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
                    for LED in self.LEDs: # Check for collision with EXISTING buttons
                      if LED.clickable: # Toggled On/Off when clicked
                        if LED.rect.collidepoint(cur_x,cur_y):
                            idx = self.LEDs.index(LED)
                            print ("LED ID: ",idx)
                            if LED.ONOFF == "OFF": # WAS OFF
                                LED.ONOFF = "ON"   # NOW ON
                                if   LED.index == 0: # LEFT CONDITION LIGHT
                                    GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,True,self.cur_time)
                                elif LED.index == 1: # RIGHT CONDITION LIGHT
                                    GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,True,self.cur_time)

                                # NOSE POKES
                                elif LED.index == 2 or LED.index == 3: # NOSE POKES
                                   self.NOSE_POKE_TIME = time.perf_counter()
                                   # NOTE:  We are redrawing here again (instead of just in main loop)
                                   #       because state will be reset ot actual machine state (which is what
                                   #       really matters.  I you don't care about this, comment out next 3 lines.
                                   LED.draw()
                                   pygame.display.flip()
                                   time.sleep(0.25) # sec

                                # FEEDER LEDS
                                elif LED.index == 4 or LED.index == 5: # FEEDER LIGHTS
                                    self.feederBox.fill_color,LEDsONOFF = GUIFunctions.Food_Light_ONOFF (self, self.events,True,self.cur_time)
                                    self.LEDs[4].ONOFF = LEDsONOFF
                                    self.LEDs[5].ONOFF = LEDsONOFF

                            else:                  # WAS ON
                                LED.ONOFF = "OFF"  # NOW OFF
                                LED.draw()
                                if   LED.index == 0: # LEFT CONDITION LIGHT
                                    GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)
                                elif LED.index == 1: # RIGHT CONDITION LIGHT
                                    GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)

                                # FEEDER LEDS
                                elif LED.index == 4 or LED.index == 5: # FEEDER LIGHTS
                                    self.feederBox.fill_color,LEDsONOFF = GUIFunctions.Food_Light_ONOFF (self, self.events,False,self.cur_time)
                                    self.LEDs[4].ONOFF = LEDsONOFF
                                    self.LEDs[5].ONOFF = LEDsONOFF


                    # FEEDER BOXES
                    for box in self.boxes: # Check for collision with EXISTING buttons
                        if box.rect.collidepoint(cur_x,cur_y):
                           if self.FEEDER_LT_ON: #Toggle OFF
                              self.feederBox.fill_color,LEDsONOFF = GUIFunctions.Food_Light_ONOFF(self, self.events,False,self.cur_time)
                              self.LEDs[4].ONOFF = LEDsONOFF
                              self.LEDs[5].ONOFF = LEDsONOFF
                              self.FEEDER_LT_ON = False
                           else: # Toggle ON
                              self.feederBox.fill_color,LEDsONOFF = GUIFunctions.Food_Light_ONOFF (self, self.events,True,self.cur_time)
                              self.FEEDER_LT_ON = True

                    # SPEEKER PRESSED
                    if self.speeker.collidepoint(cur_x,cur_y):
                          # NOTE: Tone_OFF logged while drawing speeker above in main loop
                          self.GUIFunctions.PLAY_TONE(self, self.events,"TONE1",self.cur_time)


                    # SHOCK PRESSED
                    if self.shock.collidepoint(cur_x,cur_y):
                          self.SHOCK_TIME = self.cur_time
                          if self.SHOCK_ON:
                                self.SHOCK_ON = False
                                GUIFunctions.log_event(self, self.events,"Shock_OFF",self.cur_time)
                                # NOTE: SHOCK ALSO TURNED OFF IN GAME LOOP AFTER Shock_Duration (s)
                          else:
                                self.SHOCK_ON = True
                                GUIFunctions.log_event(self, self.events,"Shock_ON",self.cur_time,("Voltage", str(self.Shock_V),"Amps",str(self.Shock_Amp),"Duration(S)",str(self.Shock_Duration)))
                                # NOTE: SHOCK ALSO TURNED OFF IN GAME LOOP AFTER Shock_Duration (s)

                          print("SHOCK PRESSED")

                    # CAMERA PRESSED
                    if self.camera.collidepoint(cur_x,cur_y):
                          if self.CAMERA_ON: #CAMERAL ALREWADY ON, TURN CAMERA OFF
                                self.CAMERA_ON = False
                                self.RECORDING = False
                                GUIFunctions.log_event(self, self.events,"Camera_OFF",self.cur_time)
                                print("CAMERA OFF")
                                self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'STOP', 'PATH_FILE':self.video_file_path_name}

                          else: #TURN CAMERA ON
                                self.CAMERA_ON = True
                                GUIFunctions.log_event(self, self.events,"Camera_ON",self.cur_time)
                                print("CAMERA ON")
                                self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'ON', 'PATH_FILE':self.video_file_path_name}
                                GUIFunctions.MyVideo(self)

                    # USER KEYBOARD INPUTS
                    for user_input in self.user_inputs:
                        if user_input.rect.collidepoint(cur_x,cur_y):
                            user_input.get_key_input()
                            if user_input.label == "EXPT":
                                 self.Expt_Name=user_input.text
                            elif user_input.label == "SUBJECT":
                                 self.Subject = user_input.text
                            elif user_input.label == "TRIAL":
                                 self.trial_num =  user_input.text
                            elif user_input.label == "EXPT PATH":
                                 self.datapath = user_input.text
                            elif user_input.label == "EXPT FILE NAME":
                                 self.expt_file_name = user_input.text
                                 self.expt_file_path_name = os.path.join(self.datapath,self.expt_file_name )

                            elif user_input.label == "Spk(S)":
                                 self.Tone1_Duration = float(user_input.text)
                            elif user_input.label == "Freq(Hz)":
                                 self.Tone1_Freq = float(user_input.text)
                            elif user_input.label == "Vol(0-1)":
                                 self.Tone1_Vol = float(user_input.text)

                            elif user_input.label == "Shck(S)":
                                 self.Shock_Duration = float(user_input.text)
                            elif user_input.label == "V":
                                 self.Shock_V = float(user_input.text)
                            elif "Amps" in user_input.label:
                                 self.Shock_Amp = float(user_input.text)


           # MOUSE UP
            elif (event.type == pygame.MOUSEBUTTONUP ):
                self.NEW_BUTTON = False
                self.LEFT_MOUSE_DOWN = False
                self.RIGHT_MOUSE_DOWN = False
                self.BUTTON_SELECTED = False
                self.LBL_SELECTED = False
                self.LED_SELECTED = False
                self.BOX_SELECTED = False
                self.CORNER_SET = False
                self.DELETE_ITEM = False
                self.CIRC_SELECTED = False
                self.SLIDER_SELECTED = False

                for button in self.buttons: # Check for collision with EXISTING buttons
                    if button.text == "REC":  # Leave REC button down while recording
                        if not self.RECORDING: button.UP_DN = "UP"

                    elif button.text == "R":  # Leave R button down while recording
                        if not self.R_LEVER_EXTENDED: button.UP_DN = "UP"
                    elif button.text == "L":  # Leave R button down while recording
                        if not self.L_LEVER_EXTENDED: button.UP_DN = "UP"
                    elif button.text == "FEED":  # Leave R button down while recording
                        button.UP_DN = "UP"
                        GUIFunctions.FOOD_REWARD_RESET(self)


                    else: # ALL OTHER BUTTONS, NOT REC BUTTON
                        button.UP_DN = "UP"


###########################################################################################################
#  HANDLE BEHAVIORAL CHAMBER EVENTS
###########################################################################################################
    def checkNIDAQEvents(self):
        '''
        CHECK INPUTS FROM BEH CHAMBER
        '''
        if self.NIDAQ_AVAILABLE:
            if self.L_LEVER_EXTENDED or self.R_LEVER_EXTENDED:
                  wasleverPressed = daqHelper.detectPress(self.checkPressLeft, self.checkPressRight)
                  #cur_time = time.perf_counter()
                  self.LEVER_PRESS_TIME = self.cur_time
                  if  wasleverPressed == 'Right':
                        GUIFunctions.log_event(self, self.events,"Lever_Pressed_R",self.cur_time)
                        self.LEVER_PRESSED_R = True
                        print("RIGHT LEVER PRESSED")
                        self.num_R_lever_preses += 1
                        self.levers[1].STATE = "DN"

                  if  wasleverPressed == 'Left':
                        GUIFunctions.log_event(self, self.events,"Lever_Pressed_L",self.cur_time)
                        self.LEVER_PRESSED_L = True
                        print("LEFT LEVER PRESSED")
                        self.num_L_lever_preses += 1
                        self.levers[0].STATE = "DN"

            # nose pokes
            #cur_time = time.perf_counter()
            was_nose_poked_L = daqHelper.checkLeftNosePoke(self.L_nose_poke)

            if was_nose_poked_L:
                print("LEFT Nose Poked")
                self.NOSE_POKE_TIME = self.cur_time
                #events.append("LEFT Nose Poke: " + str(cur_time))
                GUIFunctions.log_event(self, self.events,"Nose_Poke_L",self.cur_time)
                self.NOSE_POKED_L = True
                self.num_L_nose_pokes += 1
                for LED in self.LEDs:
                    if LED.index == 2: # R NOSE POKES
                          LED.ONOFF = "ON"
            else:
                for LED in self.LEDs:
                    if LED.index == 2: # R NOSE POKES
                          LED.ONOFF = "OFF"

            was_nose_poked_R = daqHelper.checkRightNosePoke(self.R_nose_poke)
            if was_nose_poked_R:
                print("Right Nose Poked")
                #events.append("RIGHT Nose Poke: " + str(cur_time))
                GUIFunctions.log_event(self, self.events,"Nose_Poke_R",self.cur_time)
                self.NOSE_POKE_TIME = time.perf_counter()
                self.NOSE_POKED_R = True
                self.num_R_nose_pokes += 1
                for LED in self.LEDs:
                    if LED.index == 3: # R NOSE POKES
                      LED.ONOFF = "ON"
            else:
                for LED in self.LEDs:
                    if LED.index == 3: # R NOSE POKES
                          LED.ONOFF = "OFF"

            # food eaten
            #cur_time = time.perf_counter()
            foodEaten = daqHelper.checkFoodEaten(self.eaten)

            if foodEaten:
                print("Yum!")
                self.num_eaten +=1
                #events.append("Food Eaten: " + str(cur_time))
                GUIFunctions.log_event(self, self.events,"Food_Eaten",self.cur_time)

###########################################################################################################
#  SETUP EXPERIMENT
###########################################################################################################
    def runSetup(self):
        '''
        RUN SETUP
        '''
        #cur_time = time.perf_counter()
        print("SETUPDICT:....................",self.setup,"length: ",len(self.setup),"linenum: ",self.setup_ln_num)
        setupDict = self.setup[self.setup_ln_num]
        key = list(setupDict.keys())[0] # First key in protocolDict
        print ("KEY:.....................",key)
        if key == "":
            self.setup_ln_num +=1
        elif key == "FAN_ON":
           val = str2bool(setupDict[key])
           print("FAN")
           GUIFunctions.FAN_ON_OFF(self, self.events,val,self.cur_time) # {'FAN_ON': True} or {'FAN_ON': False}
           self.setup_ln_num +=1
        elif key == "CAB_LIGHT":
           val = str2bool(setupDict[key])
           print("CAB_LIGHT")
           self.Background_color = GUIFunctions.CAB_LIGHT(self, self.events,val,self.cur_time)
           #CAB_LIGHT(events,val,cur_time)
           self.setup_ln_num +=1
        elif key == "FOOD_LIGHT":
            print("FOOD LIGHT: ",setupDict["FOOD_LIGHT"])
            val = str2bool(setupDict[key])
            self.setup_ln_num +=1
            self.feederBox.fill_color,LEDsONOFF = GUIFunctions.Food_Light_ONOFF (self, self.events,val,self.cur_time)
            self.LEDs[4].ONOFF = LEDsONOFF
            self.LEDs[5].ONOFF = LEDsONOFF
        elif key == "CAMERA":
            print("CAMERA")
            val = str2bool(setupDict[key])
            self.setup_ln_num +=1
            if val:  # TURN CAMERA ON
                if not self.CAMERA_ON: # CAMERA WAS OFF
                    self.CAMERA_ON = True
                    GUIFunctions.log_event(self, self.events,"Camera_ON",self.cur_time)
                    self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'ON', 'PATH_FILE':self.video_file_path_name}
                    GUIFunctions.MyVideo(self)
                else: # CAMERA IS ALREADY ON
                    GUIFunctions.log_event(self, self.events,"Camera is ALREADY ON",self.cur_time)
            else: # TURN CAMERA OFF
                if self.CAMERA_ON: # CAMERA CURRENTLY ON
                    self.CAMERA_ON = False
                    self.RECORDING = False
                    GUIFunctions.log_event(self, self.events,"Camera_OFF",self.cur_time)
                    self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'STOP', 'PATH_FILE':self.video_file_path_name}
        elif key == "REC":
            print ("recording")
            self.RECORDING = True
            val = str2bool(setupDict[key])
            self.setup_ln_num +=1
            if val:  # REC == TRUE.  Remember Camera STATE = (ON,OFF,REC)
                self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'REC', 'PATH_FILE':self.video_file_path_name}
            else:
                self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'ON', 'PATH_FILE':self.video_file_path_name}
        elif key == 'ROI':
            print('setting ROI')
            self.setup_ln_num += 1
            self.vidDict['ROI'] = setupDict[key].split('#')[0]
        elif key == 'FREEZE':
            print('adding freeze')
            self.setup_ln_num += 1
            val = str2bool(setupDict[key])
            self.vidDict['FREEZE'] = val

        if self.setup_ln_num >= len(self.setup):
            self.RUN_SETUP = False

###########################################################################################################
#  RUN EXPERIMENT
###########################################################################################################
    def runExpt(self):
        '''
        RUN EXPERIMENTAL PROTOCOL IF START EXPT BUTTON PRESSED
        '''
        GUIFunctions.FOOD_REWARD_RESET(self) #NOTE: THIS IS SO LOW BIT IS SENT TO FEEDER WITHOUT PAUSING THE PROGRAM
        protocolDict = self.protocol[self.Protocol_ln_num]
        key = list(protocolDict.keys())[0] # First key in protocolDict

        # Tell open ephys to start acquisiton and recording?
        #cur_time = time.perf_counter()

        if key == "":
            self.Protocol_ln_num +=1
        elif key == "FAN_ON":
           val = str2bool(protocolDict[key])
           print("FAN")
           GUIFunctions.FAN_ON_OFF(self, self.events,val,self.cur_time) # {'FAN_ON': True} or {'FAN_ON': False}
           self.Protocol_ln_num +=1

        elif key == "CAB_LIGHT":
           val = str2bool(protocolDict[key])
           print("CAB_LIGHT")
           self.Background_color = GUIFunctions.CAB_LIGHT(self, self.events,val,self.cur_time)
           #CAB_LIGHT(events,val,cur_time)
           self.Protocol_ln_num +=1

        elif "TONE" in key:
            self.Protocol_ln_num +=1
            idx = key[4:]
            print("TONE idx: ",idx)
            if idx == '1':
                 GUIFunctions.PLAY_TONE(self, self.events,"TONE1", self.cur_time)
                 self.TONE_TIME = self.cur_time
            elif idx == '2':
                 GUIFunctions.PLAY_TONE(self, self.events,"TONE2", self.cur_time)
                 self.TONE_TIME = self.cur_time
            self.TONE_ON = True

        elif key == "FOOD_LIGHT":
            val = str2bool(protocolDict[key])
            self.Protocol_ln_num +=1
            self.feederBox.fill_color,LEDsONOFF = GUIFunctions.Food_Light_ONOFF(self, self.events,val, self.cur_time)
            self.LEDs[4].ONOFF = LEDsONOFF
            self.LEDs[5].ONOFF = LEDsONOFF

        elif key  == 'SHOCK':
                 log_event(self.events,"Shock_ON", self.cur_time,("Voltage", str(self.Shock_V),"Amps",str(self.Shock_Amp),"Duration(S)",str(self.Shock_Duration)))
                 self.SHOCK_ON = True

        elif key == "L_CONDITIONING_LIGHT":
            val = str2bool(protocolDict[key])
            self.Protocol_ln_num +=1
            if val:
                GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,True, self.cur_time)
                self.LEDs[0].ONOFF = "ON"
            else:
                GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,False, self.cur_time)
                self.LEDs[0].ONOFF = "OFF"

        elif key == "R_CONDITIONING_LIGHT":
            val = str2bool(protocolDict[key])
            self.Protocol_ln_num +=1

            if val:
                GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,True, self.cur_time)
                self.LEDs[1].ONOFF = "ON"
            else:
                GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,False, self.cur_time)
                self.LEDs[1].ONOFF = "OFF"

        elif key == "CAMERA":
            print("CAMERA")
            val = str2bool(protocolDict[key])
            self.Protocol_ln_num +=1
            if val:  # TURN CAMERA ON
                if not self.CAMERA_ON: # CAMERA WAS OFF
                    self.CAMERA_ON = True
                    GUIFunctions.log_event(self, self.events,"Camera_ON",self.cur_time)
                    self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'ON', 'PATH_FILE':self.video_file_path_name}
                    GUIFunctions.MyVideo(self)
                else: # CAMERA IS ALREADY ON
                    GUIFunctions.log_event(self, self.events,"Camera is ALREADY ON", self.cur_time)
            else: # TURN CAMERA OFF
                if self.CAMERA_ON: # CAMERA CURRENTLY ON
                    self.CAMERA_ON = False
                    self.RECORDING = False
                    GUIFunctions.log_event(self, self.events,"Camera_OFF",self.cur_time)
                    self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'STOP', 'PATH_FILE':self.video_file_path_name}


        elif key == "REC":
            print ("rec")
            self.RECORDING = True
            val = str2bool(protocolDict[key])
            self.Protocol_ln_num +=1
            if val:  # REC == TRUE.  Remember Camera STATE = (ON,OFF,REC)
                self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'REC', 'PATH_FILE':self.video_file_path_name}
            else:
                self.vidDict = {'trial_num' : self.trial_num, 'cur_time':self.cur_time, 'STATE':'ON', 'PATH_FILE':self.video_file_path_name}

        elif "EXTEND_LEVERS" in key:
            if protocolDict[key] == "L_LVR":
                   GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers Extended",True,False,self.cur_time)
            elif protocolDict[key] == "R_LVR":
               GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers Extended",False,True,self.cur_time)
            else:
                val = str2bool(protocolDict[key])
                self.Protocol_ln_num +=1
                if val: # EXTEND_LEVERS == True
                   print ("EXTEND LEVERS")
                   GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers Extended",True,True,self.cur_time)
                   for lever in self.levers:
                         lever.STATE = "OUT"
                   for button in self.buttons:
                        if button.text == "EXTEND": button.text = "RETRACT"
                else: # RETRACT LEVERS (EXTEND_LEVERS == False)
                   print ("RETRACT LEVERS")
                   GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers_Retracted",False,False,self.cur_time)
                   for lever in self.levers:
                        lever.STATE = "IN"
                   for button in self.buttons:
                        if button.text == "RETRACT": button.text = "EXTEND"

        elif "DRAW_IMAGES" in key:
            if self.TOUCHSCREEN_USED:
                self.TSq.put(self.touch_img_files)
                self.Protocol_ln_num +=1

        elif "START_LOOP" in key:
            print("\n.............TRIAL = ",self.trial_num, "LOOP: ", self.loop,"..................")
            self.loop +=1
            self.trial_num +=1
            for user_input in self.user_inputs:
                if user_input.label == "TRIAL":
                        user_input.text = str(self.trial_num)


            self.CONDITONS_NOT_SET = True

            self.loop_start_line_num = self.Protocol_ln_num
            self.Protocol_ln_num +=1
            if "RANDOM" in protocolDict[key]:
                if self.LOOP_FIRST_PASS:
                    intrange = protocolDict[key][7:len(protocolDict[key])-1]
                    print("intrange: ", intrange)
                    a,b = intrange.split(",")
                    print("a,b: ", a,b)
                    self.NUM_LOOPS = random.randint(int(a), int(b))
                    self.LOOP_FIRST_PASS = False
            else:  self.NUM_LOOPS = int(protocolDict[key])
            GUIFunctions.log_event(self, self.events,"LOOPING "+ str(self.NUM_LOOPS)+ " times, TRIAL "+str(self.trial_num),self.cur_time)

        elif "END_LOOP" in key:
            self.num_lines_in_loop = self.Protocol_ln_num - self.loop_start_line_num
            if self.loop  < int(self.NUM_LOOPS):
                self.Protocol_ln_num = self.Protocol_ln_num - self.num_lines_in_loop
                self.VI_index += 1
            else:
                self.Protocol_ln_num +=1
                GUIFunctions.log_event(self, self.events,"END_OF_LOOP",self.cur_time)
                self.loop = 0
                self.LOOP_FIRST_PASS = True
                self.VI_index = 0
            #trial = 0 Do not set here in case there are more than 1 loops

        elif key == "PAUSE":
            try: # WAS A NUMBER
                self.PAUSE_TIME = float(protocolDict["PAUSE"])
            except: # NOT A NUMBER. MUST BE VI_TIMES
                #print(protocolDict["PAUSE"])
                #print(habituation_vi_times)
                if "HABITUATION" in protocolDict["PAUSE"]:
                    self.PAUSE_TIME = self.habituation_vi_times[self.VI_index]
                if "CONDITIONING" in protocolDict["PAUSE"]:
                    self.PAUSE_TIME = self.conditioning_vi_times[self.VI_index]
            if not self.PAUSE_STARTED:
                GUIFunctions.log_event(self, self.events,"PAUSEING FOR "+str(self.PAUSE_TIME)+" sec",self.cur_time)
                self.PAUSE_STARTED = True
                self.pause_start_time = self.cur_time
            else: #PAUSE_STARTED
                time_elapsed = self.cur_time - self.pause_start_time
                if time_elapsed >= self.PAUSE_TIME:
                    self.Protocol_ln_num +=1 #Go to next protocol item
                    self.PAUSE_STARTED = False

        elif key == "CONDITIONS":
            self.runConditions(protocolDict, self.cur_time)

        else:
            print("PROTOCOL ITEM NOT RECOGNIZED",key)

        if self.BAR_PRESS_INDEPENDENT_PROTOCOL: #Running independently of CONDITIONS. Used for conditioning, habituation, extinction, and recall
           #print (cur_time,"VI................", self.VI, (self.VI_start + self.VI))
           if self.cur_time > (self.VI_start + self.VI):
              if self.LEVER_PRESSED_R: # RIGHT LEVER
                 self.VI_start = self.cur_time
                 self.VI = random.randint(0,int(self.var_interval_reward*2))
                 print("new vi", self.VI)
                 GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet",self.cur_time)

        # Clean up vars
        self.LEVER_PRESSED_R = False
        self.LEVER_PRESSED_L = False

        if self.Protocol_ln_num >= len(self.protocol):
           print("Protocol_ln_num: ",self.Protocol_ln_num,"plength: ", len(self.protocol),"\n")
           print("PROTOCOL ENDED")
           print(".................")
           GUIFunctions.log_event(self, self.events,"PROTOCOL ENDED",self.cur_time)
           self.START_EXPT = False
           self.Protocol_ln_num = 0
           self.LEDs[0].ONOFF = "OFF"
           self.LEDs[1].ONOFF = "OFF"
           GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)
           GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)

           # TEll open ephys to stop acquistion and recording?
           self.snd.send(self.snd.STOP_ACQ)
           self.snd.send(self.snd.STOP_REC)

           if self.TOUCHSCREEN_USED:
               self.TSq.put('')
               self.TOUCHSCREEN_USED = False

######################################################################################################
    def runConditions(self, protocolDict, cur_time):
        '''
        RUNS CONDITIONS
        '''
        num_conditions = len(self.conditions)
        if protocolDict["CONDITIONS"] == "RANDOM": #Or SEQUENTIAL or a particular condition number
            self.choose_cond = random.randint(0,num_conditions-1)
        elif  protocolDict["CONDITIONS"] == "SEQUENTIAL":
            self.condition_idx += 1
            self.choose_cond = self.condition_idx
        else: # a particual sequence number
            cond_num = int(protocolDict["CONDITIONS"])
            self.choose_cond = cond_num

        ###############################
        # SET CONDITONS HERE
        ###############################
        if self.CONDITONS_NOT_SET:
            self.HAS_ALREADY_RESPONDED = False
            self.CONDITONS_NOT_SET = False
            self.cond = self.conditions[self.choose_cond]
            GUIFunctions.log_event(self, self.events,"CONDITION["+str(self.choose_cond)+"]",self.cur_time)
            COND_MAX_TIME = float(self.cond["MAX_TIME"])
            reset = self.cond["RESET"]

            print("\n\nCONDTION")
            print(self.cond)
            #condkey = list(condDict.keys())[0] # First key in condDict


            # SET CONDITIONS
            # SET LEVERS WHEN IN CONDITIONS
            try:
                if self.cond['EXTEND_L_LEVER'] and self.cond['EXTEND_R_LEVER']:
                    daqHelper.EXTEND_LEVERS(self.events,"Levers Extended",True,True,self.cur_time)

                elif self.cond['EXTEND_L_LEVER']:
                    daqHelper.EXTEND_LEVERS(self.events,"L Lever Extended",True,False,self.cur_time)

                elif self.cond['EXTEND_R_LEVER']:
                    daqHelper.EXTEND_LEVERS(self.events,"R Lever Extended",False,True,self.cur_time)

                else:
                    daqHelper.EXTEND_LEVERS(self.events,"Levers Retracted",False,False,self.cur_time)

            except:
                pass
            # SET CONDITIONING LIGHTS
            try: # if conditionaing lights are used
                if self.cond['L_CONDITION_LT']: # Left_Conditioning lit 1/0
                    GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,True,self.cur_time)
                    self.LEDs[0].ONOFF = "ON"
                else:
                    GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)
                    self.LEDs[0].ONOFF = "OFF"


                if self.cond['R_CONDITION_LT']: # Left_Conditioning lit 1/0
                    GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,True,self.cur_time)
                    self.LEDs[1].ONOFF = "ON"
                else:
                    GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)
                    self.LEDs[1].ONOFF = "OFF"
            except: # Conditionaing lights not used, Use Touch screen instead
                pass

        # Wait for response
        if not self.CONDITION_STARTED: #
           self.condition_start_time = self.cur_time
           self.CONDITION_STARTED = True
           self.TIME_IS_UP = False
           self.CORRECT = False
           self.WRONG = False
           self.NO_ACTION_TAKEN = False

        else: # CONDITION STARTED
           cond_time_elapsed = self.cur_time - self.condition_start_time

           if self.LEVER_PRESSED_L: # LEFT LEVER
               GUIFunctions.log_event(self, self.events,"Left_Lever_Pressed",self.cur_time)
               if not self.HAS_ALREADY_RESPONDED:# Prevents rewarding for multiple presses
                   if self.cond['DES_L_LEVER_PRESS']:
                       GUIFunctions.log_event(self, self.events,"CORRECT Response",self.cur_time)
                       self.CORRECT = True
                       if self.cond["RESET"] == "ON_RESPONSE":
                          self.CONDITION_STARTED = False
                   else:
                       self.WRONG = True
                       GUIFunctions.log_event(self, self.events,"WRONG Response",self.cur_time)
                   self.HAS_ALREADY_RESPONDED = True
                   GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)
                   GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)
                   self.LEDs[0].ONOFF = "OFF"
                   self.LEDs[1].ONOFF = "OFF"

           if self.LEVER_PRESSED_R: # RIGHT LEVER
               GUIFunctions.log_event(self, self.events,"Right_Lever_Pressed",self.cur_time)
               if not self.HAS_ALREADY_RESPONDED:# Prevents rewarding for multiple presses
                   print("cond['DES_R_LEVER_PRESS']",self.cond['DES_R_LEVER_PRESS'])
                   if self.cond['DES_R_LEVER_PRESS']:
                       GUIFunctions.log_event(self, self.events,"CORRECT Response",self.cur_time)
                       self.CORRECT = True
                       if self.cond["RESET"] == "ON_RESPONSE":
                          self.CONDITION_STARTED = False
                   else:
                       self.WRONG = True
                       GUIFunctions.log_event(self, self.events,"WRONG Response",self.cur_time)
                   self.HAS_ALREADY_RESPONDED = True
                   self.LEDs[0].ONOFF = "OFF"
                   self.LEDs[1].ONOFF = "OFF"
                   GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)
                   GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)

           if self.TOUCHSCREEN_USED:
               if not self.TSBack_q.empty():
                   touchMsg = self.TSBack_q.get()
                   GUIFunctions.log_event(self, self.events,touchMsg['picture'] + " Pressed " + str(touchMsg['XY']) , self.cur_time)
                   if touchMsg['picture'] == 'missed':
                       print('missed')
                   elif not self.HAS_ALREADY_RESPONDED:
                       self.HAS_ALREADY_RESPONDED = True
                       for i in range(len(self.touch_img_files)):
                           for key in self.touch_img_files[i].keys():
                               if key in touchMsg['picture']:
                                   if i == 0 and self.cond["DES_IMG1_PRESSP"]:
                                       GUIFunctions.log_event(self, self.events,"CORRECT Response",self.cur_time)
                                       self.CORRECT = True
                                       break
                                   elif i == 1 and self.cond["DES_IMG2_PRESSP"]:
                                       GUIFunctions.log_event(self, self.events,"CORRECT Response",self.cur_time)
                                       self.CORRECT = True
                                       break
                       if not self.CORRECT:
                           self.WRONG = True
                           GUIFunctions.log_event(self, self.events,"WRONG Response",self.cur_time)

           if self.cond["RESET"] == "FIXED":
               if cond_time_elapsed >= float(self.cond["MAX_TIME"]): # Time is up
                  self.CONDITION_STARTED = False
                  if not self.WRONG and not self.CORRECT:
                      self.NO_ACTION_TAKEN = True
                      GUIFunctions.log_event(self, self.events,"END_OF_TRIAL: NO_ACTION_TAKEN",self.cur_time)
                  self.TIME_IS_UP = True

           if self.cond["RESET"] == "ON_RESPONSE":
               #print (cond["Reset"])
               if self.WRONG or self.CORRECT: # A response was given
                   self.CONDITION_STARTED = False  # Time is up
                   GUIFunctions.log_event(self, self.events,"END_OF_TRIAL",self.cur_time)
                   self.TIME_IS_UP = True
               if cond_time_elapsed >= float(self.cond["MAX_TIME"]): # Time is up
                  self.CONDITION_STARTED = False
                  if not self.WRONG and not self.CORRECT:
                      self.NO_ACTION_TAKEN = True
                      GUIFunctions.log_event(self, self.events,"END_OF_TRIAL: NO_ACTION_TAKEN",self.cur_time)
                  self.TIME_IS_UP = True

           if self.cond['RESET'] == "VI":
               pass

           if self.TIME_IS_UP:
               # SET OUTCOMES
               if self.CORRECT:
                  outcome = self.cond['CORRECT'].upper()  # Outcome for correct response(in Expt File)
                  print("Correct")
               elif self.WRONG:
                  outcome = self.cond['WRONG'].upper()    # Outcome for wrong response(in Expt File)
                  print("Wrong")
               else:
                  print("No Action Taken")
                  outcome = self.cond['NO_ACTION'].upper()# Outcome for No_Action taken(in Expt File)

               # OUTCOMES

               if 'PELLET' in outcome:
                   if len(outcome)<=6: # Just 'PELLET'
                       GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet",self.cur_time)
                   else: #"PELLET##"
                       probability_of_reward = float(outcome[6:])
                       if random.random()*100 <= probability_of_reward:
                           GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet w"+str(probability_of_reward)+ "% probability", self.cur_time)
                       else:
                           GUIFunctions.log_event(self, self.events,"Reward NOT given w " + str(probability_of_reward)+"% probability", self.cur_time)


               elif 'TONE' in outcome:
                   idx = outcome[4:]
                   if idx == '1':
                      GUIFunctions.PLAY_TONE(self, self.events,"TONE1",self.cur_time)
                      self.TONE_TIME = self.cur_time
                   elif idx == '2':
                      GUIFunctions.PLAY_TONE(self, self.events,"TONE2",self.cur_time)
                      self.TONE_TIME = self.cur_time

               elif outcome == 'SHOCK':
                    GUIFunctions.log_event(self, self.events,"Shock_ON",self.cur_time,("Voltage", str(self.Shock_V),"Amps",str(self.Shock_Amp),"Duration(S)",str(self.Shock_Duration)))
                    self.SHOCK_ON = True
               else: #outcome == 'NONE'
                   GUIFunctions.log_event(self, self.events,"NONE",self.cur_time)
                   print("Outcome = NONE")
               self.TIME_IS_UP = False
               self.CONDITION_STARTED = False
               self.Protocol_ln_num +=1

if __name__ == "__main__":
    openWhisker()
    beh = BEH_GUI(NIDAQ_AVAILABLE)
    beh.BehavioralChamber()

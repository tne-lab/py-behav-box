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
import pygame

import math, random
import numpy as np
import zmq
import json
#from NIDAQ_GUI_elements import *
from RESOURCES.GUI_elements_by_flav import *
#import daqHelper
#import daqAPI
#NIDAQ_AVAILABLE = True
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
import win32gui, win32con




class BEH_GUI():
    def __init__(self, NIDAQ_AVAILABLE):
        self.NIDAQ_AVAILABLE = NIDAQ_AVAILABLE
        self.setGlobals()
        self.computer = os.environ['COMPUTERNAME']
        random.seed()
        #self.load_expt_file()
        self.setupGUI()

    from setGlobals import setGlobals
    from loadProtocol import load_expt_file, create_expt_file_copy, create_files
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
                if self.ROIstr == "":
                    try:  # Get ROI value if it exists
                        self.ROIstr = backDict['ROI']
                        if self.ROIstr != "":
                            print(self.ROIstr)
                            newROIstr = self.ROIstr.replace(",",";")
                            print(newROIstr)
                            GUIFunctions.log_event(self, self.events,"ROI:",self.cur_time,(newROIstr + ",( x; y; width; height)"))
                            print("ROI",self.ROIstr," x; y; width; hieght")
                            self.ROI_RECEIVED = True
                    except:
                        pass


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
            GUIFunctions.updateVideoQ(self)
########################################################################################
    def drawScreen(self):
        self.cur_time = time.perf_counter()-self.Experiment_Start_time
        #print("cur_time : Experiment_Start_time-->",self.cur_time, self.Experiment_Start_time)
        #######################
        # DRAW SCREEN AND GUI ELEMENTS
        #######################
        self.myscreen.fill(self.Background_color)
        self.myscreen.blit(self.TNElogo,(400,5))
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
                if self.START_EXPT: info.text = [str(round(self.cur_time/60.0,3))]
                #else: info.text = ['0.000']
            elif info.label == "EVENT LOG":
                lines_in_txt = len(self.events)
                y_per_line = int(self.sliders[0].slotL / 14.0)
                if lines_in_txt > 14: # 14 lines fit in window
                    ##########################################################
                    # SLIDER:
                    #               NOTE only 14 text lines fit inside window
                    ##########################################################
                    slider_Button_ht = int((14.0/float(lines_in_txt)) * self.sliders[0].slotL) # portion of SlotL
                    # Prevent slider Button from getting too small
                    if slider_Button_ht <= 10:
                        self.sliders[0].bh = 10
                    else:
                        self.sliders[0].bh = slider_Button_ht

                    # Set Slider location
                    self.sliders[0].sliderY = self.new_slider_y #+ self.start_line * self.y_per_line
                    #self.sliders[0].sliderY = self.new_slider_y + (self.sliders[0].slotL - self.sliders[0].bh) - self.start_line * self.y_per_line



                    self.sliders[0].draw()
                    #info.text = self.events[self.start_line:self.start_line+14]
                    # Proportion of events to display
                    self.start_line = int(len(self.events) * (self.sliders[0].sliderY/(self.sliders[0].slotL  -  self.sliders[0].bh) ))
                    #self.start_line = int(len(self.events) * (self.sliders[0].sliderY-self.sliders[0].bh)/(self.sliders[0].slotL ))
                    info.text = self.events[self.start_line:self.start_line+14]


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
              # Note: This just draws the speeker on GUI. Tone turned on during GUI mousedown events.
              if (self.cur_time - self.TONE_TIME) > float(self.Tone1_Duration): # seconds
                  #print("TONE OFF")
                  self.TONE_ON = False
                  if "EPHYS-1" in self.computer:
                      self.low_tone.sendDBit(False)
                  GUIFunctions.log_event(self, self.events,"Tone_OFF",self.cur_time)

        # DRAW SHOCK LIGHTNING
        self.shock = GUIFunctions.draw_lighting(self.myscreen, self.SHOCK_ON, 248,150,1,(255,255,0),2)
        if self.SHOCK_ON:
              if (self.cur_time - self.SHOCK_TIME) <= self.Shock_Duration: # seconds
                  self.apply_shock.sendDBit(True)
              else:
                  self.SHOCK_ON = False
                  self.apply_shock.sendDBit(False)
                  #print("SHOCK OFF")
                  GUIFunctions.log_event(self, self.events,"Shock_OFF",self.cur_time)


        # DRAW CAMERA
        #    Note:                 draw_camera(self.myscreen,fill_color, ON_OFF, REC, x, y, w,h, linew)
        self.camera = GUIFunctions.draw_camera(self.myscreen, (100,100,100),self.CAMERA_ON,self.RECORDING,235, 245, 30,20, 2)

        # GUI TOUCH SCREEN
        for x,y in self.background_hits:
            #print(x,y)
            draw_plus_sign(self.myscreen, x + 40, y +320, 5, (255,0,0) ) # (40,320) is top left of gui touchscreen, 1/4 is the gui scale factor                      self.touch_time = cur_time

        for x,y in self.correct_img_hits:
            draw_plus_sign(self.myscreen, x + 40, y +320, 5, (0,255,0) ) # (40,320) is top left of gui touchscreen, 1/4 is the gui scale factor                      self.touch_time = cur_time

        for x,y in self.wrong_img_hits:
            draw_plus_sign(self.myscreen, x + 40, y +320, 5, (0,0,255) ) # (40,320) is top left of gui touchscreen, 1/4 is the gui scale factor                      self.touch_time = cur_time

        try:
            #print(self.touchImgCoords)
            for coords in self.touchImgCoords:
                #print (coords)
                x,y = int(coords[0]/4 + 40), int(coords[1]/4 + 320)   # NOTE: 40,320 is top-left of gui touch representation. 1/4 is its scale
                pygame.draw.rect(self.myscreen, (0,0,255) , (x,y,60,60),  1)


        except: pass

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
                        #self.start_line = int(new_slider_y/self.y_per_line)
                        #print("new_slider_y: ",new_slider_y, "start_line: ",self.start_line)

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

                elif event.button == 4:  #Wheel roll UP
                     self.MOUSE_WHEEL_SCROLL_UP = True
                     self.new_slider_y = self.sliders[0].sliderY - (1 + int( self.sliders[0].slotL/self.sliders[0].bh))
                     # Limit possible slider position
                     if self.new_slider_y <= 0: self.new_slider_y = 0
                     elif self.new_slider_y >= self.sliders[0].slotL-self.sliders[0].bh:
                         self.new_slider_y = self.sliders[0].slotL-self.sliders[0].bh
                     #print("SCROLLING UP",self.sliders[0].sliderY )

                elif event.button == 5: #Wheel roll Down
                     self.MOUSE_WHEEL_SCROLL_DN = True
                     self.new_slider_y = self.sliders[0].sliderY + (1 + int( self.sliders[0].slotL/self.sliders[0].bh))
                     # Limit possible slider position
                     if self.new_slider_y >= self.sliders[0].slotL - self.sliders[0].bh:
                       self.new_slider_y = self.sliders[0].slotL - self.sliders[0].bh
                     #print("SCROLLING DOWN",self.sliders[0].sliderY )


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
                                          if self.RECORDING: #STOP RECORDING BUT KEEP CAMERA ON. # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
                                                self.RECORDING = False  #KEEP CAMERA ON, JUST STOP RECORDING
                                                GUIFunctions.log_event(self, self.events,"STOP_RECORDING_by_GUI",self.cur_time)
                                                self.vidSTATE= 'REC_VID'
                                                button.UP_DN = "UP"
                                          else:
                                                self.RECORDING = True
                                                button.UP_DN = "DN"
                                                GUIFunctions.log_event(self, self.events,"START_RECORDING_by_GUI",self.cur_time)
                                                self.vidSTATE = 'REC_VID'


                                    else:
                                          print("CAMERA NOT ON!")

                               #######################################
                               #
                               #   LOAD EXPERIMENTAL PROTOCOL FILE
                               #
                               #######################################
                               elif button.text == "LOAD FILE":
                                    self.RUN_SETUP = False
                                    self.START_EXPT = False
                                    button.UP_DN = "DN"
                                    self.events = []
                                    #print("LOADING EXPT FILE: in BehGUI_Main ", self.expt_file_path_name)
                                    self.EXPT_FILE_LOADED = self.load_expt_file()

                                    if self.EXPT_FILE_LOADED:
                                        print("\n###########################")
                                        print("#   EXPT FILE LOADED!!    #")
                                        print("###########################")
                                        self.EXPT_FILE_LOADED = True


                                        win32gui.EnumWindows(GUIFunctions.lookForProgram, 'Open Ephys GUI')
                                        if self.USING_OPEN_EPHYS:
                                            if not GUIFunctions.IsOpenEphysRunning:
                                                programName = 'Open Ephys GUI'
                                                self.computer = os.environ['COMPUTERNAME']
                                                print("USING COMPUTER (in GUIfunctions): ",self.computer)
                                                oe = self.open_ephys_path

                                                window = subprocess.Popen(oe)# # doesn't capture output
                                                time.sleep(2)
                                                win32gui.EnumWindows(GUIFunctions.lookForProgram, programName)
                                            #except:
                                            #    print("Could not start Open Ephys")
                                            else: print("Open Ephysis already RUNNING")
                                            print(".............................................")


                                        #GUIFunctions.log_event(self, self.events,"EXPT FILE LOADED",self.cur_time)
                                        if len(self.setup) > 0:
                                            self.RUN_SETUP = True
                                            self.setup_ln_num = 0
                                            self.setupGUI()
                               #######################################
                               #
                               #   START EXPERIMENT
                               #
                               #######################################
                               elif button.text == "START EXPT":
                                    self.setup_ln_num = 0
                                    if self.EXPT_FILE_LOADED:
                                        button.UP_DN = "DN"
                                        #if self.EXPT_FILE_LOADED:
                                        if self.Subject == "" or "?" in self.Subject or self.Subject == " " or len(self.Subject) == 0 :
                                            GUIFunctions.log_event(self, self.events,"Check SUBJECT  and EXPT name!!!!",self.cur_time)
                                            print('SUBJECT = "" or "?" or same as last time')
                                            # HIGHLIGHT USER INPUT BOXES
                                            for user_input in self.user_inputs:
                                                if user_input.label == "EXPT":
                                                     user_input.border_color = (255,0,0)
                                                elif user_input.label == "SUBJECT":
                                                     user_input.border_color = (255,0,0)

                                        if self.NAME_OR_SUBJ_CHANGED :  # READY TO GO!!!
                                            self.Expt_Count +=1
                                            self.create_files()
                                            self.create_expt_file_copy()
                                            self.NAME_OR_SUBJ_CHANGED = False
                                            print("EXPT FILE COPY UPDATED!!!!")
                                            # GOOD TO GO!
                                            print("EXPT STARTED!")
                                            self.Protocol_ln_num = 0
                                            self.trial_num = 0
                                            for user_input in self.user_inputs:
                                                if user_input.label == "EXPT":
                                                   user_input.text = str(self.Expt_Name)+str(self.Expt_Count)
                                            self.RUN_SETUP = True
                                            GUIFunctions.log_event(self, self.events,"EXPT STARTED USING " + self.expt_file_path_name_COPY,self.cur_time)
                                            button.text = "STOP EXPT"
                                            if self.TOUCHSCREEN_USED: GUIFunctions.StartTouchScreen(self)

                                    else:
                                        self.EXPT_FILE_LOADED = False
                                        print("HUMPH! COULD NOT LOAD EXPT FILE (on button press)")
                                        GUIFunctions.log_event(self, self.events,"Expt File name or path DOES NOT EXIST",self.cur_time)

                               #######################################
                               #
                               #   STOP EXPERIMENT
                               #
                               #######################################
                               elif button.text == "STOP EXPT":
                                    button.text = "START EXPT"
                                    self.START_EXPT = False
                                    print("BUTTON cur_time : Experiment_Start_time-->",self.cur_time, self.Experiment_Start_time)
                                    self.end_expt()



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
                            #print ("LED ID: ",idx)
                            if LED.ONOFF == "OFF": # WAS OFF
                                LED.ONOFF = "ON"   # NOW ON
                                if   LED.index == 0: # LEFT CONDITION LIGHT
                                    GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,True,self.cur_time)
                                elif LED.index == 1: # RIGHT CONDITION LIGHT
                                    GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,True,self.cur_time)

                                # NOSE POKES
                                elif LED.index == 2 or LED.index == 3: # NOSE POKES
                                   if LED.index == 2: self.NOSE_POKED_L = True
                                   elif LED.index == 3: self.NOSE_POKED_R = True
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
                          print("TONE1 DURATION: ", self.Tone1_Duration)
                          if "EPHYS-2" in self.computer:
                             self.GUIFunctions.PLAY_TONE(self, self.events,"TONE1",self.cur_time) #using computer speeker
                          elif "EPHYS-1" in self.computer:
                             self.GUIFunctions.PLAY_TONE_LAF(self, self.events,"TONE1",self.cur_time) #using computer speeker


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

                          #print("SHOCK PRESSED")

                    # CAMERA PRESSED
                    if self.camera.collidepoint(cur_x,cur_y):
                          if self.CAMERA_ON: #CAMERAL ALREWADY ON, TURN CAMERA OFF.  # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
                                self.CAMERA_ON = False
                                self.RECORDING = False
                                GUIFunctions.log_event(self, self.events,"Camera_OFF",self.cur_time)
                                #print("CAMERA OFF")
                                self.vidSTATE = 'OFF'

                          else: #TURN CAMERA ON # NOTE: STATE = (ON,OFF,REC, START_EXPT,STOP_EXPT)
                                self.CAMERA_ON = True
                                GUIFunctions.log_event(self, self.events,"Camera_ON",self.cur_time)
                                #print("CAMERA ON")
                                self.vidSTATE = 'ON'
                                GUIFunctions.MyVideo(self)

                    # USER KEYBOARD INPUTS
                    for user_input in self.user_inputs:
                        if user_input.rect.collidepoint(cur_x,cur_y):
                            user_input.get_key_input()
                            if user_input.label == "EXPT":
                                 self.Expt_Name=user_input.text
                                 self.NAME_OR_SUBJ_CHANGED = True
                            elif user_input.label == "SUBJECT":
                                 self.Subject = user_input.text
                                 self.NAME_OR_SUBJ_CHANGED = True
                                 # RESET ROUGH EXPT START TIME FOR NEW DIRECTORY NAME
                                 self.exptTime = time.strftime("%H-%M")
                            elif user_input.label == "TRIAL":
                                 self.trial_num =  user_input.text
                            elif user_input.label == "EXPT PATH":
                                 self.datapath = user_input.text
                            elif user_input.label == "EXPT FILE NAME":
                                 self.expt_file_name = GUIFunctions.choose_file()
                                 self.expt_file_path_name = os.path.join(self.protocolpath,self.expt_file_name )
                                 print ("File selected: in BehGUI main",self.expt_file_name,self.expt_file_path_name)
                                 if self.expt_file_name == '':
                                     self.expt_file_name = user_input.text
                                     self.expt_file_path_name = os.path.join(self.datapath,self.expt_file_name )
                                     print ("File selected: in BehGUI main2",self.expt_file_name,self.expt_file_path_name)
                            elif user_input.label == "Spk(S)":
                                try:    self.Tone1_Duration = float(user_input.text)
                                except: self.Tone1_Duration = ''
                            elif user_input.label == "Freq(Hz)":
                                try:    self.Tone1_Freq = float(user_input.text)
                                except: self.Tone1_Freq = ''
                            elif user_input.label == "Vol(0-1)":
                                try:    self.Tone1_Vol = float(user_input.text)
                                except: self.Tone1_Vol = ''

                            elif user_input.label == "Shck(S)":
                                try:    self.Shock_Duration = float(user_input.text)
                                except: self.Shock_Duration = ''
                            elif user_input.label == "V":
                                try:    self.Shock_V = float(user_input.text)
                                except: self.Shock_V = ''
                            elif "Amps" in user_input.label:
                                try:    self.Shock_Amp = float(user_input.text)
                                except: self.Shock_Amp = ''

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
                        #print("RIGHT LEVER PRESSED")
                        self.num_R_lever_preses += 1
                        self.levers[1].STATE = "DN"

                  if  wasleverPressed == 'Left':
                        GUIFunctions.log_event(self, self.events,"Lever_Pressed_L",self.cur_time)
                        self.LEVER_PRESSED_L = True
                        #print("LEFT LEVER PRESSED")
                        self.num_L_lever_preses += 1
                        self.levers[0].STATE = "DN"

            # nose pokes
            #cur_time = time.perf_counter()
            was_nose_poked_L = daqHelper.checkLeftNosePoke(self.L_nose_poke)

            if was_nose_poked_L:
                #print("LEFT Nose Poked")
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
                #print("Right Nose Poked")
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
                self.num_eaten +=1
                #events.append("Food Eaten: " + str(cur_time))
                GUIFunctions.log_event(self, self.events,"Food_Eaten",self.cur_time)
                print("Yum!")

###########################################################################################################
#  SETUP EXPERIMENT
###########################################################################################################
    def runSetup(self):
        '''
        RUN SETUP
        '''
        #cur_time = time.perf_counter()
        if self.setup_ln_num < len(self.setup):
            print("SETUPDICT:....................",self.setup,"length: ",len(self.setup),"linenum: ",self.setup_ln_num)

            setupDict = self.setup[self.setup_ln_num]
            key = list(setupDict.keys())[0] # First key in protocolDict
            #print ("KEY:.....................",key)
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
                print("CAMERA\n")
                val = str2bool(setupDict["CAMERA"])
                self.setup_ln_num +=1
                if val:  # TURN CAMERA ON.     # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
                    if not self.CAMERA_ON: # CAMERA WAS OFF
                        self.CAMERA_ON = True
                        GUIFunctions.log_event(self, self.events,"Camera_ON",self.cur_time)
                        self.vidSTATE = 'ON'
                        GUIFunctions.updateVideoQ(self)
                        GUIFunctions.MyVideo(self)
                    else: # CAMERA IS ALREADY ON
                        GUIFunctions.log_event(self, self.events,"Camera is ALREADY ON",self.cur_time)
                else: # TURN CAMERA OFF
                    if self.CAMERA_ON: # CAMERA CURRENTLY ON
                        self.CAMERA_ON = False
                        self.RECORDING = False
                        GUIFunctions.log_event(self, self.events,"Camera_OFF",self.cur_time)
                        self.vidSTATE = 'OFF'


            elif key == "REC":
                print ("recording ....")
                self.RECORDING = True
                val = str2bool(setupDict[key])
                self.setup_ln_num +=1
                if val:  # REC == TRUE.  Remember Camera NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
                    #self.snd.send(self.snd.START_ACQ) # OPEN_EPHYS
                    #self.snd.send(self.snd.START_REC) # OPEN_EPHYS
                    self.vidSTATE = 'REC_VID'
                    if self.CAMERA_ON:
                        print("\nFREEZE DETECTION ENABLED")
                        print(self.ROI)
                        self.vidROI = self.ROI
                        print("\nSelf.ROI: ",self.ROI,"\n")
                else:  # REC == False.  Remember Camera  NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT), so KEEP CAMERA ON, JUST STOP RECORDING
                    self.vidSTATE = 'REC_STOP'
                    print("\nREC = False, Self.ROI: ",self.ROI,"\n")

            elif "EXTEND_LEVERS" in key:
                self.setup_ln_num +=1
                if setupDict[key] == "L_LVR":
                       GUIFunctions.EXTEND_LEVERS(self, self.events,"Left Lever Extended",True,False,self.cur_time)
                elif setupDict[key] == "R_LVR":
                   GUIFunctions.EXTEND_LEVERS(self, self.events,"Right Lever Extended",False,True,self.cur_time)
                else:
                    val = str2bool(setupDict[key])
                    if val: # EXTEND_LEVERS == True
                       print ("LEVERS EXTENDED")
                       GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers Extended",True,True,self.cur_time)
                       for lever in self.levers:
                             lever.STATE = "OUT"
                       for button in self.buttons:
                            if button.text == "EXTEND": button.text = "RETRACT"
                    else: # RETRACT LEVERS (EXTEND_LEVERS == False)
                       #print ("RETRACT LEVERS")
                       GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers_Retracted",False,False,self.cur_time)
                       for lever in self.levers:
                            lever.STATE = "IN"
                       for button in self.buttons:
                            if button.text == "RETRACT": button.text = "EXTEND"


            elif "MAX_EXPT_TIME" in key:
                self.setup_ln_num +=1
                self.MAX_EXPT_TIME = float(setupDict["MAX_EXPT_TIME"])
                print("Max Expt Time :", self.MAX_EXPT_TIME * 60.0, " sec")

        else:
            setup_done = False
            if self.CAMERA_ON and self.ROI == 'GENERATE':
                if self.ROI_RECEIVED:
                    setup_done = True
                    print('ROI recv', self.ROIstr)
            else:
                setup_done = True
                print('no roi')

            if setup_done:
                self.setup_ln_num = 0
                self.RUN_SETUP = False
                if  self.BAR_PRESS_INDEPENDENT_PROTOCOL:
                    # NOTE: THIS IS USED IF REWARDING FOR BAR PRESS (AFTER VI) IS THE ONLY CONDITION (HABITUATION AND CONDITIONING ARE RUNNING CONCURRENTLY)
                    if self.VI_REWARDING:
                        self.VI_start = 0.0 #self.cur_time
                        self.VI = random.randint(0,int(self.var_interval_reward*2))
                        GUIFunctions.log_event(self, self.events,"New VI: " + str(self.VI),self.cur_time)
                        #print("VI.......................", self.VI)
                    if self.BAR_PRESS_TRAINING:
                        pass

            ##################################
            #
            # RESET EXPT TIMER
            #
            ##################################
            #self.events = []

                self.cur_time = time.perf_counter()
                self.Experiment_Start_time = self.cur_time
                self.cur_time = self.cur_time-self.Experiment_Start_time
                self.TPM_start_time = self.cur_time #Screen TOUCHES per Min start time
                self.START_EXPT = True
                self.vidSTATE = 'START_EXPT'  # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
                print("BUTTON cur_time : Experiment_Start_time-->",self.cur_time, self.Experiment_Start_time)
                for LED in self.LEDs: # Look for EXPT STARTED LED
                  if LED.index == 6: # Expt Started light
                      LED.ONOFF = "ON"
###########################################################################################################
#  RUN EXPERIMENT
###########################################################################################################
    def runExpt(self):
        '''
        RUN EXPERIMENTAL PROTOCOL IF START EXPT BUTTON PRESSED
        '''
       # GUIFunctions.FOOD_REWARD_RESET(self) #NOTE: THIS IS SO LOW BIT IS SENT TO FEEDER WITHOUT PAUSING THE PROGRAM
        protocolDict = self.protocol[self.Protocol_ln_num]
        key = list(protocolDict.keys())[0] # First key in protocolDict
        # Tell open ephys to start acquisiton and recording?
        #cur_time = time.perf_counter()

        if key == "":
            self.Protocol_ln_num +=1
        elif key == "FAN_ON":
           val = str2bool(protocolDict[key])
           #print("FAN")
           GUIFunctions.FAN_ON_OFF(self, self.events,val,self.cur_time) # {'FAN_ON': True} or {'FAN_ON': False}
           self.Protocol_ln_num +=1

        elif key == "CAB_LIGHT":
           val = str2bool(protocolDict[key])
           #print("CAB_LIGHT")
           self.Background_color = GUIFunctions.CAB_LIGHT(self, self.events,val,self.cur_time)
           #CAB_LIGHT(events,val,cur_time)
           self.Protocol_ln_num +=1

        elif "TONE" in key:
            self.Protocol_ln_num +=1
            idx = key[4:]
            #print("TONE idx: ",idx)
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
            GUIFunctions.log_event(self, self.events,"Shock_ON", self.cur_time,("Voltage", str(self.Shock_V),"Amps",str(self.Shock_Amp),"Duration(S)",str(self.Shock_Duration)))
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
            #print("CAMERA")
            val = str2bool(protocolDict[key])
            self.Protocol_ln_num +=1
            if val:  # TURN CAMERA ON
                if not self.CAMERA_ON: # CAMERA WAS OFF
                    self.CAMERA_ON = True
                    GUIFunctions.log_event(self, self.events,"Camera_ON",self.cur_time)
                    self.vidSTATE = 'ON'
                    GUIFunctions.updateVideoQ(self)
                                    # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
                    GUIFunctions.MyVideo(self)
                else: # CAMERA IS ALREADY ON
                    GUIFunctions.log_event(self, self.events,"Camera is ALREADY ON", self.cur_time)
            else: # TURN CAMERA OFF
                if self.CAMERA_ON: # CAMERA CURRENTLY ON
                    self.CAMERA_ON = False
                    self.RECORDING = False
                    GUIFunctions.log_event(self, self.events,"Camera_OFF",self.cur_time)
                    self.vidSTATE = 'OFF'  # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)

        elif key == "REC": ## NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
            #print ("rec")
            self.RECORDING = True
            val = str2bool(protocolDict[key])
            self.Protocol_ln_num +=1
            if val:  # REC == TRUE.  Remember Camera STATE = (ON,OFF,REC, START_EXPT,STOP_EXPT)
                self.vidSTATE = 'REC_VID'
            else:  # KEEP CAMERA ON, JUST STOP RECORDING
                self.vidSTATE = 'REC_STOP'

        elif "EXTEND_LEVERS" in key:
            self.Protocol_ln_num +=1
            if protocolDict[key] == "L_LVR":
                   GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers Extended",True,False,self.cur_time)
            elif protocolDict[key] == "R_LVR":
               GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers Extended",False,True,self.cur_time)
            else:
                val = str2bool(protocolDict[key])
                if val: # EXTEND_LEVERS == True
                   #print ("EXTEND LEVERS")
                   GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers Extended",True,True,self.cur_time)
                   for lever in self.levers:
                         lever.STATE = "OUT"
                   for button in self.buttons:
                        if button.text == "EXTEND": button.text = "RETRACT"
                else: # RETRACT LEVERS (EXTEND_LEVERS == False)
                   #print ("RETRACT LEVERS")
                   GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers_Retracted",False,False,self.cur_time)
                   for lever in self.levers:
                        lever.STATE = "IN"
                   for button in self.buttons:
                        if button.text == "RETRACT": button.text = "EXTEND"
        ##############################
        #  TOUCHSCREEN  in RUNEXPT (DRAWS IMAGES)
        ##############################
        elif "DRAW_IMAGES" in key: # IF USING TOUCHSCREEN
            if self.TOUCHSCREEN_USED:
                if self.RANDOM_IMG_COORDS:
                    placementList = [1] # 1 1mage, random locations
                    self.touchImgCoords=(random.randint(0,784),random.randint(0,278))
                    print(placementList, self.touchImgCoords)

                    # NOTE: The above assumes pics are 240 x 240 and screen is 1024 x (768 - deadzone) = 1024 x 518,
                    #       hence  farthest bottom-right is 784 x 278 (1024-240 x 518-240)
                    imgList = {}
                    for key in self.touchImgs.keys():

                        imgList[key] = self.touchImgCoords #places images
                        self.TSq.put(imgList)
                        self.Protocol_ln_num +=1
                    print('\n\nImgList', imgList,"\n\n")

                    #input("paused ENTER")

                    log_string = str(imgList)   # Looks like this:  {'FLOWER_REAL.BMP': (181, 264)}
                    log_string = log_string.replace('{', "") #Remove dictionary bracket from imgList
                    log_string = log_string.replace('}', "") #Remove dictionary bracket from imgList
                    log_string = log_string.replace(',', ';') #replace ',' with ';' so it is not split in CSV file
                    log_string = log_string.replace(':', ',') #put ',' between image name and coordinates to split coord from name in CSV file

                    print('log_string', log_string)
                    GUIFunctions.log_event(self, self.events, log_string, self.cur_time)


                else: # PLACE IMAGES IN COORDINATES PRESSCRIBED I PROTOCOL

                    placementList = random.sample(range(0,len(self.touchImgCoords)), len(self.touchImgCoords)) # Randomize order of images
                    print(placementList, self.touchImgCoords)

                    # NOTE: random.sample(population, k)
                    #       Returns a new list containing elements from the population while leaving
                    #       the original population unchanged.
                    #       Here: for 2 images, population = (0,2), k = 2.  returns (0,1) or (1,0)
                    imgList = {}
                    i=0
                    for key in self.touchImgs.keys():
                        imgList[key] = self.touchImgCoords[placementList[i]] #places images
                        #print('ImgList', imgList)
                        i+=1
                        self.TSq.put(imgList)

                    self.Protocol_ln_num +=1

                    #print('\n\nImgList', imgList,"\n\n")
                    #input("paused ENTER")
                    log_string = str(imgList) # Looks like this:  {'SPIDER_REAL.BMP': (181, 100), 'FLOWER_REAL.BMP': (602, 100)}
                    log_string = log_string.replace('{', "") #Remove dictionary bracket from imgList
                    log_string = log_string.replace('}', "") #Remove dictionary bracket from imgList
                    log_string = log_string.replace(',', ';') #replace ',' with ';' so it is not split in CSV file
                    log_string = log_string.replace(':', ',') #put ',' between image name and coordinates to split coord from name in CSV file
                    idx = log_string.find(")")
                    #print("IDX: ", idx, "logstring: ", log_string)
                    while idx != -1: # returns -1 if string not found
                        try:
                            if log_string[idx+1] == ";": # Could be out of range if ")" is last char
                                log_string = log_string[:idx+1]+ "," + log_string[idx+2:] # This will change the ";" separating images into "," to separate images and coordinates in CSV file
                            idx = log_string.find[:idx+2](")")
                            print("IDX: ", idx, "logstring: ", log_string)
                        except:
                            print("\n\n IDX: ",idx,"  FAILED creating log string\n\n")
                            break
                    print('log_string', log_string)
                    GUIFunctions.log_event(self, self.events, log_string, self.cur_time)
        ###############################
        # START LOOP
        ###############################
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
            # NUMBER OF LOOPS DEPENDS ON PERCENT CORRECT?
            # START_LOOPS = RANDOM(5,10), Picks random number beteen 5, 10 inclusive (?)
            if "RANDOM" in protocolDict[key]:
                if self.LOOP_FIRST_PASS:
                    intrange = protocolDict[key][7:len(protocolDict[key])-1]
                    print("intrange: ", intrange)
                    a,b = intrange.split(",")
                    print("a,b: ", a,b)
                    self.NUM_LOOPS = random.randint(int(a), int(b))
                    self.LOOP_FIRST_PASS = False

            # NUMBER OF LOOPS DEPENDS ON PERCENT CORRECT?
            # START_LOOPS = COORECT(50%,5,10), If CONDITION OUTCOMS are correct 50% of the time, end loop. Min loops = 5, max loops = 10
            elif 'CORRECT' in protocolDict[key]:
                info = protocolDict[key].split('(')
                percent, min, max = info[1].split(',')
                self.percent = int(percent[:-1])
                self.max = int(max[:-1])
                self.NUM_LOOPS = int(min)
                self.check_correct = True
            # NUMBER OF LOOPS DEPENDS ON PERCENT CORRECT?
            # START_LOOPS = WRONG(50%,5,10), If CONDITION OUTCOMS are wrong 50% of the time, end loop. Min loops = 5, max loops = 10
            elif 'WRONG' in protocolDict[key]:
                info = protocolDict[key].split('(')
                percent, min, max = info[1].split(',')
                self.percent = int(percent[:-1])
                self.max = int(max[:-1])
                self.NUM_LOOPS = int(min)
                self.check_wrong = True
            # NUMBER OF LOOPS DEPENDS ON PERCENT CORRECT?
            # START_LOOPS = NO_ACTION(50%,5,10), If CONDITION OUTCOMS are NO_ACTION 50% of the time, end loop. Min loops = 5, max loops = 10
            elif 'NO_ACTION' in protocolDict[key]:
                info = protocolDict[key].split('(')
                percent, min, max = info[1].split(',')
                self.percent = int(percent[:-1])
                self.max = int(max[:-1])
                self.NUM_LOOPS = int(min)
                self.check_no_action = True

            else:  self.NUM_LOOPS = int(protocolDict[key])
            GUIFunctions.log_event(self, self.events,"LOOPING "+ str(self.NUM_LOOPS)+ " times, TRIAL "+str(self.trial_num),self.cur_time)
        ###############################
        # END LOOP
        ###############################
        elif "END_LOOP" in key:
            self.num_lines_in_loop = self.Protocol_ln_num - self.loop_start_line_num
            if self.percent: #if using percent based loops
                if int(self.NUM_LOOPS) > self.trial_num+1:
                    self.Protocol_ln_num = self.loop_start_line_num
                elif (self.max < self.trial_num + 1
                        or (self.percent < self.correctPercentage and self.check_correct)
                        or (self.percent < self.wrongPercentage and self.check_wrong)
                        or (self.percent < self.no_actionPercentage and self.check_no_action)):
                    self.Protocol_ln_num +=1
                    GUIFunctions.log_event(self, self.events,"END_OF_LOOP",self.cur_time)
                    self.loop = 0
                    self.LOOP_FIRST_PASS = True
                    self.VI_index = 0
                    self.percent = False
                else:
                    self.Protocol_ln_num = self.loop_start_line_num

            elif self.loop  < int(self.NUM_LOOPS):
                #self.Protocol_ln_num = self.Protocol_ln_num - self.num_lines_in_loop
                self.Protocol_ln_num = self.loop_start_line_num
                self.VI_index += 1


            else:
                self.Protocol_ln_num +=1
                GUIFunctions.log_event(self, self.events,"END_OF_LOOP",self.cur_time)
                self.loop = 0
                self.LOOP_FIRST_PASS = True
                self.VI_index = 0
            #trial = 0 Do not set here in case there are more than 1 loops

        ###############################
        # PAUSE
        ###############################
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

            if self.TOUCHSCREEN_USED:
                if not self.TSBack_q.empty():
                       self.touchMsg = self.TSBack_q.get()
                       GUIFunctions.log_event(self, self.events, self.touchMsg['picture'] + "Pressed BETWEEN trials, " + "(" + self.touchMsg['XY'][0] + ";" +self.touchMsg['XY'][1] + ")" , self.cur_time)

        elif key == "CONDITIONS":
            self.runConditions(protocolDict, self.cur_time)

        else:
            print("PROTOCOL ITEM NOT RECOGNIZED",key)

        #########################################################################################
        # RUN BAR PRESS INDEPENDENT OF PROTOCOLS OR CONDTIONS
        #########################################################################################
        if self.BAR_PRESS_INDEPENDENT_PROTOCOL: #Running independently of CONDITIONS. Used for conditioning, habituation, extinction, and recall
            if self.LEVER_PRESSED_R or self.LEVER_PRESSED_L: # ANY LEVER
               self.num_bar_presses +=1

            if self.VI_REWARDING:  # [BAR_PRESS] in protocol
                                   #  VI=15
                self.VI = self.var_interval_reward

            elif self.BAR_PRESS_TRAINING: # BAR_PRESS_TRAIN=VI(1,15) in protocol

                # Calculate Bar Presses Per Minute
                BPPM_time_interval = self.cur_time - self.VI_calc_start

                if BPPM_time_interval >= 60.0:  #Calculate BPPM every minute (60 sec)
                    self.BPPM =  self.num_bar_presses#   0.0
                    GUIFunctions.log_event(self, self.events, "Bar Presses Per Min:,"+ str(self.BPPM ) , self.cur_time)
                    print ("\n\n\nnum_bar_presses:: ",self.num_bar_presses, "BPPM: ",self.BPPM)
                    self.BPPMs.append(self.BPPM) # Add a BPPM calcualtion to list every minute
                    # Reset for next minute  TPM_start_time
                    self.num_bar_presses = 0
                    self.VI_calc_start = self.cur_time

                    # Calculate MEAN Bar Presses Per Minute over 10 min
                    #if len(self.BPPMs)> 10:#10: # after every 10 minutes (That is, 10 one minute evaluations convolved every minute)
                    if len(self.BPPMs)== 10:#10: # after first 10 minutes only!!
                        print("BPPMs: ",self.BPPMs)
                        self.meanBPPM10 = sum(self.BPPMs[-10:])/10.0#10.0       # Mean Bar PRESSES per minute over last 10 minutes
                        GUIFunctions.log_event(self, self.events, "MEAN Bar Presses Per Min:,"+ str(self.BPPM )+",Over 1st 10 min" , self.cur_time)
                        print ("MEAN BPPM over ist 10 min: ",self.meanBPPM10)
                        #self.BPPMs.pop(0)                                  # Removes first item of list for running list
                        if self.BAR_PRESS_TRAINING: # [BAR_PRESS] in protocol
                                                  #  BAR_PRESS_TRAIN=VI(1,15)
                                                  #  note: VI(a,b); a = initial VI for bar PRESS, b = final VI for session

                            if self.meanBPPM10 >= 10.0: #increae VI reward interval if mean over 1st 10 min exceeeds 10 BPPM
                                self.var_interval_reward += 15 # Increases VI by 15
                                if self.var_interval_reward >=  self.VI_final:
                                    self.var_interval_reward =  self.VI_final # Limit VI to final value (b above)
                                GUIFunctions.log_event(self, self.events, "NEW VI between: 0 and "+ str(2*self.var_interval_reward) + " (sec)" , self.cur_time)
                                print ("NEW VI between: 0 and "+ str(2*self.var_interval_reward) + " (sec)" )

            # Check if amount of VI has passed. If so, reward. Recalc VI
            if self.LEVER_PRESSED_R or self.LEVER_PRESSED_L: # ANY LEVER
                if self.cur_time > (self.VI_start + self.VI):

                   GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet",self.cur_time)
                   # Calculate self.VI for next time
                   if self.var_interval_reward <= 1:
                       self.VI = 0
                   else:
                       self.VI = random.randint(0,int(self.var_interval_reward*2)) #NOTE: VI15 = reward given on variable interval with mean of 15 sec

                   GUIFunctions.log_event(self, self.events, "Current VI now: "+ str(self.VI) + " (sec)" , self.cur_time)
                   self.VI_start = self.cur_time

                self.LEVER_PRESSED_R = False
                self.LEVER_PRESSED_L = False

#Variable Ratio rewards.
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#                  if self.VR == 1:
#                      GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet",self.cur_time) # Give reward on each bar press
#                      self.VRs_given +=1
#                      if self.VRs_given > 10:
#                          self.VRs_given = 0
#                          self.VR +=1 #VR = 2
#                      GUIFunctions.log_event(self, self.events, "new vi: "+ str(self.VI) + " (sec)" , self.cur_time)
#
#                  if self.VR == 2:
#                      VR_reward = random.randint(1,self.VR) # Give reward on average every 2 bar presses
#                      GUIFunctions.log_event(self, self.events, "VR reward: "+ str(VR_reward), self.cur_time)
#                      #print("VR", self.VR, "rand num: ", VR_reward)
#                      if VR_reward == self.VR:
#                         GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet",self.cur_time)
#                         self.VRs_given +=1
#                         if self.VRs_given > 10:
#                            self.VRs_given = 0
#                            self.VR +=3 #VR = 5

#
#                  if self.VR % 5 == 0:  # Will continue giving rewards on average 1 out of every N times(where n is divisible by 5, i.e. 5, 10, 15, 20 ...)
#                      VR_reward = random.randint(1,self.VR)
#                      GUIFunctions.log_event(self, self.events, "VR reward: "+ str(VR_reward), self.cur_time)
#                      #print("VR", self.VR, "rand num: ", VR_reward)
#                      if VR_reward == self.VR:
#                         GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet",self.cur_time)
#                         self.VRs_given +=1
#                         if self.VRs_given > 10:
#                            self.VRs_given = 0
#                            if self.VR < 35: #VR will stay at 30 and no more until END_LOOP is reached.
#                                self.VR +=5 #VR = 10, 15, 20, 25, 30
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


        # Clean up vars
        self.LEVER_PRESSED_R = False
        self.LEVER_PRESSED_L = False

        #########################################################
        #  PROTOCOL ENDED (Reset everything for next run
        #########################################################
        #print("TIME ELAPSED: ", self.cur_time, "MAX EXPT TIME: ", self.max_time * 60.0, " sec")
        if self.cur_time >= self.MAX_EXPT_TIME * 60.0: # Limits the amout of time rat can be in chamber (self.MAX_EXPT_TIME in PROTOCOL.txt file (in min)
           GUIFunctions.log_event(self, self.events,"Exceeded MAX_EXPT_TIME",self.cur_time)
           print("MAX EXPT TIME EXCEEDED: ", self.cur_time, " MAX_EXPT_TIME: ",self.MAX_EXPT_TIME)
           GUIFunctions.log_event(self, self.events,"PROTOCOL ENDED-max time exceeded",self.cur_time)
           print("\nPROTOCOL ENDED-Max time exceeded")
           self.RECORDING = False
           GUIFunctions.log_event(self, self.events,"Camera_OFF",self.cur_time)
           self.vidSTATE = 'REC_STOP'  # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
           self.end_expt()

        if self.Protocol_ln_num >= len(self.protocol):
           GUIFunctions.log_event(self, self.events,"PROTOCOL ENDED",self.cur_time)
           print("\nPROTOCOL ENDED NORMALLY")
           GUIFunctions.log_event(self, self.events,"Camera_OFF",self.cur_time)
           self.vidSTATE = 'REC_STOP'  # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
           self.end_expt()


####################################################################################
#   END EXPT
####################################################################################

    def end_expt(self):
           print("Protocol_ln_num: ",self.Protocol_ln_num,"plength: ", len(self.protocol),"\n")
           print("......END.....\n")
           print("__________________________________________________________________________\n\n\n\n")
           self.START_EXPT = False

           self.LEDs[0].ONOFF = "OFF"
           self.LEDs[1].ONOFF = "OFF"
           for LED in self.LEDs: # Look for EXPT STARTED LED
               if LED.index == 6: # Expt Started light
                  LED.ONOFF = "OFF"
           GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)
           GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,False,self.cur_time)



           # Tell open ephys to stop acquistion and recording?
           # Maybe we want to wait and continue getting data for awhile. Just send some sort of event
           self.snd.send(self.snd.STOP_ACQ)
           self.snd.send(self.snd.STOP_REC)

           if self.TOUCHSCREEN_USED:
               self.TSq.put('')
               self.TOUCHSCREEN_USED = False
               while not self.TSBack_q.empty():  # EMPTY TSBack_q between Expt Runs.
                   self.touchMsg = self.TSBack_q.get()

           for user_input in self.user_inputs:
              if user_input.label == "SUBJECT":
                 self.Subject = ''
                 self.prev_Subject = self.Subject

           GUIFunctions.log_event(self, self.events,"EXPT ENDED",self.cur_time)

           self.RECORDING = False
           GUIFunctions.log_event(self, self.events,"Recording_OFF",self.cur_time)
           self.vidSTATE = 'REC_STOP'  # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)

           if "EPHYS-2" in self.computer:
               GUIFunctions.L_CONDITIONING_LIGHT(self, self.events,False, self.cur_time)
               GUIFunctions.R_CONDITIONING_LIGHT(self, self.events,False, self.cur_time)

           GUIFunctions.FAN_ON_OFF(self, self.events,False,self.cur_time) # {'FAN_ON': True} or {'FAN_ON': False}
           self.Background_color = GUIFunctions.CAB_LIGHT(self, self.events,False,self.cur_time)
           GUIFunctions.EXTEND_LEVERS(self, self.events,"Levers_Retracted",False,False,self.cur_time)


####################################################################################
#   DO CONDITIONS
####################################################################################
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

            #print("\n\nCONDTION")
            #print(self.cond)
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
               if not self.HAS_ALREADY_RESPONDED:# Prevents rewarding for multiple presses. Ensures max of one press per trial.
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
                   #print("cond['DES_R_LEVER_PRESS']",self.cond['DES_R_LEVER_PRESS'])
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

           ######################################
           #     TOUCHSCREEN USED
           ######################################
           if self.TOUCHSCREEN_USED:
               TPM_time_interval = self.cur_time - self.TPM_start_time # TO CALCULATE TOUCHES PER MIN (TPM)

               ######################
               # SCREEN TOUCHED
               ######################
               if not self.TSBack_q.empty():
                   self.touchMsg = self.TSBack_q.get()
                   x = int(self.touchMsg['XY'][0])
                   y = int(self.touchMsg['XY'][1])
                   ##########################################
                   #  BACKGROUND TOUCHED (image missed)
                   ##########################################
                   if self.touchMsg['picture'] == 'missed': # Touched background

                       GUIFunctions.log_event(self, self.events," missed ," + "(" + str(x) + ";" + str(y)  + ")", self.cur_time)
                       self.background_hits.append((int(x/4),int(y/4)))# To draw on gui. Note:(40,320) is top left of gui touchscreen, 1/4 is the gui scale factor
                       self.background_touches += 1
                       #if self.TOUCH_TRAINING:
                       #   self.WRONG = True # When TOUCHSCREEN TRAING, ANY TOUCH RESULTS IN TRUE (??????????)
                       self.WRONG = True # When TOUCHSCREEN TRAING, ANY TOUCH RESULTS IN TRUE (??????????)
                   ###################
                   #  IMAGE TOUCHED
                   ###################
                   elif not self.HAS_ALREADY_RESPONDED: # Target touched
                       self.touch_time = cur_time
                       self.HAS_ALREADY_RESPONDED = True
                       self.any_image_touches += 1
                       # Check probability for pic/trial
                       ##################################
                       # BANDIT TOUCH
                       ##################################
                       if self.TOUCH_BANDIT:
                           for img, probabilityList in self.touchImgs.items():
                               #print(probabilityList,'problist\n')

                               probabilityListIDX = self.trial_num % len(probabilityList) # IDX = trial num. If Trial num exceeds len(probabilityList), it starts over
                               reward_prob_for_this_img = probabilityList[probabilityListIDX]


                               print(" reward_prob_for ", img, " = ", reward_prob_for_this_img  )
                               print(self.touchMsg['picture'], img)
                               if self.touchMsg['picture'] == img:  # Touched an image
                                   print(self.touchMsg['picture'], img)
                                   GUIFunctions.log_event(self,self.events, "Probability of pellet: " + str(probabilityList[self.trial_num]),self.cur_time)

                                   if reward_prob_for_this_img > 50.0:
                                       self.correct_img_hits.append((int(x/4),int(y/4)))# To draw on gui. Note:(40,320) is top left of gui touchscreen, 1/4 is the gui scale factor
                                       GUIFunctions.log_event(self, self.events,"High PROB: " + self.touchMsg['picture'] + ":" + img + " TOUCHED, " +  "(" + str(x) + ";" + str(y)  + ")" , self.cur_time)
                                   else: # Less desirable image touchewd
                                       self.wrong_img_hits.append((int(x/4),int(y/4)))# To draw on gui. Note:(40,320) is top left of gui touchscreen, 1/4 is the gui scale factor
                                       GUIFunctions.log_event(self, self.events,"Low PROB: " + self.touchMsg['picture'] + ":" + img + " TOUCHED, " +  "(" + str(x) + ";" + str(y)  + ")" , self.cur_time)
                                   # Holds the probability for each trial
                                   self.cur_probability = probabilityList[self.trial_num] # List of probabilities specified after images in protocol files
                                   self.CORRECT = True
                                   self.correct_image_touches += 1

                       #################################
                       # TOUCH TRAINING
                       #################################
                       elif self.TOUCH_TRAINING:
                           self.correct_img_hits.append((int(x/4),int(y/4)))# To draw on gui. Note:(40,320) is top left of gui touchscreen, 1/4 is the gui scale factor

                           for img in self.touchImgs.keys():
                               if self.touchMsg['picture'] == img:  # Touched an image
                                  self.correct_image_touches += 1
                                  self.CORRECT = True
                                  GUIFunctions.log_event(self, self.events,self.touchMsg['picture'] + " Pressed," + "(" + str(x) + ";" + str(y) + ")" , self.cur_time)

               # CALCULATE TOUCHES PER MINUTE (TPMs)
               if TPM_time_interval > 60.0: #60.0: #Calculate TPM every minute (60 sec)
                  self.TPM = self.background_touches + self.any_image_touches
                  self.TPMimg = self.any_image_touches
                  print("TPM: ", self.TPM, "\nTPMimgs: ", self.TPMimg)
                  print("total touches: ", (self.background_touches + self.any_image_touches),"\nimages touches only: ", self.any_image_touches)

                  self.TPMs.append(self.TPM) # Add a TPM calcualtion to list every minute
                  self.TPMimgs.append(self.TPMimg)

                  # Reset for next minute  TPM_start_time
                  self.TPM_start_time = self.cur_time
                  self.background_touches = 0
                  self.any_image_touches = 0
                  #self.correct_image_touches = 0


                  #if len(self.TPMs)%10 == 0: # after every 10 minutes (That is, 10 one minute evaluations)
                  if len(self.TPMs)> 10:#10: # after every 10 minutes (That is, 10 one minute evaluations convolved every minute)
                      self.meanTPM10 = sum(self.TPMs[-10:])/10.0             # Mean touches per minute over last 10 minutes (includes both screen and image touches)
                      self.meanTPM10imgs = sum(self.TPMs[-10:])/10.0         # Mean touches per minute over last 10 minutes calculated every 10 min(includes only image touches)

                      self.TPMs.pop(0)              # Removes first item of list for running list
                      self.TPMimgs.pop(0)           # Removes first item of list for running list

                      #####################################

                      if self.meanTPM10 > 10:# 10: # Reduce probability of reward for touching background + self.any_image_touches
                            self.VI_background += 15.0
                            GUIFunctions.log_event(self, self.events,"VI for BACKGROUND Touches: "+ str(self.VI_background),self.cur_time)
                      if self.meanTPM10imgs > 10:# 10: # Reduce probability of reward for touching images only
                            self.VI_images += 1.0
                            if self.VI_images >= 15.0: self.VI_images = 15.0 # Limits VI for images to 60!!!!
                            GUIFunctions.log_event(self, self.events,"VI for IMG Touches: "+ str(self.VI_images),self.cur_time)

                            self.VI_background += 15.0
                            GUIFunctions.log_event(self, self.events,"VI for BACKGROUND Touches: "+ str(self.VI_background),self.cur_time)

                      print("MeanTPM10: ", self.meanTPM10, "MeanTPM10imgs: ", self.meanTPM10imgs)
                      print("\nVI_background: ", self.VI_background,"\nVI_images ", self.VI_images)


           ################
           #  RESET
           ################
           if self.cond["RESET"] == "FIXED":
               if cond_time_elapsed >= float(self.cond["MAX_TIME"]): # Time is up
                  self.CONDITION_STARTED = False
                  if not self.WRONG and not self.CORRECT:
                      self.NO_ACTION_TAKEN = True
                      GUIFunctions.log_event(self, self.events,"NO_ACTION_TAKEN",self.cur_time)
                  self.TIME_IS_UP = True

           if self.cond["RESET"] == "ON_RESPONSE":
               #print (cond["Reset"])
               if self.WRONG or self.CORRECT: # A response was given
                   self.CONDITION_STARTED = False  # Time is up
                   # NOTE: "END_OF_TRIAL" LOGGED AFTER OUTCOMES
                   self.TIME_IS_UP = True
               if cond_time_elapsed >= float(self.cond["MAX_TIME"]): # Time is up
                  self.CONDITION_STARTED = False
                  if not self.WRONG and not self.CORRECT:
                      self.NO_ACTION_TAKEN = True
                      GUIFunctions.log_event(self, self.events,"NO_ACTION_TAKEN",self.cur_time)
                  self.TIME_IS_UP = True

           if self.cond['RESET'] == "VI":
               pass


           ################
           #  TIME IS UP
           ################
           if self.TIME_IS_UP: # TIME IS UP FOR LOOP
               # SET OUTCOMES
               if self.CORRECT:
                  print("TONE1 DuRATION: ", self.Tone1_Duration)
                  #self.TONE_ON = True
                  self.GUIFunctions.PLAY_TONE(self, self.events,'TONE1 for Correct Response',self.cur_time) #THIS IS DONE EVERY CORRECT RESPOSE EVEN IF REWARD NOT GIVEN
                  outcome = self.cond['CORRECT'].upper()  # Outcome for correct response(in Expt File)
                  self.num_correct += 1
                  self.correctPercentage = self.num_correct/self.trial_num * 100
                  print("Correct")
               elif self.WRONG:
                  outcome = self.cond['WRONG'].upper()    # Outcome for wrong response(in Expt File)
                  self.num_wrong += 1
                  self.wrongPercentage = self.num_wrong/self.trial_num * 100
                  print("Wrong")
               else:
                  outcome = self.cond['NO_ACTION'].upper()# Outcome for No_Action taken(in Expt File)
                  self.num_no_action += 1
                  self.no_actionPercentage = self.num_no_action/self.trial_num * 100
                  print("No Action Taken")
               print(outcome)
               ##############################################################
               # OUTCOMES (Specified in protocol files under [CONDITIONS])
               ##############################################################
               if 'PELLET' in outcome:
                   if len(outcome)<=6: # Just 'PELLET'
                       GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet",self.cur_time)
                       #GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet,100, % Probabilty",self.cur_time)
                   else: #"PELLET****" i.e. PELLET80 or PELLET_VAR or PELLET_TOUCHVI1 or PELLET_TOUCHVI2
                       left_of_outcome_str = outcome[6:]
                       #print(left_of_outcome_str)
                       if "_TOUCHVI1" == left_of_outcome_str: # PELLET_TOUCHVI1: Touched image (CORRECT RESPONSE)
                           if self.cur_time > (self.VI_start + self.cur_VI_images): # Give reward and reset VIs
                              # Give Rewards
                              GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet",self.cur_time)
                              #GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet," + str(self.cur_VI_images)+ ",VI",self.cur_time)

                              # Reset VIs
                              self.VI_start = self.cur_time
                              self.cur_VI_images = random.randint(0,int(self.VI_images * 2)) #NOTE: VI15 = reward given on variable interval with mean of 15 sec
                              #print("new vi", self.cur_VI_images, " (sec)")
                              GUIFunctions.log_event(self, self.events,"NEW_VI FOR IMAGE TOUCH = " + str(self.cur_VI_images),self.cur_time)

                       elif "_TOUCHVI2" in left_of_outcome_str: # or PELLET_TOUCHVI2: Touched Background (WRONG RESPONSE)
                           if self.cur_time > (self.VI_start + self.cur_VI_background): # Give reward and reset VIs
                              # Give 1 Reward
                              GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet",self.cur_time)
                              #GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet," + str(self.cur_VI_images)+ ",VI",self.cur_time)

                              # Reset VIs
                              self.VI_start = self.cur_time
                              self.cur_VI_background = random.randint(0,int(self.VI_background*2)) #NOTE: VI15 = reward given on variable interval with mean of 15 sec
                              #print("new backgroung vi", self.VI_background, " (sec)")
                              GUIFunctions.log_event(self, self.events,"NEW_VI FOR BACKGROUND TOUCH = " + str(self.cur_VI_images),self.cur_time)


                       elif "VAR" in left_of_outcome_str: # if "PELLET_VAR" in conditions portion of protocol
                           rand = random.random() * 100
                           #print("our random number", rand)
                           if rand <= self.cur_probability:
                               #print("Food_Pellet w"+str(self.cur_probability)+ "% probability")
                               GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet", self.cur_time)
                               #GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet,"+str(self.cur_probability)+ ",% probability", self.cur_time)

                           else:
                               #print("Reward NOT given w " + str(self.cur_probability)+"% probability")
                               GUIFunctions.log_event(self, self.events,"Reward NOT given," + str(self.cur_probability)+",% probability", self.cur_time)

                       else: # if PELLET80 or something like it.  NOTE: PELLETXX, converts XX into probability
                           if random.random()*100 <= float(left_of_outcome_str):
                               GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet", self.cur_time)
                               #GUIFunctions.FOOD_REWARD(self, self.events,"Food_Pellet,"+str(left_of_outcome_str)+ "%, probability", self.cur_time)

                           else:
                               GUIFunctions.log_event(self, self.events,"Reward NOT given" + str(left_of_outcome_str)+",% probability", self.cur_time)


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
                   #print("Outcome = NONE")
               if self.TOUCHSCREEN_USED:
                   # Want to wait a second before blanking screen
##                   if self.cur_time - self.touch_time > 1.0:
##                       self.TSq.put('')
                   self.TSq.put('')

               self.TIME_IS_UP = False
               self.CONDITION_STARTED = False
               GUIFunctions.log_event(self, self.events,"END_OF_TRIAL",self.cur_time)
               self.Protocol_ln_num +=1

if __name__ == "__main__":
    print("NIDAQ_AVAILABLE: ", NIDAQ_AVAILABLE)
    GUIFunctions.openWhiskerEphys(NIDAQ_AVAILABLE)
    beh = BEH_GUI(NIDAQ_AVAILABLE)
    beh.BehavioralChamber()

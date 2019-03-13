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

import os
import sys, time
import pygame
from pygame.locals import *

import math, random
import numpy as np
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
import GUIFunctions
import subprocess
import experiment
import win32gui, win32con
from tkinter import *
from tkinter import messagebox
Tk().wm_withdraw() #to hide the main window

class BEH_GUI():
    def __init__(self, NIDAQ_AVAILABLE):
        self.NIDAQ_AVAILABLE = NIDAQ_AVAILABLE
        self.setGUIGlobals()
        self.computer = os.environ['COMPUTERNAME']
        random.seed()
        #self.expt = experiment.Experiment(self)
        self.setupExpt()


    from setGUIGlobals import setGUIGlobals
    from loadProtocol import load_expt_file, create_expt_file_copy, create_files
    import GUIFunctions
    from setupGUI import setupExpt

    def BehavioralChamber(self):
        while True:
            self.drawScreen()
            self.checkSystemEvents()
            self.checkNIDAQEvents()

            if self.START_EXPT:
                self.expt.run()
            if self.RESTART_EXPT:
                self.setupExpt() # Setups experiment and GUI!

            ######################################
            #   UPDATE SCREEN
            ######################################
            pygame.display.flip()

########################################################################################
    def drawScreen(self):
        if self.START_EXPT:
            self.cur_time = time.perf_counter()-self.expt.Experiment_Start_time
        else:
            self.cur_time = time.perf_counter()
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
                         self.LEVER_PRESSED_L = False
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
                   if (time.perf_counter() - self.NOSE_POKE_TIME) > 0.25: #Leaves on for 0.25 sec
                         LED.ONOFF = "OFF"  # NOW OFF
                         self.NOSE_POKED_L = False
                   else:
                         LED.ONOFF = "ON"

            elif LED.index == 3: #Right NOSE POKE
                if self.NOSE_POKED_R:
                   if (time.perf_counter() - self.NOSE_POKE_TIME) > 0.25: #Leaves on for 0.25 sec
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
                if not self.EXPT_LOADED:
                    info.text = "0"
                else:
                  info.text = [str(self.expt.num_L_nose_pokes)]
            elif info.label == "R NOSE POKES":
                if not self.EXPT_LOADED:
                    info.text = "0"
                else:
                  info.text = [str(self.expt.num_R_nose_pokes)]
            elif info.label == "L PRESSES":
                if not self.EXPT_LOADED:
                    info.text = "0"
                else:
                  info.text = [str(self.expt.num_L_lever_preses)]
            elif info.label == "R PRESSES":
                if not self.EXPT_LOADED:
                    info.text = "0"
                else:
                  info.text = [str(self.expt.num_R_lever_preses) ]
            elif info.label == "PELLETS":
                if not self.EXPT_LOADED:
                    info.text = "0"
                else:
                  info.text = [str(self.expt.num_pellets)]
            elif info.label == "EATEN":
                if not self.EXPT_LOADED:
                    info.text = "0"
                else:
                  info.text = [str(self.expt.num_eaten)]
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
                if not self.EXPT_LOADED:
                    user_input.text = "0"
                else:
                 user_input.text  = str(self.expt.trial_num)
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
              if (time.perf_counter() - self.TONE_TIME) > float(self.Tone1_Duration): # seconds
                  #print("TONE OFF")
                  self.TONE_ON = False
                  if "EPHYS-1" in self.computer:
                      self.low_tone.sendDBit(False)
                  if self.EXPT_LOADED: self.expt.log_event("Tone_OFF")

        # DRAW SHOCK LIGHTNING
        self.shock = GUIFunctions.draw_lighting(self.myscreen, self.SHOCK_ON, 248,150,1,(255,255,0),2)
        if self.SHOCK_ON:
              if (self.cur_time - self.SHOCK_TIME) <= self.Shock_Duration: # seconds
                  if self.NIDAQ_AVAILABLE: self.apply_shock.sendDBit(True)
              else:
                  self.SHOCK_ON = False
                  if self.NIDAQ_AVAILABLE: self.apply_shock.sendDBit(False)
                  #print("SHOCK OFF")
                  if self.EXPT_LOADED: self.expt.log_event("Shock_OFF")


        # DRAW CAMERA
        #    Note:                 draw_camera(self.myscreen,fill_color, ON_OFF, REC, x, y, w,h, linew)
        self.camera = GUIFunctions.draw_camera(self.myscreen, (100,100,100),self.CAMERA_ON,self.RECORDING,235, 245, 30,20, 2)

        # GUI TOUCH SCREEN
        if self.EXPT_LOADED and self.expt.TOUCHSCREEN_USED:
            for x,y in self.expt.background_hits:
                #print(x,y)
                draw_plus_sign(self.myscreen, x + 40, y +320, 5, (255,0,0) ) # (40,320) is top left of gui touchscreen, 1/4 is the gui scale factor                      self.touch_time = cur_time

            for x,y in self.expt.correct_img_hits:
                draw_plus_sign(self.myscreen, x + 40, y +320, 5, (0,255,0) ) # (40,320) is top left of gui touchscreen, 1/4 is the gui scale factor                      self.touch_time = cur_time

            for x,y in self.expt.wrong_img_hits:
                draw_plus_sign(self.myscreen, x + 40, y +320, 5, (0,0,255) ) # (40,320) is top left of gui touchscreen, 1/4 is the gui scale factor                      self.touch_time = cur_time

        try:
            #print(self.touchImgCoords)
            for coords in self.expt.touchImgCoords:
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
            if event.type == pygame.QUIT:
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
                                       self.Background_color = GUIFunctions.CAB_LIGHT(self,False)
                                       self.CAB_LIGHT_ON = False
                                   else: # Toggle ON
                                       self.Background_color = GUIFunctions.CAB_LIGHT(self,True)
                                       self.CAB_LIGHT_ON = True
                               if button.text == "FAN": #TOGGLE ON TOGGLE OFF
                                    if self.FAN_0N:
                                       self.FAN_0N = False
                                       GUIFunctions.FAN_ON_OFF(self,self.FAN_0N)

                                    else:
                                       self.FAN_0N = True
                                       GUIFunctions.FAN_ON_OFF(self,self.FAN_0N)

                               elif button.text == "FEED":
                                    button.UP_DN = "DN"
                                    self.FEED = True
                                    GUIFunctions.FOOD_REWARD(self,"Food_Pellet_by_GUI")
                                    # NOTE: Food reward needs time after High bit, before low bit is sent.
                                    #       So rather than putting a sleep in the FOOD_REWARD function, a low bit
                                    #       is sent when button is released using FOOD_REWARD_RESET(self)
                               # LEFT LEVER
                               elif button.text == "L":
                                    if self.L_LEVER_EXTENDED: # Was EXTENDED
                                          button.UP_DN = "UP"
                                          GUIFunctions.EXTEND_LEVERS(self,"L_Lever_Retracted_by_GUI",False,False)
                                          self.levers[0].STATE = "IN"

                                    else: # Was not extended
                                          button.UP_DN = "DN"
                                          GUIFunctions.EXTEND_LEVERS(self,"L_Lever_Extended_by_GUI",True,False)
                                          self.levers[0].STATE = "OUT"

                               # RIGHT LEVER
                               elif button.text == "R":
                                    if self.R_LEVER_EXTENDED: # Was EXTENDED
                                          button.UP_DN = "UP"
                                          GUIFunctions.EXTEND_LEVERS(self,"R_Lever_Retracted_by_GUI",False,False)
                                          self.levers[1].STATE = "IN"

                                    else: # was not extended
                                          button.UP_DN = "DN"
                                          GUIFunctions.EXTEND_LEVERS(self,"R_Lever_Extended_by_GUI",False,True)
                                          self.levers[1].STATE = "OUT"

                               # BOTH LEVERS AT ONCE
                               elif button.text == "EXTEND" or button.text == "RETRACT":
                                    if self.LEVERS_EXTENDED: #Toggle EXTEND and RETRACT
                                          button.UP_DN = "UP"
                                          #LEVERS_EXTENDED = False
                                          GUIFunctions.EXTEND_LEVERS(self,"Levers_Retracted_by_GUI",False,False)
                                          button.text = "EXTEND"
                                          for lever in self.levers:
                                                lever.STATE = "IN"

                                    else: # not extended
                                          button.UP_DN = "DN"
                                          button.text = "RETRACT"
                                          #LEVERS_EXTENDED = True
                                          GUIFunctions.EXTEND_LEVERS(self,"Levers_Extended_by_GUI",True,True)
                                          for lever in self.levers:
                                                lever.STATE = "OUT"

                               elif button.text == "REC":
                                    if self.CAMERA_ON:
                                          if self.RECORDING: #STOP RECORDING BUT KEEP CAMERA ON. # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
                                                self.RECORDING = False  #KEEP CAMERA ON, JUST STOP RECORDING
                                                if self.EXPT_LOADED: self.expt.log_event("STOP_RECORDING_by_GUI")
                                                self.vidSTATE= 'ON'
                                                button.UP_DN = "UP"
                                          else:
                                                self.RECORDING = True
                                                button.UP_DN = "DN"
                                                if self.EXPT_LOADED: self.expt.log_event("START_RECORDING_by_GUI")
                                                self.vidSTATE = 'REC_VID'


                                    else:
                                          print("CAMERA NOT ON!")

                               #######################################
                               #
                               #   LOAD EXPERIMENTAL PROTOCOL FILE
                               #
                               #######################################
                               elif button.text == "LOAD FILE":
                                    if not self.START_EXPT or self.exptEnded:
                                        self.exptEnded = False
                                        self.RUN_SETUP = False
                                        self.START_EXPT = False
                                        button.UP_DN = "DN"
                                        self.events = []
                                        self.setupExpt()
                                        self.EXPT_LOADED = True
                                        for LED in self.LEDs: # Look for EXPT STARTED LED
                                              if LED.index == 6: # Expt Started light
                                                  LED.ONOFF = "OFF"
                                    else:
                                        messagebox.showinfo('WARNING', 'Stop experiment first!')


                               #######################################
                               #
                               #   STOP EXPERIMENT
                               #
                               #######################################
                               elif button.text == "STOP EXPT":
                                    self.expt.endExpt()

                               #######################################
                               #
                               #   START EXPERIMENT
                               #
                               #######################################
                               elif button.text == "START EXPT":
                                    if self.exptEnded == True:
                                        self.exptEnded = False
                                        self.setupExpt()
                                    if self.EXPT_LOADED:
                                        button.UP_DN = "DN"
                                        self.Expt_Count +=1
                                        #if self.EXPT_FILE_LOADED:
                                        if self.Subject == "" or "?" in self.Subject or self.Subject == " " or len(self.Subject) == 0 :
                                            print('SUBJECT = "" or "?" or same as last time')
                                            messagebox.showinfo('WARNING', 'SUBJECT = "" or "?" or same as last time')
                                            # HIGHLIGHT USER INPUT BOXES
                                            for user_input in self.user_inputs:
                                                if user_input.label == "EXPT":
                                                     user_input.border_color = (255,0,0)
                                                elif user_input.label == "SUBJECT":
                                                     user_input.border_color = (255,0,0)

                                        if self.NAME_OR_SUBJ_CHANGED :  # READY TO GO!!!
                                            # GOOD TO GO!
                                            print("EXPT STARTED!")
                                            for user_input in self.user_inputs:
                                                if user_input.label == "EXPT":
                                                   user_input.text = str(self.Expt_Name)+str(self.Expt_Count)
                                                   for user_input in self.user_inputs:
                                                       if user_input.label == "EXPT":
                                                            user_input.border_color = (0,0,0)
                                                       elif user_input.label == "SUBJECT":
                                                            user_input.border_color = (0,0,0)

                                            button.text = "STOP EXPT"
                                            self.START_EXPT = True

                                    else:
                                        #self.EXPT_FILE_LOADED = False
                                        print("Experiment not loaded yet")
                                        #if self.EXPT_LOADED: self.expt.log_event("Expt File name or path DOES NOT EXIST")

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
                                    GUIFunctions.L_CONDITIONING_LIGHT(self,True)
                                elif LED.index == 1: # RIGHT CONDITION LIGHT
                                    GUIFunctions.R_CONDITIONING_LIGHT(self,True)

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
                                    self.feederBox.fill_color,LEDsONOFF = GUIFunctions.Food_Light_ONOFF (self,True)
                                    self.LEDs[4].ONOFF = LEDsONOFF
                                    self.LEDs[5].ONOFF = LEDsONOFF

                            else:                  # WAS ON
                                LED.ONOFF = "OFF"  # NOW OFF
                                LED.draw()
                                if   LED.index == 0: # LEFT CONDITION LIGHT
                                    GUIFunctions.L_CONDITIONING_LIGHT(self,False)
                                elif LED.index == 1: # RIGHT CONDITION LIGHT
                                    GUIFunctions.R_CONDITIONING_LIGHT(self,False)

                                # FEEDER LEDS
                                elif LED.index == 4 or LED.index == 5: # FEEDER LIGHTS
                                    self.feederBox.fill_color,LEDsONOFF = GUIFunctions.Food_Light_ONOFF (self,False)
                                    self.LEDs[4].ONOFF = LEDsONOFF
                                    self.LEDs[5].ONOFF = LEDsONOFF


                    # FEEDER BOXES
                    for box in self.boxes: # Check for collision with EXISTING buttons
                        if box.rect.collidepoint(cur_x,cur_y):
                           if self.FEEDER_LT_ON: #Toggle OFF
                              self.feederBox.fill_color,LEDsONOFF = GUIFunctions.Food_Light_ONOFF(self,False)
                              self.LEDs[4].ONOFF = LEDsONOFF
                              self.LEDs[5].ONOFF = LEDsONOFF
                              self.FEEDER_LT_ON = False
                           else: # Toggle ON
                              self.feederBox.fill_color,LEDsONOFF = GUIFunctions.Food_Light_ONOFF (self,True)
                              self.FEEDER_LT_ON = True

                    # SPEEKER PRESSED
                    if self.speeker.collidepoint(cur_x,cur_y):
                          # NOTE: Tone_OFF logged while drawing speeker above in main loop
                          if "EPHYS-2" in self.computer:
                             GUIFunctions.PLAY_TONE(self,"TONE1") #using computer speeker
                          elif "EPHYS-1" in self.computer:
                             GUIFunctions.PLAY_TONE_LAF(self,"TONE1") #using computer speeker
                          else:
                              messagebox.showinfo('WARNING','Unknown device, need to set how to play tone. \nLine 605 in BEH_GUI_MAIN')


                    # SHOCK PRESSED
                    if self.shock.collidepoint(cur_x,cur_y):
                          self.SHOCK_TIME = self.cur_time
                          if self.SHOCK_ON:
                                self.SHOCK_ON = False
                                if self.EXPT_LOADED: self.expt.log_event("Shock_OFF")
                                # NOTE: SHOCK ALSO TURNED OFF IN GAME LOOP AFTER Shock_Duration (s)
                          else:
                                self.SHOCK_ON = True
                                if self.EXPT_LOADED: self.expt.log_event("Shock_ON",("Voltage", str(self.Shock_V),"Amps",str(self.Shock_Amp),"Duration(S)",str(self.Shock_Duration)))
                                # NOTE: SHOCK ALSO TURNED OFF IN GAME LOOP AFTER Shock_Duration (s)

                          #print("SHOCK PRESSED")

                    # CAMERA PRESSED
                    if self.camera.collidepoint(cur_x,cur_y):
                          if self.CAMERA_ON: #CAMERAL ALREWADY ON, TURN CAMERA OFF.  # NOTE: STATE = (ON,OFF,REC_VID,REC_STOP, START_EXPT)
                                self.CAMERA_ON = False
                                self.RECORDING = False
                                if self.EXPT_LOADED: self.expt.log_event("Camera_OFF")
                                #print("CAMERA OFF")
                                self.vidSTATE = 'OFF'

                          else: #TURN CAMERA ON # NOTE: STATE = (ON,OFF,REC, START_EXPT,STOP_EXPT)
                                self.CAMERA_ON = True
                                if self.EXPT_LOADED:
                                    self.expt.MyVideo(self)
                                    self.expt.log_event("Camera_ON")
                                #print("CAMERA ON")
                                self.vidSTATE = 'ON'


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
                                 self.setupExpt()
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
                        #GUIFunctions.FOOD_REWARD_RESET(self)


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
                        if self.EXPT_LOADED: self.expt.log_event("Lever_Pressed_R")
                        self.LEVER_PRESSED_R = True
                        #print("RIGHT LEVER PRESSED")
                        self.levers[1].STATE = "DN"

                  if  wasleverPressed == 'Left':
                        if self.EXPT_LOADED: self.expt.log_event("Lever_Pressed_L")
                        self.LEVER_PRESSED_L = True
                        #print("LEFT LEVER PRESSED")
                        if self.START_EXPT: self.expt.num_L_lever_preses += 1
                        self.levers[0].STATE = "DN"

            # nose pokes
            #cur_time = time.perf_counter()
            was_nose_poked_L = daqHelper.checkLeftNosePoke(self.L_nose_poke)

            if was_nose_poked_L:
                #print("LEFT Nose Poked")
                self.NOSE_POKE_TIME = self.cur_time
                #events.append("LEFT Nose Poke: " + str(cur_time))
                if self.EXPT_LOADED: self.expt.log_event("Nose_Poke_L")
                self.NOSE_POKED_L = True
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
                if self.EXPT_LOADED: self.expt.log_event("Nose_Poke_R")
                self.NOSE_POKE_TIME = time.perf_counter()
                self.NOSE_POKED_R = True
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
                self.FOOD_EATEN = True
                event = 'Food_Eaten'
                #events.append("Food Eaten: " + str(cur_time))
                if self.EXPT_LOADED: self.expt.log_event("Food_Eaten")
                print("Yum!")

if __name__ == "__main__":
    print("NIDAQ_AVAILABLE: ", NIDAQ_AVAILABLE)
    GUIFunctions.openWhiskerEphys(NIDAQ_AVAILABLE)
    beh = BEH_GUI(NIDAQ_AVAILABLE)
    beh.BehavioralChamber()

import pygame
import threading
import whiskerTouchZMQ
import time
from RESOURCES.GUI_elements_by_flav import play_sound
import sys
import freezeAlg

def FAN_ON_OFF(self, events, FAN_ON, cur_time):
    if FAN_ON:
        log_event(self, events,"Fan_ON",cur_time)
        if self.NIDAQ_AVAILABLE:    self.fan.sendDBit(True)
    else:
        log_event(self, events,"Fan_OFF",cur_time)
        if self.NIDAQ_AVAILABLE:    self.fan.sendDBit(False)
        #self.fan.end()

def PLAY_TONE(self, events, TONE_ID, cur_time):
    # NOTE: Tone_OFF logged while drawing speeker above in main loop
    if TONE_ID == 'TONE1':
        log_event(self, events,"Tone_ON",cur_time,("Freq(Hz)", str(self.Tone1_Freq), "Vol(0-1)",str(self.Tone1_Vol), "Duration(S)",str(self.Tone1_Duration)))

        newThread = threading.Thread(target=play_sound, args=(self.Tone1_Freq, self.Tone1_Vol,self.Tone1_Duration))

    elif TONE_ID == 'TONE2':
        log_event(self, events,"Tone_ON",cur_time,("Freq(Hz)", str(self.Tone2_Freq), "Vol(0-1)",str(self.Tone2_Vol), "Duration(S)",str(self.Tone2_Duration)))
        newThread = threading.Thread(target=play_sound, args=(self.Tone2_Freq, self.Tone2_Vol,self.Tone2_Duration))

    newThread.start()
    self.TONE_TIME = cur_time
    self.TONE_ON = True

def CAB_LIGHT(self, events, ON_OFF, cur_time):
    gray        = (100,100,100)
    darkgray    = (50,50,50)
    if ON_OFF: # ON
       log_event(self, events,"Cabin Light ON",cur_time)
       Background_color = gray
       #self.cabin_light = daqAPI.cabinLightSetup()
       if self.NIDAQ_AVAILABLE:  self.cabin_light.sendDBit(True)

    else: # ON_OFF = False
       log_event(self, events,"Cabin Light OFF",cur_time)
       Background_color = darkgray
       if self.NIDAQ_AVAILABLE: self.cabin_light.sendDBit(False)
       #self.cabin_light.end()
    return Background_color


def EXTEND_LEVERS(self, events, text, L_LVR, R_LVR, cur_time):
    if L_LVR and R_LVR: # Extend both levers
        if self.NIDAQ_AVAILABLE:  self.leverOut.sendDByte(3)
        log_event(self, events, text, cur_time)
        self.LEVERS_EXTENDED = True
        self.R_LEVER_EXTENDED = True
        self.L_LEVER_EXTENDED = True

    elif L_LVR:  # Extend L lever only
        if self.NIDAQ_AVAILABLE:  self.leverOut.sendDByte(1)
        log_event(self, events, text, cur_time)
        self.LEVERS_EXTENDED = False
        self.R_LEVER_EXTENDED = False
        self.L_LEVER_EXTENDED = True
    elif R_LVR:  # Extend R lever only
        if self.NIDAQ_AVAILABLE:  self.leverOut.sendDByte(2)
        log_event(self, events, text, cur_time)
        self.LEVERS_EXTENDED = False
        self.R_LEVER_EXTENDED = True
        self.L_LEVER_EXTENDED = False
    else: # Retract both
        if self.NIDAQ_AVAILABLE:  self.leverOut.sendDByte(0)
        log_event(self, events, text, cur_time)
        self.LEVERS_EXTENDED = False
        self.R_LEVER_EXTENDED = False
        self.L_LEVER_EXTENDED = False

def L_CONDITIONING_LIGHT(self, events,ON_OFF,cur_time):
    if ON_OFF : # ON
       log_event(self, events,"Left_Light_ON",cur_time)
       if self.NIDAQ_AVAILABLE:  self.L_condition_Lt.sendDBit(True)

    else: # ON_OFF = False
       log_event(self, events,"Left_Light_OFF",cur_time)
       if self.NIDAQ_AVAILABLE:  self.L_condition_Lt.sendDBit(False)

def R_CONDITIONING_LIGHT(self, events,ON_OFF,cur_time):
    if ON_OFF: # ON
       log_event(self, events,"Right_Light_ON",cur_time)
       if self.NIDAQ_AVAILABLE:   R_condition_Lt.sendDBit(True)

    else: # ON_OFF = False
       log_event(self, events,"Right_Light_OFF",cur_time)
       if self.NIDAQ_AVAILABLE:   R_condition_Lt.sendDBit(False)

def Food_Light_ONOFF(self, events,ON_OFF,cur_time):
    gray = (100,100,100)
    black = (0,0,0)
    if ON_OFF: # ON
          fill_color = gray
          LEDsONOFF = "ON"
          log_event(self, events,"Feeder_Light_ON",cur_time)
          if self.NIDAQ_AVAILABLE:  self.food_light.sendDBit(True)

    else:
          fill_color = black
          LEDsONOFF = "OFF"
          if self.NIDAQ_AVAILABLE:  self.food_light.sendDBit(False)
          log_event(self, events,"Feeder_Light_OFF",cur_time)

    return fill_color,LEDsONOFF

def FOOD_REWARD(self, events, text,cur_time):
    log_event(self, events,text,cur_time)
    self.num_pellets +=1
    if self.NIDAQ_AVAILABLE:
        self.give_food.sendDBit(True)
        self.give_food.sendDBit(False)

def log_event(self, event_lst, event, cur_time, other=''):
    #print("Log file: ", self.log_file_path_name)
    event_string = str(cur_time) + ',  ' + event
    #print (event_string, other)
    event_other = ''
    for item in other:
        print (item)
        event_other = event_other + ",  " +  str(item)

    event_lst.append(event_string+event_other) # To Display on GUI
    try:
        #print(self.log_file_path_name)
        log_file = open(self.log_file_path_name,'a')         # OPEN LOG FILE
        log_file.write(event_string + event_other + '\n')   # To WRITE TO FILE
        log_file.close()                                #CLOSE LOG FILE
    except:
        print ('Log file not created yet. Check EXPT PATH, then Press "LOAD EXPT FILE BUTTON"')

def StartTouchScreen(self):
    if not self.TOUCH_TRHEAD_STARTED:
        whiskerThread = threading.Thread(target = whiskerTouchZMQ.main, args=(self.TSBack_q,self.TSq))#, kwargs=({'media_dir' : self.TOUCH_IMG_PATH}))
        whiskerThread.daemon = True
        whiskerThread.start()
        self.TOUCH_TRHEAD_STARTED = True

def MyVideo(self):
      vid_thread = threading.Thread(target=freezeAlg.runVid, args=(self.VIDq,self.VIDBack_q,))
      vid_thread.daemon = True
      self.VIDq.append(self.vidDict)
      vid_thread.start()

      while True:
          time.sleep(0.1)
          if not self.VIDBack_q.empty():
              msg = self.VIDBack_q.get()
              if msg == 'vid ready':
                  return


def exit_game(self):
    if self.NIDAQ_AVAILABLE:
      self.fan.end()
      self.cabin_light.end()
      self.food_light.end()
      self.give_food.end()
      eaten.end()

      self.leverOut.end()

      self.L_condition_Lt.end()
      self.R_condition_Lt.end()
      self.high_tone.end()
      self.L_nose_poke.end()
      self.R_nose_poke.end()
      self.checkPressLeft.end()
      self.checkPressRight.end()

    if self.vidDict['STATE'] == 'ON' or self.vidDict['STATE'] == 'REC':
        self.vidDict['STATE'] = 'STOP'
        self.VIDq.append(self.vidDict)
    if self.TOUCH_TRHEAD_STARTED == True:
        self.TSq.put('STOP')
    self.openEphysQ.put('STOP')
    pygame.quit()
    sys.exit()


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

def draw_camera( myscreen,fill_color, CAMERA_ON, REC, x, y, w,h, linew):
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

def draw_lighting( surface, SHOCK_ON, x,y,scale,color,width):
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

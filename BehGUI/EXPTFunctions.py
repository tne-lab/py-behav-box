import video_function
import whiskerTouch
import time
import threading
import GUIFunctions
####################################################################################
#   GET BOX INPUTS FROM GUI
####################################################################################
def checkStatus(self):

    # Maybe reset inputs?
    self.FOOD_EATEN = False
    self.LEVER_PRESSED_L = False
    self.LEVER_PRESSED_R = False
    self.NOSE_POKED_L = False
    self.NOSE_POKED_R = False


    # Get info from GUI
    self.LEVER_PRESSED_L = self.GUI.LEVER_PRESSED_L
    if self.LEVER_PRESSED_L:
        self.num_L_nose_pokes += 1
        self.log_event("Lever_Pressed_L")
    self.LEVER_PRESSED_R = self.GUI. LEVER_PRESSED_R
    if self.LEVER_PRESSED_R:
        self.num_R_lever_preses += 1
        self.log_event("Lever_Pressed_R")
    self.NOSE_POKED_L = self.GUI.NOSE_POKED_L
    if self.NOSE_POKED_L:
        self.num_L_nose_pokes += 1
        self.log_event("Nose_Poke_L")
    self.NOSE_POKED_R = self.GUI.NOSE_POKED_R
    if self.NOSE_POKED_R:
        self.num_R_nose_pokes += 1
        self.log_event("Nose_Poke_R")
    self.FOOD_EATEN = self.GUI.FOOD_EATEN
    if self.FOOD_EATEN:
        self.num_eaten +=1
        self.log_event("Food_Eaten")


    # Not sure what to do here. Reset self.GUI inputs?
    self.GUI.FOOD_EATEN = False
    self.GUI.LEVER_PRESSED_L = False
    self.GUI.LEVER_PRESSED_R = False
    self.GUI.NOSE_POKED_L = False
    self.GUI.NOSE_POKED_R = False

###########################################################################################################
# CHECK Qs
###########################################################################################################
def checkQs(self):
    # Handle Video
    if self.VID_ENABLED:
        #Check Vid Q
        if not self.VIDBack_q.empty():
            backDict = self.VIDBack_q.get()
            if backDict['FROZEN']: # FROZEN
                  # NOTE: this must be "debounced"
                  if not self.FROZEN_ALREADY_LOGGED:
                      self.log_event("Frozen",("Orig_NIDAQ_t",backDict['NIDAQ_time'],"video_time",backDict['vid_time'],"time_diff",backDict['Vid-NIDAQ']))
                      self.FROZEN_ALREADY_LOGGED = True
                      self.UNFROZEN_ALREADY_LOGGED = False

            else:  # UN FROZEN
                if self.PREVIOUSLY_FROZEN:
                   # NOTE: this must be "debounced"
                   if not self.UNFROZEN_ALREADY_LOGGED:
                        self.log_event("Unfrozen")
                        self.FROZEN_ALREADY_LOGGED = False
                        self.UNFROZEN_ALREADY_LOGGED = True
            if self.ROIstr == "":
                try:  # Get ROI value if it exists
                    self.ROIstr = backDict['ROI']
                    if self.ROIstr != "":
                        newROIstr = self.ROIstr.replace(",",";")
                        self.log_event("ROI:",(newROIstr + ",( x; y; width; height)"))
                        self.ROI_RECEIVED = True
                except:
                    pass

        ### UPDATE VID Q ###
        self.vidDict['cur_time'] = self.cur_time
        self.vidDict['trial_num'] = self.trial_num
        self.vidDict['STATE'] = self.vidSTATE
        self.vidDict['PATH_FILE'] = self.video_file_path_name
        self.vidDict['FLIP'] = self.FLIP
        self.vidDict['REC'] = self.RECORDING
        self.vidDict['ROI'] = self.ROI
        self.VIDq.append(self.vidDict)

    if self.EPHYS_ENABLED:
        ### CHECK OE Q ###
        if not self.openEphysBack_q.empty():
            OEMsg = self.openEphysBack_q.get()
            self.log_event(str(OEMsg))


###########################################################################################################
#  START THREADS FOR VID/TOUCHSCREEN
###########################################################################################################
def MyVideo(self):
    vid_thread = threading.Thread(target=video_function.runVid, args=(self.VIDq,self.VIDBack_q, self.freeze_file_path))
    vid_thread.daemon = True
    self.VIDq.pop()
    self.checkQs()
    vid_thread.start()

    while True:
      time.sleep(0.1)
      if not self.VIDBack_q.empty():
          msg = self.VIDBack_q.get()
          if msg == 'vid ready':
              return

####################################################################################
#   LOG EVENTS
####################################################################################
def log_event(self,event, event_other=''):
    cur_time = time.perf_counter() - self.Experiment_Start_time
    event_string = str(round(cur_time,9)) + ',  ' + event
    if len(event_other) > 0:
        event_other =  ",  "+ str(event_other)
    self.GUI.events.append(event_string+event_other) # To Display on GUI
    if len(self.GUI.events) > 14:  self.start_line = len(self.GUI.events) - 14
    try:
        self.log_file.write(event_string + event_other + '\n')   # To WRITE TO FILE
        print(event_string + event_other)                   # print to display
    except:
        print ('Log file not created yet. Check EXPT PATH, then Press "LOAD EXPT FILE BUTTON"')


####################################################################################
#   Make sure everything in box is back to false (Called with self.GUI)
####################################################################################
def resetBox(self):
    self.fan.sendDBit(False)
    self.cabin_light.sendDBit(False)
    if 'EPHYS-2' in self.computer:
        self.food_light.sendDBit(False)
        if self.expt.TOUCHSCREEN_USED:
            self.TSq.put('')
    #if 'EPHYS-1' in self.computer:
        #self.low_tone.sendDByte(0)

    self.L_condition_Lt.sendDBit(False)
    self.R_condition_Lt.sendDBit(False)

    GUIFunctions.EXTEND_LEVERS(self,"Levers_Retracted",False,False)

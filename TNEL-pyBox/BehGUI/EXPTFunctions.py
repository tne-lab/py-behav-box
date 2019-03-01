#import video_function
#import whiskerTouch
import time
####################################################################################
#   GET BOX INPUTS FROM GUI
####################################################################################
def checkStatus(self):
    self.LEVER_PRESSED_L = self.GUI.LEVER_PRESSED_L
    if self.LEVER_PRESSED_L:
        #self.num_L_lever_preses += 1
        self.log_event("Lever_Pressed_L")
    self.LEVER_PRESSED_R = self.GUI. LEVER_PRESSED_R
    if self.LEVER_PRESSED_R:
        #self.num_R_lever_preses += 1
        self.log_event("Lever_Pressed_R")
    self.NOSE_POKED_L = self.GUI.NOSE_POKED_L
    if self.NOSE_POKED_L:
        #self.num_L_nose_pokes += 1
        self.log_event("Nose_Poke_L")
    self.NOSE_POKED_R = self.GUI.NOSE_POKED_R
    if self.NOSE_POKED_R:
        #self.num_R_nose_pokes += 1
        self.log_event("Nose_Poke_R")
    if self.GUI.FOOD_EATEN:
        #self.num_eaten += 1
        self.log_event("Food_Eaten")
        self.GUI.FOOD_EATEN = False

    self.GUI.LEVER_PRESSED_L = False
    self.GUI. LEVER_PRESSED_R = False
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
                    newROIstr = self.ROIstr.replace(",",";")
                    print(newROIstr)
                    GUIFunctions.log_event(self, self.events,"ROI:",self.cur_time,(newROIstr + ",( x; y; width; height)"))
                except:
                    pass

        ### UPDATE VID Q ###
        self.vidDict['cur_time'] = self.cur_time
        self.vidDict['trial_num'] = self.trial_num
        self.vidDict['STATE'] = self.vidSTATE
        self.vidDict['PATH_FILE'] = self.video_file_path_name
        self.VIDq.append(self.vidDict)

    if self.EPHYS_ENABLED:
        ### CHECK OE Q ###
        if not self.openEphysBack_q.empty():
            OEMsg = self.openEphysBack_q.get()


###########################################################################################################
#  START THREADS FOR VID/TOUCHSCREEN
###########################################################################################################
def StartTouchScreen(self):
    i = 0
    '''
    if not self.TOUCH_TRHEAD_STARTED:
        whiskerThread = threading.Thread(target = whiskerTouch.main, args=(self.TSBack_q,self.TSq), kwargs={'media_dir' : self.resourcepath})
        whiskerThread.daemon = True
        whiskerThread.start()
        self.TOUCH_TRHEAD_STARTED = True
    '''

def MyVideo(self):
    i = 0
    '''
    vid_thread = threading.Thread(target=video_function.runVid, args=(self.VIDq,self.VIDBack_q,))
    vid_thread.daemon = True
    self.VIDq.pop()
    updateVideoQ(self)
    vid_thread.start()

    while True:
      time.sleep(0.1)
      if not self.VIDBack_q.empty():
          msg = self.VIDBack_q.get()
          if msg == 'vid ready':
              return
    '''
####################################################################################
#   LOG EVENTS
####################################################################################
def log_event(self,event, other=''):
    cur_time = time.perf_counter()
    event_string = str(round(cur_time,9)) + ',  ' + event

    event_other =  ",  "+ str(other)
    self.GUI.events.append(event_string+event_other) # To Display on GUI
    if len(self.GUI.events) > 14:  self.start_line = len(self.GUI.events) - 14
    try:
        self.log_file.write(event_string + event_other + '\n')   # To WRITE TO FILE
        print(event_string + event_other)                   # print to display
    except:
        print ('Log file not created yet. Check EXPT PATH, then Press "LOAD EXPT FILE BUTTON"')

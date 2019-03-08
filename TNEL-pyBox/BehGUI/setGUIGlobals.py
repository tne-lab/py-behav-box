#import cv2
import os
import pygame
import time
try:
    import daqAPI
except:
    pass
def setGUIGlobals(self):
    self.computer = os.environ['COMPUTERNAME']
    self.cur_time = time.perf_counter()
    ################################################################
    # GUI GLOBALS
    ################################################################
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    WINDOW_WIDTH = SCREEN_WIDTH - 100
    WINDOW_WCENTER = WINDOW_WIDTH/2
    WINDOW_HEIGHT = SCREEN_HEIGHT -100
    WINDOW_HCENTER = WINDOW_HEIGHT/2
    self.GAME_AREA = pygame.Rect(20, 10, WINDOW_WIDTH, WINDOW_HEIGHT)


    ################################################################
    # NIDAQ GLOBALS
    ################################################################
    if self.NIDAQ_AVAILABLE:
        # OUTPUTS
        self.fan = daqAPI.fanSetup()
        self.cabin_light = daqAPI.cabinLightSetup()
        self.leverOut = daqAPI.leverOutputSetup()
        if "EPHYS-2" in self.computer:
            self.food_light = daqAPI.foodLightSetup()
        self.give_food = daqAPI.giveFoodSetup()

        self.apply_shock = daqAPI.shockerSetup()
        if "EPHYS-1" in self.computer:#NOTE: Tones generated by PC in EPHIS-2 PC
            self.low_tone = daqAPI.lowToneSetup()
            #self.high_tone = daqAPI.highToneSetup()

        self.L_condition_Lt = daqAPI.conditioningLightsLeftSetup()
        self.R_condition_Lt = daqAPI.conditioningLightsRightSetup()


        # INPUTS
        self.L_nose_poke = daqAPI.leftNoseInputSetup()
        self.R_nose_poke = daqAPI.rightNoseInputSetup()
        self.checkPressLeft, self.checkPressRight = daqAPI.leverInputSetup()
        self.eaten = daqAPI.foodEatInputSetup()

        # Create stim thread
        #self.STIM_ENABLED = True
        #self.stimQ = Queue()
        #stimThread = threading.Thread(target=stimmer.Stim, args=(ADDRESS***, self.stimQ)) # NEED TO UPDATE ADDRESS


    ##################
    # DATA
    ##################
    cwd = os.getcwd()
    self.datapath = os.path.join(cwd,'DATA' )
    self.protocolpath = os.path.join(cwd,'PROTOCOLS' )
    self.resourcepath = os.path.join(cwd, 'RESOURCES')

    #self.expt_file_name = 'PROTOCOL_TOUCH_SCRN_TRAIN2' #Flav's Machine
    self.expt_file_name = 'PROTOCOL_BAR_PRESS_TRAIN-Ephys.txt'#Jean's Machine
    self.expt_file_path_name = os.path.join(self.protocolpath,self.expt_file_name )

    self.exptFileLines = []
    self.VIFileLines = []

    self.date = time.strftime("%b_%d_%y")#month-day-Year-H:M
    self.dateTm = time.strftime("%b_%d_%y-%H_%M")#month_day_Year-H:M
    self.exptTime = time.strftime("%H-%M")
    self.events = []

    ################################################################
    # EXPT DEFAULTS
    ################################################################
    self.EXPT_LOADED = False
    self.Expt_Name = ''
    self.Subject = ''
    self.prev_Subject = ''
    self.NAME_OR_SUBJ_CHANGED = False
    self.START_EXPT = False
    self.RESTART_EXPT = False
    self.TOUCH_TRHEAD_STARTED = False
    self.Expt_Count = 0

    ################################################################
    # TONE AND SHOCK DEFAULTS
    ################################################################
    self.globalsTone1_Duration = 1.0 # sec
    self.Tone1_Duration = 1.0 # sec
    self.Tone1_Freq = 1800.0
    self.Tone1_Vol = 1.0
    self.Tone2_Duration = 1.0 # sec
    self.Tone2_Freq = 1200.0
    self.Tone2_Vol = 1.0
    self.TONE_ON = False
    self.Shock_Duration = 1.0
    self.Shock_V = 9.0
    self.Shock_Amp = 0.5

    ################################################################
    # LEVERS
    ################################################################
    self.L_LEVER_EXTENDED = False
    self.R_LEVER_EXTENDED = False
    self.LEVERS_EXTENDED = False

    ## Get number of cameras
    self.num_cameras = 0#count_cameras()
'''
def count_cameras():
    max_tested = 2
    for i in range(max_tested):
        temp_camera = cv2.VideoCapture(i)
        if temp_camera.isOpened():
            temp_camera.release()
            continue
        return i + 1
'''

try:
    import daqAPI
except:
    pass

import pygame
import os
import time
from collections import deque
from queue import Queue

def setGlobals(self):
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
    # OUTPUTS
    if self.NIDAQ_AVAILABLE:
        self.fan = daqAPI.fanSetup()
        self.cabin_light = daqAPI.cabinLightSetup()
        self.leverOut = daqAPI.leverOutputSetup()
        self.food_light = daqAPI.foodLightSetup()
        self.give_food = daqAPI.giveFoodSetup()

        self.high_tone = daqAPI.highToneSetup()

        self.L_condition_Lt = daqAPI.conditioningLightsLeftSetup()
        self.R_condition_Lt = daqAPI.conditioningLightsRightSetup()


        #INPUTS
        self.L_nose_poke = daqAPI.leftNoseInputSetup()
        self.R_nose_poke = daqAPI.rightNoseInputSetup()
        self.checkPressLeft, self.checkPressRight = daqAPI.leverInputSetup()
        self.eaten = daqAPI.foodEatInputSetup()
    ##################
    # DATA
    ##################
    cwd = os.getcwd()
    print(cwd)
    self.datapath = os.path.join(cwd,'DATA' )
    print("....")
    print (self.datapath)

    self.expt_file_name = 'PROTOCOL_HABITUATION_AND_CONDITIONING.txt'
    self.expt_file_path_name = os.path.join(self.datapath,self.expt_file_name )
    print("EXPT FILE TO LOAD: ", self.expt_file_path_name)

    self.date = time.strftime("%b_%d_%y")#month-day-Year-H:M
    self.dateTm = time.strftime("%b_%d_%y-%H_%M")#month_day_Year-H:M
    self.exptTime = time.strftime("%H-%M")

    ##
    self.log_file_name = ''
    self.log_file_path_name = ''
    self.video_file_name = ''
    self.video_file_path_name = ''
    self.data_file_name = ''
    self.data_file_path_name = ''
    self.TOUCH_IMG_PATH = ''
    self.touch_img_files = []

    self.VIs_file_path = ''
    self.habituation_vi_times = []
    self.conditioning_vi_times = []
    self.extinction_vi_times = []
    self.recall_vi_times = []

    ################################################################
    # VIDEO GLOBALS
    ################################################################
    self.vidDict = {'STATE' : 'STOP'}
    self.VIDq = deque(maxlen = 1) # Most recent
    self.VIDBack_q = Queue()
    ################################################################
    # TOUCH GLOBALS
    ################################################################
    self.TSq = Queue()
    self.TSBack_q = Queue()
    self.TOUCH_TRHEAD_STARTED = False
    ################################################################
    # GENERAL GLOBALS
    ################################################################
    self.globalsTone1_Duration = 1.0 # sec
    self.Tone1_Duration = 1.0 # sec
    self.Tone1_Freq = 450.0
    self.Tone1_Vol = 1.0
    self.Tone2_Duration = 1.0 # sec
    self.Tone2_Freq = 1800.0
    self.Tone2_Vol = 0.5
    self.TONE_ON = False
    self.Shock_Duration = 1.0
    self.Shock_V = 9.0
    self.Shock_Amp = 0.5

    self.Expt_Name = '1'
    self.Subject ='1'
    self.trial_num = 0
    self.num_pellets = 0
    self.EXPT_FILE_LOADED = False

    self.setup = []
    self.protocol = []
    self.conditions = []

    self.L_LEVER_EXTENDED = False
    self.R_LEVER_EXTENDED = False
    self.LEVERS_EXTENDED = False
    self.TOUCHSCREEN_USED = False
    self.var_interval_reward = 0.0
    self.BAR_PRESS_INDEPENDENT_PROTOCOL = False

    self.open_ephys_started = False

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

        self.apply_shock = daqAPI.shockerSetup()
        self.low_tone = daqAPI.lowToneSetup()
        #self.high_tone = daqAPI.highToneSetup()

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
    self.protocolpath = os.path.join(cwd,'PROTOCOLS' )
    self.resourcepath = os.path.join(cwd, 'RESOURCES')
    print("....")
    print ("PROTOCOL PATH: ",self.protocolpath)

    self.expt_file_name = 'PROTOCOL_TOUCH_SCRN_TRAIN.txt'
    self.expt_file_path_name = os.path.join(self.protocolpath,self.expt_file_name )
    print("EXPT FILE TO LOAD: ", self.expt_file_path_name)

    self.exptFileLines = []
    self.VIFileLines = []

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
    self.TOUCH_TRAINING = False
    self.TOUCH_BANDIT = False
    self.touchImgCoords = []
    self.touchImgs = {}
    ################################################################
    # GENERAL GLOBALS
    ################################################################
    self.globalsTone1_Duration = 1.0 # sec
    self.Tone1_Duration = 5.0 # sec
    self.Tone1_Freq = 800.0
    self.Tone1_Vol = 1.0
    self.Tone2_Duration = 1.0 # sec
    self.Tone2_Freq = 1800.0
    self.Tone2_Vol = 0.5
    self.TONE_ON = False
    self.Shock_Duration = 1.0
    self.Shock_V = 9.0
    self.Shock_Amp = 0.5

    self.Expt_Name = ''
    self.Subject =''
    self.prev_Subject =''
    self.NAME_OR_SUBJ_CHANGED = False
    self.trial_num = 0
    self.num_pellets = 0
    self.EXPT_FILE_LOADED = False

    self.setup = []
    self.protocol = []
    self.conditions = []

    self.num_correct = 0
    self.num_wrong = 0
    self.num_no_action = 0
    self.percent = False
    self.wrongPercentage = 0
    self.correctPercentage = 0
    self.no_actionPercentage = 0
    self.check_correct = False
    self.check_wrong = False
    self.check_no_action = False

    self.L_LEVER_EXTENDED = False
    self.R_LEVER_EXTENDED = False
    self.LEVERS_EXTENDED = False
    self.TOUCHSCREEN_USED = False

    self.BAR_PRESS_INDEPENDENT_PROTOCOL = False
    self.VI_REWARDING = False
    self.var_interval_reward = 0.0
    self.VI_start = 0.0
    #################################
    self.BAR_PRESS_TRAINING = False
    self.background_touches = 0  #Num touches to background
    self.any_image_touches = 0
    self.correct_image_touches = 0
    self.TPM = 0.0   #Screen Touches per minute (background + image)
    self.TPMs = []
    self.TPMimg = 0.0   #Screen Touches per minute (touched images only)
    self.TPMimgs = []
    self.TPMcorrect_img = 0.0   #Screen Touches per minute (touched correct images only)
    self.TPMcorrect_imgs = []

    self.meanTPM10 = 0.0 #Running mean screen touches per min
    self.meanTPM10imgs = 0.0
    self.meanTPM10correct_imgs = 0.0
    self.VI_images = 0.0                # Used for Touch Training
    self.VI_background = 0.0            # Used for Touch Training
    self.cur_VI_images = 0.0              # Used for Touch Training
    self.cur_VI_background = 0.0        # Used for Touch Training

    self.cur_probability = 0.0  # Used for PELLET_VAR
    self.TPM_start_time = 0.0
    self.VI = 1.0
    ##################################
    self.VRs_given = 0
    self.VR = 1

    self.open_ephys_started = False
    self.Experiment_Start_time = 0.0
    self.cur_time = 0.0
    self.MAX_EXPT_TIME = 60 # in min

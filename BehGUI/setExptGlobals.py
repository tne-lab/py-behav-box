import time
from queue import Queue
import threading
import video_function
from collections import deque
def setExptGlobals(self):
    ################################################################
    # DATA FILES
    ################################################################
    self.exptFileLines = []
    self.VIFileLines = []

    self.date = time.strftime("%b_%d_%y")#month-day-Year-H:M
    self.dateTm = time.strftime("%b_%d_%y-%H_%M")#month_day_Year-H:M
    self.exptTime = time.strftime("%H-%M")
    self.cur_time =  time.perf_counter()

    ##
    self.log_file_name = ''
    self.log_file_path_name = ''
    self.data_file_name = ''
    self.data_file_path_name = ''
    self.freeze_file_path = ''

    ################################################################
    # GENERAL GLOBALS
    ################################################################
    self.trial_num = 0
    self.EXPT_FILE_LOADED = False
    self.RECORDING = False
    self.MASTER_PAUSE = False

    ################################################################
    # STIM PARAMETERS
    ################################################################
    self.NUM_PULSE_X = 0
    self.NUM_PULSE_Y = 0
    self.stimAddressY = 'Dev3/ao1'
    self.stimAddressX = 'Dev3/ao0'
    self.stimX = None
    self.stimY = None
    self.stim = None # Stim thread to none
    self.CL_Enabled = False
    self.phaseDelay = 0
    self.paramDelay = 0
    self.paramDelayVar = 0

    ################################################################
    # EXPERIMENT PARAMETERS
    ################################################################
    self.setup = []
    self.protocol = []
    self.conditions = []
    self.Protocol_ln_num = 0
    self.loop = 0
    self.Protocol_loops = 0
    self.LOOP_FIRST_PASS = True
    self.CONDITONS_NOT_SET = True
    self.CONDITION_STARTED = False
    self.RUN_SETUP = False
    self.START_EXPT = False

    ################################################################
    # EXPERIMENT PARAMETERS
    ################################################################
    self.TTL_LEVER_L = 0
    self.TTL_LEVER_R = 0
    self.TLL_NOSE_L = 0
    self.TLL_NOSE_R = 0
    self.TLL_FOOD = 0

    self.TTL_ON = []

    ################################################################
    # OUTCOME STATS
    ################################################################
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
    self.cur_probability = 0.0  # Used for PELLET_VAR

    self.num_L_nose_pokes = 0
    self.num_R_nose_pokes = 0
    self.num_L_lever_preses = 0
    self.num_R_lever_preses = 0
    self.num_eaten = 0
    self.num_pellets = 0

    ################################################################
    # VI
    ################################################################
    self.VI_REWARDING = False
    self.var_interval_reward = 0.0
    self.VI_start = 0.0
    self.VI_initial = 1
    self.VI_final = 30
    self.VI_images = 0.0                # Used for Touch Training
    self.VI_background = 0.0            # Used for Touch Training
    self.cur_VI_images = 0.0              # Used for Touch Training
    self.cur_VI_background = 0.0        # Used for Touch Training
    self.VI = 1.0
    self.VIs_file_path = ''
    self.habituation_vi_times = []
    self.conditioning_vi_times = []
    self.extinction_vi_times = []
    self.recall_vi_times = []
    self.VI_start = 0.0       # To see if VI time has passed
    self.VI_calc_start = 0.0  # To recalc PRESSES PER MINUTE every minute
    self.VI_index = 0

    ################################################################
    # Touches Per Minute
    ################################################################
    self.num_bar_presses = 0
    self.bar_press_time = 0.0
    self.BPPM = 0.0   #Screen Touches per minute (background + image)
    self.BPPMs = []
    self.TPM = 0.0   #Screen Touches per minute (background + image)
    self.TPMs = []
    self.TPMimg = 0.0   #Screen Touches per minute (touched images only)
    self.TPMimgs = []
    self.TPMcorrect_img = 0.0   #Screen Touches per minute (touched correct images only)
    self.TPMcorrect_imgs = []
    self.meanTPM10 = 0.0 #Running mean screen touches per min
    self.meanTPM10imgs = 0.0
    self.meanTPM10correct_imgs = 0.0
    self.TPM_start_time = 0.0

    ################################################################
    # VR
    ################################################################
    self.VRs_given = 0
    self.VR = 1
    self.VR_initial = 0
    self.VR_final = 30

    ################################################################
    # Timing Stuff
    ################################################################
    self.Experiment_Start_time = 0.0
    self.cur_time = 0.0
    self.MAX_EXPT_TIME = 60 # in min

    ################################################################
    # PAUSE
    ################################################################
    self.EAT_TO_START = False
    self.BARPRESS_TO_START = False
    self.NOSEPOKE_TO_START = False

    ################################################################
    # What are we using for this EXPT? (Gets set in load_expt_file())
    ################################################################
    self.EPHYS_ENABLED = False
    self.VID_ENABLED = False
    self.TOUCHSCREEN_USED = False
    self.BAR_PRESS_INDEPENDENT_PROTOCOL = False
    self.BAR_PRESS_TRAINING = False

    ################################################################
    # AUX CAMERA (Only starts if second camera is exists)
    ################################################################
    self.SIMPLEVIDq = Queue()
    simpleVidThread = threading.Thread(target=video_function.runSimpleVid, args=(self.SIMPLEVIDq,))
    simpleVidThread.start()

    ################################################################
    # PAUSE
    ################################################################
    self.PAUSE_STARTED = False
    self.TOUCHED_TO_START_TRIAL = False
    self.START_IMG_PLACED = False

    self.setVidGlobals()
    ################################################################
    # VIDEO GLOBALS
    ################################################################
def setVidGlobals(self):
    self.VID_ENABLED = True
    self.vidDict = {'STATE' : 'STOP'}
    self.VIDq = deque(maxlen = 1) # Most recent
    self.VIDBack_q = Queue()
    self.video_file_name = ''
    self.video_file_path_name = ''
    self.ROIstr = ""
    self.vidSTATE= ''
    self.FLIP = False
    self.FROZEN_ALREADY_LOGGED = False #Used for "DEBOUNCING" Frozen msg from video
    self.UNFROZEN_ALREADY_LOGGED = False #Used for "DEBOUNCING" Frozen msg from video
    self.FREEZE_DETECTION_ENABLED = False
    self.PREVIOUSLY_FROZEN = False #Used to prevent 'unfrozen' from being logged prior to first 'frozen' event
    self.ROI = ""
    self.ROI_RECEIVED = False
    if "EPHYS-2" in self.GUI.computer:
        self.FLIP = True


    ################################################################
    # TOUCH GLOBALS
    ################################################################
def setTouchGlobals(self):
    self.TOUCHSCREEN_USED = True
    self.TOUCH_TRAINING = False
    self.TOUCH_BANDIT = False
    self.touchImgCoords = []
    self.touchImgs = {}
    self.touch_time = 0.0
    self.RANDOM_IMG_COORDS = False
    self.touchMsg = []
    self.background_hits = []
    self.wrong_img_hits = []
    self.correct_img_hits = []
    self.background_touches = 0  #Num touches to background
    self.any_image_touches = 0
    self.correct_image_touches = 0
    self.TOUCH_IMG_PATH = ''
    self.touch_img_files = []
    self.TOUCH_IMAGES_SENT = False
    self.SPAL = False

def setExptGlobals(self):
    ################################################################
    # DATA FILES
    ################################################################
    self.exptFileLines = []
    self.VIFileLines = []

    self.date = time.strftime("%b_%d_%y")#month-day-Year-H:M
    self.dateTm = time.strftime("%b_%d_%y-%H_%M")#month_day_Year-H:M
    self.exptTime = time.strftime("%H-%M")

    ##
    self.log_file_name = ''
    self.log_file_path_name = ''
    self.data_file_name = ''
    self.data_file_path_name = ''

    ################################################################
    # GENERAL GLOBALS
    ################################################################
    self.Expt_Name = ''
    self.Subject = ''
    self.prev_Subject = ''
    self.NAME_OR_SUBJ_CHANGED = False
    self.trial_num = 0
    self.EXPT_FILE_LOADED = False

    ################################################################
    # EXPERIMENT PARAMETERS
    ################################################################
    self.setup = []
    self.protocol = []
    self.conditions = []

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

    self.L_LEVER_EXTENDED = False
    self.R_LEVER_EXTENDED = False
    self.LEVERS_EXTENDED = False

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
    # What are we using for this EXPT? (Gets set in load_expt_file())
    ################################################################
    self.EPHYS_ENABLED = True
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
    # More to parse and make sure work
    ################################################################
    self.cur_time =  time.perf_counter()

    self.Protocol_ln_num = 0
    self.loop = 0
    self.Protocol_loops = 0
    self.LOOP_FIRST_PASS = True
    self.CONDITONS_NOT_SET = True
    self.CONDITION_STARTED = False
    self.RUN_SETUP = False
    self.VI_index = 0
    self.PAUSE_STARTED = False

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
    self.ROI = (0,0,0,0)
    self.vidSTATE= ''


    ################################################################
    # TOUCH GLOBALS
    ################################################################
def setTouchGlobals(self):
    self.TOUCHSCREEN_USED = True
    self.TSq = Queue()
    self.TSBack_q = Queue()
    self.TOUCH_TRHEAD_STARTED = False
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
    self.PREVIOUSLY_FROZEN = False #Used to prevent 'unfrozen' from being logged prior to first 'frozen' event
    self.FROZEN_ALREADY_LOGGED = False #Used for "DEBOUNCING" Frozen msg from video
    self.UNFROZEN_ALREADY_LOGGED = False #Used for "DEBOUNCING" Frozen msg from video

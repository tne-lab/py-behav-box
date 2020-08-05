from RESOURCES.GUI_elements_by_flav import convertString
import os
import subprocess
import GUIFunctions
import time
import webbrowser
import win32gui
import shutil
import numpy as np

def get_val_between_equal_sign_and_hash(line):
    try:
        Left_right = line.split('=')
        right = Left_right[1].strip()
        new_Left_right = right.split('#') #IGNORES "#" FOLLOWED BY COMMENTS
        val = new_Left_right[0].strip()  # comment = left_right[1].strip()
        return val
    except:
        print("Could not parse line1:", line)
        return False

def get_LR_before_hash(line):
    try:
        left_right = line.split('=')
        left = left_right[0].strip()
        if len(left_right) > 1 : right = left_right[1].strip()
        else:  right = ''
        new_left_right = right.split('#') #IGNORES "#" FOLLOWED BY COMMENTS
        right = new_left_right[0].strip()  # comment = left_right[1].strip()
        #if len(new_left_right) > 1: print("Comment: ",new_left_right[1] )
        return left,right
    except:
        print("Could not parse line2:", line)
        return left
def get_before_hash(line):
    clean_line = line.strip()
    try:
        left = clean_line.split('#') #IGNORES "#" FOLLOWED BY COMMENTS
        new_left = left[0].strip()  #  # Remove leading and trailoing blanks and \n
        return new_left
    except:
        print("Could not parse line3:", line)
        return clean_line


def load_expt_file(self):
    try:
        currentlySetting = None
        f = open(self.GUI.expt_file_path_name,'r')
        # Read Line by line
        EXPERIMENT = False
        self.config_file_path = ''
        for ln in f:
            str_before_equal, str_after_equal = get_LR_before_hash(ln)
            line = get_before_hash(ln)

            if (not EXPERIMENT) and (currentlySetting!='STIM'): # Makes sure that path is correct
                str_after_equal = str_after_equal.upper()
                str_before_equal = str_before_equal.upper()

            self.exptFileLines.append(line)

            if str_before_equal != "" and str_before_equal[0] != "#" : #Skip Blank Lines and Skip lines that are just comments (but still copy them to new file)
                if '[EXPERIMENT' in str_before_equal:
                    currentlySetting = 'EXPERIMENT'
                elif '[OPEN_EPHYS' in str_before_equal:
                    currentlySetting = 'OPEN_EPHYS'
                elif '[TONE1' in str_before_equal:
                    currentlySetting = 'TONE1'
                elif '[TONE2' in str_before_equal:
                    currentlySetting = 'TONE2'
                elif '[SHOCK]' in str_before_equal:
                    currentlySetting = 'SHOCK'
                elif '[FREEZE]' in str_before_equal:
                    currentlySetting = 'FREEZE'
                elif '[TOUCHSCREEN]' in str_before_equal:
                    currentlySetting = 'TOUCHSCREEN'
                    self.setTouchGlobals()
                elif '[BAR_PRESS]' in str_before_equal:
                    currentlySetting = 'BARPRESS'
                elif '[STIM]' in str_before_equal:
                    currentlySetting = 'STIM'
                elif '[ERP]' in str_before_equal:
                    currentlySetting = 'ERP'
                elif '[PROTOCOL' in str_before_equal:
                    currentlySetting = 'PROTOCOL'
                elif '[PARAMETER_SWEEPING' in str_before_equal:
                    currentlySetting = 'PARAMETER_SWEEPING'
                elif '[OPEN_LOOP' in str_before_equal:
                    currentlySetting = 'OPEN_LOOP'
                elif '[CLOSED_LOOP' in str_before_equal:
                    currentlySetting = 'CLOSED_LOOP'
                elif '[SETUP' in str_before_equal:
                    currentlySetting = 'SETUP'
                elif "[CONDITIONS" in str_before_equal:
                    print("#####################")
                    print("#    CONDITIONS     #")
                    print("#####################")
                    currentlySetting = 'CONDITIONS'
                elif '[END' in str_before_equal:
                    currentlySetting = 'END'

                if currentlySetting == 'EXPERIMENT':
                    if 'EXPT_NAME' in str_before_equal:
                        print("#####################")
                        print("#    EXPERIMENT     #")
                        print("#####################")
                        #if self.GUI.Expt_Name == "": #Change only if it does not already exist
                        self.GUI.Expt_Name = str_after_equal
                        print(self.GUI.Expt_Name)

                    elif 'SUBJECT' in str_before_equal:
                        self.GUI.Subject = str_after_equal
                        print(self.GUI.Subject)

                    elif 'EXPT_PATH' in str_before_equal:
                        self.GUI.datapath = str_after_equal
                        if not os.path.isdir(self.GUI.datapath):
                            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print(self.GUI.datapath, " DOES NOT EXIST!!!!")
                            print("Please correct the path in your protocol file!")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                            self.log_event(self.GUI.datapath + " DOES NOT EXIST!!!!")
                            self.log_event("PLEASE CHECK PATH IN PROTOCOL FILE")
                            return False
                        else: print(self.GUI.datapath)

                    elif 'LOG_FILE_PATH' in str_before_equal:
                        log_file_path = str_after_equal
                        if not os.path.isdir(log_file_path):
                            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print(log_file_path, " DOES NOT EXIST!!!!")
                            print("Please correct the path in your protocol file!")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                            self.log_event(log_file_path + " DOES NOT EXIST!!!!")
                            return False
                        else: print("Log File Path",log_file_path)

                    elif 'VIDEO_FILE_PATH' in str_before_equal:
                        video_file_path = str_after_equal
                        if not os.path.isdir(video_file_path):
                            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print(video_file_path, " DOES NOT EXIST!!!!")
                            print("Please correct the path in your protocol file!")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                            self.log_event(video_file_path + " DOES NOT EXIST!!!!")
                            return False
                        print(video_file_path)

                    elif 'VI_TIMES_LIST_PATH' in str_before_equal:
                        self.VIs_file_path = str_after_equal
                        print(self.VIs_file_path)

                elif currentlySetting == 'OPEN_EPHYS':
                    if "OPEN_EPHYS_CONFIG_FILE" in str_before_equal:
                        self.config_file_path = str_after_equal

                    elif 'OPEN_EPHYS_PATH' in str_before_equal:
                        if self.GUI.NIDAQ_AVAILABLE:
                            win32gui.EnumWindows(GUIFunctions.lookForProgram, 'Open Ephys GUI')
                            if GUIFunctions.IsOpenEphysRunning:
                                win32gui.EnumWindows(GUIFunctions.killProgram, 'Open Ephys GUI')
                                time.sleep(0.5)
                            if self.config_file_path != '':
                                dest = shutil.copy(os.getcwd() + '\\RESOURCES\\CONFIGS\\' + self.config_file_path, str_after_equal[:-14] + 'lastConfig.xml')
                                print('moved config file to oe dir : ', dest)
                            oe = str_after_equal
                            window = subprocess.Popen(oe)# # doesn't capture output
                            time.sleep(0.5)
                            win32gui.EnumWindows(GUIFunctions.lookForProgram, 'Open Ephys GUI')
                            if GUIFunctions.IsOpenEphysRunning:
                                self.EPHYS_ENABLED = True

                    elif 'TTL_LEVER_R' == str_before_equal:
                        self.TTL_LEVER_L = str_after_equal

                    elif 'TTL_LEVER_L' == str_before_equal:
                        self.TTL_LEVER_R = str_after_equal

                    elif 'TTL_NOSE_L' == str_before_equal:
                        self.TTL_NOSE_L = str_after_equal

                    elif 'TTL_NOSE_R' == str_before_equal:
                        self.TTL_NOSE_R = str_after_equal

                    elif 'TTL_FOOD' == str_before_equal:
                        self.TTL_NOSE_L = str_after_equal

                elif currentlySetting == 'TONE1':#TONE1
                    if 'DURATION' in str_before_equal:
                        self.GUI.Tone1_Duration = float(str_after_equal)
                        print("self.Tone1_Duration",self.GUI.Tone1_Duration)

                    if 'FREQ' in str_before_equal:
                        self.GUI.Tone1_Freq = float(str_after_equal)
                        print("self.Tone1_Freq: ",self.GUI.Tone1_Freq)

                    if 'VOL' in str_before_equal:
                        self.GUI.Tone1_Vol = float(str_after_equal)
                        print("self.Tone1_Vol: ",self.GUI.Tone1_Vol)

                elif currentlySetting == 'TONE2':#TONE2
                    if 'DURATION' in str_before_equal:
                        self.GUI.Tone2_Duration = float(str_after_equal)
                        print("self.Tone2_Duration",self.GUI.Tone2_Duration)

                    if 'FREQ' in str_before_equal:
                        self.GUI.Tone2_Freq = float(str_after_equal)
                        print("self.Tone2_Freq: ",self.GUI.Tone2_Freq)

                    if 'VOL' in str_before_equal:
                        self.GUI.Tone2_Vol = float(str_after_equal)
                        print("self.Tone2_Vol: ",self.GUI.Tone2_Vol)

                elif currentlySetting == 'TOUCHSCREEN':
                    if '[TOUCHSCREEN]' in str_before_equal:
                        self.SKIP_MISSES = False
                    if 'IMAGES_PATH' in str_before_equal:
                        self.TOUCH_IMG_PATH = str_after_equal

                    if 'COORDS' in str_before_equal:
                        self.BANDIT_TRAINING = False
                        words = str_after_equal
                        if "RANDOM" in words:
                            self.RANDOM_IMG_COORDS = True # self.touchImgCoords will be made radom in BehGUI.py
                        elif "BANDIT_TRAINING" in words:
                            self.BANDIT_TRAINING = True
                            self.cur_img_coords = []
                            self.cur_img_coords_index = 0
                            coordSets = words.split('%')[1:]
                            for coord in coordSets:
                                imageCoords = coord.split(':') # get rid of words before first ':'
                                touchImgCoords = []
                                for i in range(len(imageCoords)): # Loop through coord list
                                    for c in '()':#Remove parenthesis from (x,y)
                                        imageCoords[i] = imageCoords[i].replace(c, "")

                                    imageCoordsStr = imageCoords[i].split(",")
                                    touchImgCoords.append((int(imageCoordsStr[0]), int(imageCoordsStr[1])))
                                self.cur_img_coords.append(touchImgCoords)
                        else:
                            self.prev_img_loc_index = [-1, -1]
                            imageCoords = words.split(':')
                            for i in range(len(imageCoords)): # Loop through coord list
                                for c in '()':#Remove parenthesis from (x,y)
                                    imageCoords[i] = imageCoords[i].replace(c, "")

                                imageCoordsStr = imageCoords[i].split(",")
                                self.touchImgCoords.append((int(imageCoordsStr[0]), int(imageCoordsStr[1])))

                    elif 'IMG' in str_before_equal:
                        words = str_after_equal
                        imageInfo = words.split(":")
                        imageName = imageInfo[0].strip()
                        if len(imageInfo)>1: # There are probability values after ":", i.e. (20,20,20,20,20)
                            for c in '()': #Remove parenthesis from rewards
                                imageInfo[1] = imageInfo[1].replace(c, "")
                            imgRewardsList = []
                            for probability in imageInfo[1].split(","):
                                if "X" in probability or "x" in probability: # There is a'X' in probability values, i.e. (20x10,80x10,...)
                                    for x in 'Xx':
                                        if x in probability:
                                            Xsplit = probability.split(x)
                                        prob = Xsplit[0]
                                        num = Xsplit[1]
                                        for i in range(int(num)):
                                            imgRewardsList.append(int(prob))
                                else:
                                    imgRewardsList.append(int(probability))
                            # Saving as dictionary with key as filename
                            # and value as list of reward probability per trial
                            self.touchImgs[imageName] = imgRewardsList
                        else:
                            # TRAINING TO TOUCH
                            # Saving as dictionary with key as filename
                            # and this means we're training so reward probability is hard coded in BEH_GUI_MAIN
                            self.touchImgs[imageName] = 0
                    elif 'TRAIN_TOUCH' in str_before_equal:
                        self.TOUCH_TRAINING = True
                        vis = str_after_equal
                        if len(vis) > 0:
                            VIs = vis.split(",")
                            self.VI_images = float(VIs[0].strip())
                            self.cur_VI_images = self.VI_images
                            self.VI_background = float(VIs[1].strip())
                            self.cur_VI_background = self.VI_background

                        #self.cur_probability = 100.0 # 100% To start. Reduced by 15% after 10 Presses/min for 10 min in BEH_GUI_MAIN
                    elif 'TOUCH_BANDIT' in str_before_equal:
                        self.TOUCH_BANDIT = True

                    elif 'SPAL' == str_before_equal:
                        self.SPAL = True
                        self.DesImgCoords = {}
                        i = 0
                        for img in self.touchImgs:
                            self.DesImgCoords[img] = self.touchImgCoords[i]
                            i=i+1

                    elif 'SKIP_MISSES' == str_before_equal:
                        self.SKIP_MISSES = True


                elif currentlySetting == 'BARPRESS':
                    self.BAR_PRESS_INDEPENDENT_PROTOCOL = True
                    if "VI" in str_before_equal: # Needs to line befroe = sign
                        self.VI_REWARDING = True
                        VI = str_after_equal
                        try:
                            self.var_interval_reward = int(VI)
                            print("var_interval_reward: ",self.var_interval_reward)
                        except:
                            print ("!!!!!!!!!!!VI must = a number in EXP PROOCOL file (VI=15 )!!!!!!!!!!!!!!")

                    if "BAR_PRESS_TRAIN" in str_before_equal:
                        self.BAR_PRESS_TRAINING = True
                        vis = str_after_equal
                        if len(vis) > 0 and "VI(" in vis: #BAR_PRESS_TRAIN=VI(1,15) needs to line after = sign
                            VIs = vis.split(",")
                            VI_intial = VIs[0][3:]
                            print("VI_INITIAL: ",VI_intial)
                            self.var_interval_reward = float(VI_intial)
                            #self.VI = self.VI_initial
                            VI_final = VIs[1][:-1]
                            print("VI_final: ",VI_final)
                            self.VI_final =  float(VI_final)
                        if len(vis) > 0 and "VR(" in vis:
                            VRs = vis.split(",")
                            VR_intial = VRs[0][3:]
                            print("VR_INITIAL: ",VR_intial)
                            self.var_interval_reward = float(VR_intial)
                            VR_final = VRs[1][:-1]
                            print("VR_final: ",VR_final)
                            self.VR_final =  float(VR_final)
##                        self.VR=1
##                        VR = get_val_between_equal_sign_and_hash(line)
##                        # (10, 1,30,5) creates 10 variable ratio reward stating at every press (1, to random between (1,30) incremented by 5 every loop)
##                        try:
##                            self.var_ratio_reward = VR
##                            print("var_RATIO_reward: ",self.var_ratio_reward)
##                        except:
##                            print ("!!!!!!!!!!!VR must have the form '(10, 1,30,5)' in EXP PROOCOL file!!!!!!!!!!!!!!")

                elif currentlySetting == "STIM":
                    if 'STIM_ADDRESS_X' == str_before_equal or 'STIM_ADDRESS' == str_before_equal:
                        self.stimAddressX = str_after_equal
                    if 'STIM_ADDRESS_Y' == str_before_equal or 'STIM_ADDRESS_SHAM' == str_after_equal:
                        self.stimAddressY = str_after_equal

                elif currentlySetting == 'CLOSED_LOOP':
                    if '[CLOSED_LOOP]' == str_before_equal: # Defaults, should do this for all!
                        self.CLCHANNEL = 1
                        self.CLMicroAmps = 100
                        self.CLLag = 0 # Default as fast as possible (milliseconds)
                        self.CLTimer = 30 # probably won't use this? Use experiment protocol Closed_loop = 30 to run for 30 minutes
                        self.CLTimeout = 1
                        self.CLTimeoutVar = 0.2
                        self.CL_Enabled = False
                    if 'EVENTCHANNEL' in str_before_equal:
                        self.CLCHANNEL = str_after_equal
                    if 'MICROAMPS' in str_before_equal:
                        self.CLMicroAmps = int(str_after_equal)
                    if 'STIM_LAG' in str_before_equal: # note 7.5ms delay here
                        stimLag = float(str_after_equal)
                        if stimLag < 7.5:
                            self.CLLag = 0
                        else:
                            self.CLLag = (stimLag - 7.5)/1000.0
                    if 'TIMER' == str_before_equal: #
                        self.CLTimer = float(str_after_equal)
                    if 'TIMEOUT' == str_before_equal:
                        self.CLTimeout = float(str_after_equal)
                    if 'TIMEOUT_VAR' == str_before_equal:
                        self.CLTimeoutVar = float(str_after_equal)



                elif currentlySetting == 'ERP':
                    if '[ERP]' == str_before_equal: # Defaults, should do this for all!
                        self.INTER_PULSE_WIDTH = 4
                        self.PULSE_VAR = 1
                        self.NUM_ERP_PULSE = 2
                        self.NUM_ERP_LOCATIONS = 2
                    if 'INTER_PULSE_WIDTH' == str_before_equal:
                        self.INTER_PULSE_WIDTH = float(str_after_equal)
                    if 'PULSE_VAR' == str_before_equal:
                        self.PULSE_VAR = float(str_after_equal)
                    if 'NUM_PULSE' == str_before_equal:
                        self.NUM_ERP_PULSE = int(str_after_equal)
                    if 'NUM_LOCATIONS' == str_before_equal:
                        self.NUM_ERP_LOCATIONS = int(str_after_equal)

                elif currentlySetting == 'OPEN_LOOP':
                    if "PHASE_DELAY" == str_before_equal:
                        self.openLoopPhaseDelay = float(str_after_equal)

                elif currentlySetting == 'PARAMETER_SWEEPING':
                    if "INTENSITY" == str_before_equal:
                        for c in '()':#Remove parenthesis from (x,y)
                            str_after_equal = str_after_equal.replace(c, "")

                        self.intensityArray = np.asarray(str_after_equal.split(","), dtype=np.float64)
                    if "DURATION" == str_before_equal:
                        for c in '()':#Remove parenthesis from (x,y)
                            str_after_equal = str_after_equal.replace(c, "")

                        self.durationArray = np.asarray(str_after_equal.split(","), dtype=np.float64)
                    if "DELAY" == str_before_equal:
                        self.paramDelay = float(str_after_equal)
                    if "DELAY_VAR" == str_before_equal:
                        self.paramDelayVar = float(str_after_equal)
                    if "SET_SIZE" == str_before_equal:
                        self.paramSetSize = int(str_after_equal)

                elif currentlySetting == 'SHOCK':
                    if 'DURATION' in str_before_equal:
                        self.GUI.Shock_Duration = float(str_after_equal)
                        print(self.GUI.Shock_Duration)

                    if 'VOLTS' in str_before_equal:
                        self.GUI.Shock_V = float(str_after_equal)
                        print(self.GUI.Shock_V)

                    if 'AMPS' in str_before_equal:
                        self.GUI.Shock_Amp = float(str_after_equal)
                        print(self.GUI.Shock_Amp)

                elif currentlySetting == 'FREEZE':
                    print("###################################")
                    print("#    FREEZE DETECTION ENABLED     #")
                    print("###################################")
                    self.FREEZE_DETECTION_ENABLED = True
                    if 'DURATION' in str_before_equal:
                        Freeze_Duration = str_after_equal
                        #print(Freeze_Duration)
                    if 'PIX' in str_before_equal:
                        Min_Pixels = str_after_equal
                        #print(Min_Pixels)

                    if 'ROI' in str_before_equal:  #key == 'ROI':  # THIS SHOULD BE IN LOAD PROTOCOL ONLY WHEN and WHERE FREEZE INFO IS GIVEN
                        self.ROI = str_after_equal
                        if "GENERATE" in self.ROI:
                            print("ROI: ",self.ROI)
                        else:
                            print("ROI COORINATES: ",self.ROI)
                            print('freeze detection assumed')

                elif currentlySetting == 'SETUP':
                    if "SETUP" in str_before_equal: # Skips [header] line
                        print("################")
                        print("#    SETUP     #")
                        print("################")
                    else:
                        try:
                            word1,word2 = get_LR_before_hash(line)
                            self.setup.append({word1:word2})
                            print({word1:word2})
                            if word1 == "CAMERA" and word2:
                                self.setVidGlobals()
                        except:
                            self.setup.append({line:True}) # For lines without an '=' in them
                            #if line == 'END': PROTOCOL = False



                elif currentlySetting == 'PROTOCOL':
                    #print("self.protocol: ",line)
                    if "PROTOCOL"  in str_before_equal: # Skips [header] line
                        print("###################")
                        print("#    PROTOCOL     #")
                        print("###################")
                    else:
                        try:
                            word1,word2 = get_LR_before_hash(line)
                            self.protocol.append({word1:word2})
                            print({word1:word2})
                        except:
                            #print("single word")
                            self.protocol.append({line:True}) # For lines without an '=' in them
                            #if line == 'END': self.protocol = False


                elif currentlySetting == 'CONDITIONS':
                    #print("self.conditions: ",line)
                    if "[CONDITIONS]" in str_before_equal: # Condition header line
                        KEY_LINE = True

                    elif KEY_LINE: # CONDITION HEADING (i.e. all the KEYS)
                        keys = line.split(',') #list of condtions but need to be stripped of blanks and tabs
                        #print ("KEYS: ", keys)
                        KEY_LINE = False
                    else: # Not a CONDITION heading line, (i.e. all the VALUES)
                        condition={}
                        values = line.split(',')
                        #print ("VALUES: ",values)

                        i=0
                        for val in values:
                            val = val.strip()
                            val = val.upper()
                            val = convertString(val)
                            condition[keys[i].strip()] = val #This strips keys, assigns a val to the key and creates condition dict

                            i+=1
                        self.conditions.append(condition)
                        print (condition)
                else:
                    END_PROTOCOL = True
            else:# line == ""
                print("BLANK LINE")

        f.close()
        print(".......\n")
    except OSError:
        print("NO SUCH FILE!!!!",self.expt_file_path_name)
        return False

    print("\n#########################")
    print("#   EXPT FILE LOADED!!    #")
    print("###########################")

    for dct in self.protocol:
        for k,v in dct.items():
            print(str(k)+" = " + str(v))
    print(".................................\n")

    if self.VIs_file_path != "":
        print("Loading VIs ...")
        try:
            #path,name = os.path.split(self.VIs_file_path)
            #VIs_file_path_COPY = name[:-4] + '_copy.txt'
            #VIs_file_path_COPY = os.path.join(self.newdatapath,VIs_file_path_COPY)
            f = open(self.VIs_file_path,'r')
            #fw = open(VIs_file_path_COPY,'w')
            # Read Line by line
            for line in f:
                #fw.write(line)
                self.VIFileLines.append(line)
                line = line.strip() # Remove leading and trailoing blanks and \n
                line = line.upper()
                print(line)
                if "HABITUATION" in line:
                    words = line.split(':')
                    words = words[1].strip()
                    words = words.split(',')
                    #print("length of words: ",len(words))
                    for items in words:
                        num = items.strip()
                        #print(num)
                        self.habituation_vi_times.append(int(num))
                if "CONDITIONING" in line:
                    words = line.split(':')
                    words = words[1].strip()
                    words = words.split(',')
                    #print("length of words: ",len(words))
                    for items in words:
                        num = items.strip()
                        #print(num)
                        self.conditioning_vi_times.append(int(num))
                if "EXTINCTION" in line:
                    words = line.split(':')
                    words = words[1].strip()
                    words = words.split(',')
                    #print("length of words: ",len(words))
                    for items in words:
                        num = items.strip()
                        #print(num)
                        self.extinction_vi_times.append(int(num))
                if "RECALL" in line:
                    words = line.split(':')
                    words = words[1].strip()
                    words = words.split(',')
                    #print("length of words: ",len(words))
                    for items in words:
                        num = items.strip()
                        #print(num)
                        self.recall_vi_times.append(int(num))
                print("VI FILE LOADED",self.VIs_file_path)

            f.close()

        except OSError:
            print("Could not open ",self.VIs_file_path)
            return False
    return True

####################################################################################
#   MAKE LOG/VIDEO/EPHYS FILES
####################################################################################
def create_files(self):
    # DATA PATH + FILES
    print("\nCREATING LOG FILES:")
    # Update times
    self.date = time.strftime("%b_%d_%y")#month-day-Year-H:M
    self.dateTm = time.strftime("%b_%d_%y-%H_%M")#month_day_Year-H:M
    self.exptTime = time.strftime("%H-%M")
    ###### EXPT COPY FILE #####
    new_dir = os.path.join(self.GUI.datapath,self.GUI.Expt_Name)
    if not os.path.exists(new_dir ):  os.mkdir(new_dir)
    new_sub_dir = os.path.join(new_dir,self.GUI.Subject)
    if not os.path.exists(new_sub_dir ):os.mkdir(new_sub_dir)
    new_sub_dir = os.path.join(new_sub_dir,self.date)
    if not os.path.exists(new_sub_dir ):os.mkdir(new_sub_dir)
    new_sub_dir = os.path.join(new_sub_dir,self.exptTime)
    if not os.path.exists(new_sub_dir ):os.mkdir(new_sub_dir)
    self.newdatapath = new_sub_dir
    expt_file_name_COPY = self.GUI.expt_file_name[:-4] + '_COPY.txt' # Removes the '.txt' from original name and adds 'COPY.txt'
    self.expt_file_path_name_COPY = os.path.join(self.newdatapath,expt_file_name_COPY)
    print(self.expt_file_path_name_COPY)

    ###### LOG FILE ####
    log_file_name = self.GUI.Expt_Name + "-" + self.GUI.Subject + '-' +  self.dateTm + '-LOG_file'  + '.csv'
    self.log_file_path_name = os.path.join(self.newdatapath,log_file_name)
    print(self.log_file_path_name)
    self.log_file = open(self.log_file_path_name,'w')        # OPEN LOG FILE

    ##### MAIN VIDEO #######
    #if self.VID_ENABLED == True: # VID_ENABLED gets set after this function is called. Might change later
    video_file_name = self.GUI.Expt_Name + "-" + self.GUI.Subject + '-' +  self.dateTm + '-VIDEO_file' + '.avi'
    self.video_file_path_name = os.path.join(self.newdatapath,video_file_name)
    print(self.video_file_path_name)

    if self.ROI != '':
        freeze_file = self.GUI.Expt_Name + "-" + self.GUI.Subject + '-' +  self.dateTm + '-FREEZES' + '.csv'
        self.freeze_file_path = os.path.join(self.newdatapath, freeze_file)
        print(self.freeze_file_path)

    ## AUX VIDEO ##
    if self.GUI.num_cameras == 2: # Need two cameras
        video_file_name_aux = self.GUI.Expt_Name + "-" + self.GUI.Subject + '-' +  self.dateTm + '-VIDEO_file_aux' + '.avi'
        self.video_file_path_name_aux = os.path.join(self.newdatapath,video_file_name_aux)
        print(self.video_file_path_name_aux)
        self.SIMPLEVIDq.put({'STATE':'ON','PATH_FILE':self.video_file_path_name_aux})

    ###### Change open ephys recoding dir #####
    if self.EPHYS_ENABLED:
        self.snd.changeVars(recordingDir = self.newdatapath, prependText = 'OPEN-EPHYS-' + self.GUI.Subject)
        #self.snd.send(self.snd.START_REC)
        #time.sleep(0.5) # Let Open Ephys record for a bit (maybe remove?)

    ###### Notes
    note_file_name = self.GUI.Expt_Name + "-" + self.GUI.Subject + '-' +  self.dateTm + '-NOTES'  + '.txt'
    self.note_file_path = os.path.join(self.newdatapath, note_file_name)
    note_file = open(self.note_file_path,'a+')
    note_file.close()
    webbrowser.open(self.note_file_path)

# COPY EXPT FILE TO EXPT FILE DATAPATH
def create_expt_file_copy(self):
    print("....................................\n")
    print("COPYING EXPT FILE", self.expt_file_path_name_COPY)
    try:
        exptfl = open(self.expt_file_path_name_COPY,'w')
    except:
        print("XXXXXX 1 could NOT copy of EXPT file",self.expt_file_path_name_COPY)
    try:
        for ln in self.exptFileLines:
            if "EXPT_NAME" in ln: #NOTE: SUBJECT not in original PROTOCOL files. It is added here
                ln = "EXPT_NAME = " + self.GUI.Expt_Name + "\nSUBJECT = " + self.GUI.Subject
                prev_ln = ln
                #exptfl.write(ln+"\n")

            if "ROI" in ln:
                ln = "ROI = " + self.ROIstr

            #print (ln)
            exptfl.write(ln+"\n")

        print("EXPT file copied",self.expt_file_path_name_COPY)
        exptfl.close()
    except:
        print("could NOT copy of EXPT file",self.expt_file_path_name_COPY)

    ########################################
    #  if there is a VIs file, copy it too
    if self.VIs_file_path != "": #if there is a VIs file, copy it too
        try:
            path,name = os.path.split(self.VIs_file_path)
            VIs_file_path_COPY = name[:-4] + '_copy.txt'
            VIs_file_path_COPY = os.path.join(self.newdatapath,VIs_file_path_COPY)
            #f = open(self.VIs_file_path,'r')
            fw = open(VIs_file_path_COPY,'w')
            # w Line by line
            for ln in self.VIFileLines:
                fw.write(ln+"\n")
        except:
            print("COULD NOT WRITE VI FILE COPY", VIs_file_path_COPY)

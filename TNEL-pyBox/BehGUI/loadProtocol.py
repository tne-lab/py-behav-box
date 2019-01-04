from RESOURCES.GUI_elements_by_flav import convertString
import os
import threading
import subprocess
import GUIFunctions

def get_val_between_equal_sign_and_hash(line):
    try:
        Left_right = line.split('=')
        right = Left_right[1].strip()
        Left_right = right.split('#') #IGNORES "#" FOLLOWED BY COMMENTS
        val = Left_right[0].strip()  # comment = left_right[1].strip()
        return val
    except:
        print("Could not parse line")
        return False

def get_all_before_hash(line):
    try:
        left_right = line.split('=')
        left = left_right[0].strip()
        right = left_right[1].strip()
        new_left_right = right.split('#') #IGNORES "#" FOLLOWED BY COMMENTS
        right = new_left_right[0].strip()  # comment = left_right[1].strip()
        #if len(new_left_right) > 1: print("Comment: ",new_left_right[1] )
        return left,right
    except:
        print("Could not parse line")
        return left

def load_expt_file(self):
    print("LOADING: ", self.expt_file_path_name)
    self.protocol = []
    self.conditions = []
    self.exptFileLines = []

    try:
        f = open(self.expt_file_path_name,'r')
        # Read Line by line

        for line in f:
            line = line.strip() # Remove leading and trailoing blanks and \n

            if not 'HAB_COND_EXT_AND_RECALL_VIs' in line: # What is this for?
                line = line.upper()
            #print(line)
            self.exptFileLines.append(line)

            if line != "" and line[0] != "#" : #Skip Blank Lines and Skip lines that are just comments (but still copy them to new file)
                #condition={} # Why is this here? Moved to line 362

                if '[EXPERIMENT' in line:
                    EXPERIMENT = True
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False
                elif '[TONE1' in line:
                    EXPERIMENT = False
                    TONE1 = True
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False
                elif '[TONE2' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = True
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False
                elif '[SHOCK]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = True
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False
                elif '[FREEZE]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = True
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False

                elif '[TOUCHSCREEN]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = True
                    BAR_PRESS = False
                    SETUP = False

                elif '[BAR_PRESS]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = True
                    SETUP = False

                elif '[PROTOCOL' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = True
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False

                elif '[SETUP' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = True

                elif "[CONDITIONS" in line:
                    print("#####################")
                    print("#    CONDITIONS     #")
                    print("#####################")
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = True
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False

                elif '[END' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                    BAR_PRESS = False
                    SETUP = False


                if EXPERIMENT:

                    if 'EXPT_NAME' in line:
                        print("#####################")
                        print("#    EXPERIMENT     #")
                        print("#####################")
                        if self.Expt_Name == "": #Change only if it does not already exist
                            self.Expt_Name = get_val_between_equal_sign_and_hash(line)
                        print(self.Expt_Name)

                    elif 'SUBJECT' in line:
                        self.Subject = get_val_between_equal_sign_and_hash(line)
                        print(self.Subject)

                    elif 'EXPT_PATH' in line:
                        self.datapath = get_val_between_equal_sign_and_hash(line)
                        if not os.path.isdir(self.datapath):
                            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print(self.datapath, " DOES NOT EXIST!!!!")
                            print("Please correct the path in your protocol file!")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                            GUIFunctions.log_event(self, self.events,self.datapath + " DOES NOT EXIST!!!!",self.cur_time)
                            GUIFunctions.log_event(self, self.events,"PLEASE CHECK PATH IN PROTOCOL FILE",self.cur_time)
                            return False
                        else: print(self.datapath)

                    elif 'LOG_FILE_PATH' in line:
                        log_file_path = get_val_between_equal_sign_and_hash(line)
                        if not os.path.isdir(log_file_path):
                            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print(log_file_path, " DOES NOT EXIST!!!!")
                            print("Please correct the path in your protocol file!")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                            GUIFunctions.log_event(self, self.events,log_file_path + " DOES NOT EXIST!!!!",self.cur_time)
                            return False
                        else: print("Log File Path",log_file_path)

                    elif 'VIDEO_FILE_PATH' in line:
                        video_file_path = get_val_between_equal_sign_and_hash(line)
                        if not os.path.isdir(video_file_path):
                            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print(video_file_path, " DOES NOT EXIST!!!!")
                            print("Please correct the path in your protocol file!")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                            GUIFunctions.log_event(self, self.events,video_file_path + " DOES NOT EXIST!!!!",self.cur_time)
                            return False
                        print(video_file_path)

                    elif 'OPEN_EPHYS_PATH' in line:
                        if not self.open_ephys_started:
                            print('opening ephys')
                            self.open_ephys_started = True
                            open_ephys_path = get_val_between_equal_sign_and_hash(line)
                            subprocess.Popen(open_ephys_path)

                    elif 'VI_TIMES_LIST_PATH' in line:
                        self.VIs_file_path = get_val_between_equal_sign_and_hash(line)
                        print(self.VIs_file_path)

                elif TONE1:#TONE1
                    if 'DURATION' in line:
                        self.Tone1_Duration = float(get_val_between_equal_sign_and_hash(line))
                        print("self.Tone1_Duration",self.Tone1_Duration)

                    if 'FREQ' in line:
                        self.Tone1_Freq = float(get_val_between_equal_sign_and_hash(line))
                        print("self.Tone1_Freq: ",self.Tone1_Freq)

                    if 'VOL' in line:
                        self.Tone1_Vol = float(get_val_between_equal_sign_and_hash(line))
                        print("self.Tone1_Vol: ",self.Tone1_Vol)

                elif TONE2:#TONE2
                    if 'DURATION' in line:
                        self.Tone2_Duration = get_val_between_equal_sign_and_hash(line)
                        print("self.Tone2_Duration",self.Tone2_Duration)

                    if 'FREQ' in line:
                        self.Tone2_Freq = float(get_val_between_equal_sign_and_hash(line))
                        print("self.Tone2_Freq: ",self.Tone2_Freq)

                    if 'VOL' in line:
                        self.Tone2_Vol = float(get_val_between_equal_sign_and_hash(line))
                        print("self.Tone2_Vol: ",self.Tone2_Vol)

                elif TOUCH:
                    touch_image_dict={}
                    if 'IMAGES_PATH' in line:
                        self.TOUCH_IMG_PATH = get_val_between_equal_sign_and_hash(line)
                        self.TOUCHSCREEN_USED = True

                    if 'COORDS' in line:
                        words = get_val_between_equal_sign_and_hash(line)
                        imageCoords = words.split(':')
                        for i in range(len(imageCoords)):
                            for c in '()':
                                #Remove parenthesis from (x,y)
                                imageCoords[i] = imageCoords[i].replace(c, "")
                            imageCoordsStr = imageCoords[i].split(",")
                            self.touchImgCoords.append((int(imageCoordsStr[0]), int(imageCoordsStr[1])))
                    elif 'IMG' in line:
                        words = get_val_between_equal_sign_and_hash(line)
                        imageInfo = words.split(":")
                        imageName = imageInfo[0].strip()
                        for c in '()':
                            #Remove parenthesis from rewards
                            imageInfo[1] = imageInfo[1].replace(c, "")
                        imgRewards = []
                        for probability in imageInfo[1].split(","):
                            imgRewards.append(int(probability))
                        self.touchImgs[imageName] = imgRewards

                elif BAR_PRESS:
                    self.BAR_PRESS_INDEPENDENT_PROTOCOL = True
                    if "VI" in line:
                        VI = get_val_between_equal_sign_and_hash(line)
                        try:
                            self.var_interval_reward = int(VI)
                            print("var_interval_reward: ",self.var_interval_reward)
                        except:
                            print ("!!!!!!!!!!!VI must = a number in EXP file!!!!!!!!!!!!!!", )

                elif SHOCK:
                    if 'DURATION' in line:
                        self.Shock_Duration = float(get_val_between_equal_sign_and_hash(line))
                        print(self.Shock_Duration)

                    if 'VOLTS' in line:
                        self.Shock_V = float(get_val_between_equal_sign_and_hash(line))
                        print(self.Shock_V)

                    if 'AMPS' in line:
                        self.Shock_Amp = float(get_val_between_equal_sign_and_hash(line))
                        print(self.Shock_Amp)

                elif FREEZE:
                    print("###################################")
                    print("#    FREEZE DETECTION ENABLED     #")
                    print("###################################")
                    self.FREEZE_DETECTION_ENABLED = True
                    if 'DURATION' in line:
                        Freeze_Duration = get_val_between_equal_sign_and_hash(line)
                        #print(Freeze_Duration)
                    if 'PIX' in line:
                        Min_Pixels = get_val_between_equal_sign_and_hash(line)
                        #print(Min_Pixels)

                    if 'ROI' in line:  #key == 'ROI':  # THIS SHOULD BE IN LOAD PROTOCOL ONLY WHEN and WHERE FREEZE INFO IS GIVEN
                        self.ROI = get_val_between_equal_sign_and_hash(line)
                        if "GENERATE" in self.ROI:
                            print("ROI: ",self.ROI)
                        else:
                            print("ROI COORINATES: ",self.ROI)
                            print('freeze detection assumed')

                elif SETUP:
                    if "SETUP" not in line: # Skips [header] line
                        #print(line)
                        try:
                            word1,word2 = get_all_before_hash(line)
                            self.setup.append({word1:word2})
                        except:
                            self.setup.append({line:True}) # For lines without an '=' in them
                            #if line == 'END': PROTOCOL = False
                        print({word1:word2})
                    else:
                        print("################")
                        print("#    SETUP     #")
                        print("################")
                elif PROTOCOL:
                    #print("self.protocol: ",line)
                    if "PROTOCOL" not in line: # Skips [header] line
                        #print(line)
                        try:
                            word1,word2 = get_all_before_hash(line)
                            self.protocol.append({word1:word2})
                        except:
                            print("single word")
                            self.protocol.append({line:True}) # For lines without an '=' in them
                            #if line == 'END': self.protocol = False
                    else:
                        print("###################")
                        print("#    PROTOCOL     #")
                        print("###################")

                elif CONDITIONS:
                    #print("self.conditions: ",line)
                    if "[CONDITIONS]" in line: # Condition header line
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
        print(self.touch_img_files)
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
        except OSError:
            print("Could not open ",self.VIs_file_path)
            return False
    return True

def create_files(self):
    # DATA PATH + FILES

    #try:
    new_dir = os.path.join(self.datapath,self.Expt_Name)
    if not os.path.exists(new_dir ):  os.mkdir(new_dir)
    new_sub_dir = os.path.join(new_dir,self.date)
    if not os.path.exists(new_sub_dir ):os.mkdir(new_sub_dir)
    new_sub_dir = os.path.join(new_sub_dir,self.exptTime)
    if not os.path.exists(new_sub_dir ):os.mkdir(new_sub_dir)
    self.newdatapath = new_sub_dir
    expt_file_name_COPY = self.expt_file_name[:-4] + '_COPY.txt' # Removes the '.txt' from original name and adds 'COPY.txt'
    self.expt_file_path_name_COPY = os.path.join(self.newdatapath,expt_file_name_COPY)
    print(self.expt_file_path_name_COPY)

    self.snd.changeVars( recordingDir = self.newdatapath)

    log_file_name = self.Expt_Name + "-" + self.Subject + '-' +  self.dateTm + '-LOG_file'  + '.csv'
    self.log_file_path_name = os.path.join(self.newdatapath,log_file_name)
    print(self.log_file_path_name)

    video_file_name = self.Expt_Name + "-" + self.Subject + '-' +  self.dateTm + '-VIDEO_file' + '.avi'
    self.video_file_path_name = os.path.join(self.newdatapath,video_file_name)
    print(self.video_file_path_name)

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
                ln = "EXPT_NAME = " + self.Expt_Name + "\nSUBJECT = " + self.Subject
                prev_ln = ln
                #exptfl.write(ln+"\n")

            if "ROI" in ln:
                ln = "ROI = " + self.ROIstr

            print (ln)
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

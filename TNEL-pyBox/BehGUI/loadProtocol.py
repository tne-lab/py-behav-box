def load_expt_file(self):
    print("LOADING: ", self.expt_file_path_name)
    self.protocol = []
    self.conditions = []
    lines = []


    try:
        f = open(self.expt_file_path_name,'r')
        # Read Line by line

        for line in f:
            line = line.strip() # Remove leading and trailoing blanks and \n
            line = line.upper()
            print(line)
            lines.append(line)
            if line != "":
                condition={}

                if '[EXPERIMENT' in line:
                    EXPERIMENT = True
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                elif '[TONE1' in line:
                    EXPERIMENT = False
                    TONE1 = True
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                elif '[TONE2' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = True
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                elif '[SHOCK]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = True
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False
                elif '[FREEZE]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = True
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False

                elif '[TOUCHSCREEN]' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = True

                elif '[PROTOCOL' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = True
                    CONDITIONS = False
                    TOUCH = False

                elif '[CONDITIONS' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = True
                    TOUCH = False

                elif '[END' in line:
                    EXPERIMENT = False
                    TONE1 = False
                    TONE2 = False
                    SHOCK = False
                    FREEZE = False
                    PROTOCOL = False
                    CONDITIONS = False
                    TOUCH = False


                if EXPERIMENT:
                    if 'EXPT_NAME' in line:
                        words = line.split('=')
                        self.Expt_Name = words[1].strip()
                        self.Expt_Name = self.Expt_Name.strip()
                        print(self.Expt_Name)

                    elif 'SUBJECT' in line:
                        words = line.split('=')
                        self.Subject = words[1].strip()
                        self.Subject = self.Subject.strip()
                        print(self.Subject)

                    elif 'EXPT_PATH' in line:
                        words = line.split('=')
                        self.datapath = words[1].strip()
                        self.datapath = self.datapath.strip()
                        print(self.datapath)
                    elif 'LOG_FILE_PATH' in line:
                        words = line.split('=')
                        log_file_path = words[1].strip()
                        log_file_path = log_file_path.strip()
                        print("LFP",log_file_path)
                    elif 'VIDEO_FILE_PATH' in line:
                        words = line.split('=')
                        video_file_path = words[1].strip()
                        video_file_path = video_file_path.strip()
                        print(video_file_path)
                    elif 'OPEN_EPHYS_PATH' in line:
                        print('opening ephys')
                        words = line.split('=')
                        open_ephys_path = words[1].strip()
                        print(open_ephys_path)
                        open_ephys_thread = threading.Thread(target=os.system, args=(open_ephys_path,))
                        open_ephys_thread.start()

                elif TONE1:#TONE1
                    if 'DURATION' in line:
                        words = line.split('=')
                        self.Tone1_Duration = float(words[1].strip())
                        print("self.Tone1_Duration",self.Tone1_Duration)
                    if 'FREQ' in line:
                        words = line.split('=')
                        self.Tone1_Freq = float(words[1].strip())
                        print("self.Tone1_Freq: ",self.Tone1_Freq)
                    if 'VOL' in line:
                        words = line.split('=')
                        self.Tone1_Vol = float(words[1].strip())
                        print("self.Tone1_Vol: ",self.Tone1_Vol)

                elif TONE2:#TONE2
                    if 'DURATION' in line:
                        words = line.split('=')
                        self.Tone2_Duration = words[1].strip()
                        print("self.Tone2_Duration",self.Tone2_Duration)
                    if 'FREQ' in line:
                        words = line.split('=')
                        self.Tone2_Freq = float(words[1].strip())
                        print("self.Tone2_Freq: ",self.Tone2_Freq)
                    if 'VOL' in line:
                        words = line.split('=')
                        self.Tone2_Vol = float(words[1].strip())
                        print("self.Tone2_Vol: ",self.Tone2_Vol)

                elif TOUCH:
                    touch_image_dict={}
                    if 'IMAGES_PATH' in line:
                        words = line.split('=')
                        self.TOUCH_IMG_PATH = words[1].strip()
                        self.TOUCHSCREEN_USED = True
                    elif 'IMG' in line:
                        words = line.split('=')
                        image_name = words[0].strip()
                        image_file_name_coord = words[1].split(",")
                        img_file_name = image_file_name_coord[0].strip()
                        x = image_file_name_coord[1].strip()
                        x = x.strip("(")
                        y = image_file_name_coord[2].strip()
                        y = y.strip(")")
                        touch_image_dict[img_file_name] = (int(x),int(y))
                        self.touch_img_files.append(touch_image_dict)


                elif SHOCK:
                    if 'DURATION' in line:
                        words = line.split('=')
                        SDuration = words[1].strip()
                        self.Shock_Duration = float(SDuration.strip())
                        print(self.Shock_Duration)
                    if 'VOLTS' in line:
                        words = line.split('=')
                        V = words[1].strip()
                        self.Shock_V = float(V.strip())
                        print(self.Shock_V)
                    if 'AMPS' in line:
                        words = line.split('=')
                        amps = words[1].strip()
                        self.Shock_Amp = float(amps.strip())
                        print(self.Shock_Amp)

                elif FREEZE:
                    if 'DURATION' in line:
                        words = line.split('=')
                        Freeze_Duration = words[1].strip()
                        Freeze_Duration = Freeze_Duration.strip()
                        #print(Freeze_Duration)
                    if 'PIX' in line:
                        words = line.split('=')
                        Min_Pixels = words[1].strip()
                        Min_Pixels = Min_Pixels.strip()
                        #print(Min_Pixels)
                elif PROTOCOL:
                    if "PROTOCOL" not in line:
                        #print(line)
                        try:
                            words = line.split('=')
                            word1 = words[0].strip()
                            word1 = word1.upper()
                            word2 = words[1].strip() #Do NOT make this an upper() to retain True and False
                            self.protocol.append({word1:word2})
                        except:
                            self.protocol.append({line:True}) # For lines without an '=' in them
                            #if line == 'END': self.protocol = False

                elif CONDITIONS:
                    print("self.conditions: ",line)
                    if "[CONDITIONS]" in line:
                        KEY_LINE = True

                    elif KEY_LINE: # CONDITION HEADING (i.e. all the KEYS)
                        keys = line.split(',') #list of condtions but need to be stripped of blanks and tabs
                        #print ("KEYS: ", keys)
                        KEY_LINE = False
                    else: # Not a CONDITION heading line, (i.e. all the VALUES)
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
                        #print (condition)
                else:
                    END_PROTOCOL = True
            else:# line == ""
                print("BLANK LINE")

        f.close()
        print(".......\n")
        print(self.touch_img_files)
    except:
        print("NO SUCH FILE!!!!",self.expt_file_path_name)
        return False

    # DATA PATH + FILES
    try:
        expt_file_name_COPY = self.Expt_Name + "-" + self.Subject + '-' +  dateTm + '-EXPT_file'  + '.txt'
        self.expt_file_path_name_COPY = os.path.join(self.datapath,expt_file_name_COPY)
        print(self.expt_file_path_name_COPY)

        log_file_name = self.Expt_Name + "-" + self.Subject + '-' +  dateTm + '-LOG_file'  + '.txt'
        self.log_file_path_name = os.path.join(log_file_path,log_file_name)
        print(self.log_file_path_name)

        video_file_name = self.Expt_Name + "-" + self.Subject + '-' +  dateTm + '-VIDEO_file' + '.avi'
        self.video_file_path_name = os.path.join(video_file_path,video_file_name)
        print(self.video_file_path_name)
    except:
        print("Could not create data file names")
    try:
        exf = open(self.expt_file_path_name_COPY,'w')
        for l in lines:
            #print(l)
            exf.write(l+"\n")
        exf.close()
    except:
        print("could not write copy of EXPT file",self.expt_file_path_name_COPY)

    print("PROTOCOL LOADED]")
    print (self.protocol)
    for dct in self.protocol:
        for k,v in dct.items():
            print(str(k)+" = " + str(v))



    return True

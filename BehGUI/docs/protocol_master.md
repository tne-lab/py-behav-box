# Protocol File Master List

I believe this is every option currently available to include with your protocol files. Use this cheatsheet with existing files to understand whats going on and whats possible. Feel free to reach out to schat107@umn.edu with questions!

## [EXPERIMENT] - Start of every protocol file. Import expt info.

### EXPT_NAME 
- = string
- Name of folder

### SUBJECT 
- = string
- Subject name (don't think is used)

### EXPT_PATH 
- = path
- Where to save data (NEED)

### LOG_FILE_PATH 
- = path
- Where to save log file

### VIDEO_FILE_PATH 
- = path
- Where to save video

### VI_TIMES_LIST_PATH 
- = path
- Path to vi file (only needed if used)
------
## [PROTOCOL]

### FAN_ON
- = TRUE or FALSE
- ON or OFF

### CAB_LIGHT
- = TRUE or FALSE
- ON or OFF

### TONE1 or TONE2
- = TRUE 
- Turns on tone based on [TONE1/2] 

### FOOD_LIGHT
- = TRUE or FALSE
- ON or OFF

### PELLET
- = TRUE 
- Gives food pellet

### SHOCK
- = TRUE
- Give shock based on [SHOCK] info

### L_CONDITIONING_LIGHT or R_CONDITIONING_LIGHT
- = TRUE or FALSE
- ON or OFF

### CAMERA
- = TRUE or FALSE
- ON or OFF

### REC
- = TRUE or FALSE
- ON or OFF

### EXTEND_LEVERS
- = TRUE or FALSE or R_LVR or L_LVR
- Extend or retract levers

### DRAW_IMAGES
- = TRUE 
- (Draws images on screen according to what was set up in [TOUCHSCREEN])

### START_LOOP
- = Number 
- how many of loops

### END_LOOP
- Gets here and goes back to START_LOOP


### CONFIRM_STIM
- Ask user to confirm correct stim wires are plugged in

### PAUSE
- = NUMBER (seconds to pause)
- = HABITUATION or CONIDTIONING (needs corresponding vi_list_path in [EXPERIMENT])
- = EAT_TO_START
- = BAR_PRESS_TO_START
- = NOSE_POKE_TO_START

### CLOSED_LOOP
- = TRUE or FALSE
- = NUMBER (runs closed loop for "number" seconds

### PARAMETER_SWEEPING
- = TRUE or FALSE
- ON or OFF

### OPEN_LOOP
- = TRUE or FALSE
- ON or OFF

### ERP
-  = text 
- to prepend to folder
- example: ERP = PRE

### RAW 
- _text = NUMBER
- to prepend to folder
- example: RAW_PRE = 120 
- record raw for 120 seconds

### CHECK_NUM_CORRECT
- = NUMBER 
- (if num correct img touches > NUMBER then end expt)

### CONDITIONS
- = NUMBER 
- (run corresponding condition line)

------
## [SETUP]
- Same as protocol, but happens before timer starts
------
## [CONDITIONS]

#### MAX_TIME
- seconds for a trial

#### RESET
- Fixed (wait entire max_time)
- ON_RESET (reset trial after a response)

#### CORRECT
- PELLET
- PELLET80 (any number - % chance of pellet)
- PELLET_VAR (Based on img from [TOUCHSCREEN])
- TONE1/2
- SHOCK
- DN_PUNISH

#### WRONG
- Same options as correct

#### NO_ACTION
- Same options as correct

#### EXTEND_L_LEVER or EXTEND_R_LEVER
- 0 or 1
- extend lever

#### L_CONDITION_LT or R_CONDITION_LT
- 0 or 1
- turn light on or off

#### DES_L_LEVER_PRESS or DES_R_LEVER_PRESS
- 0 or 1
- looking for R or L lever press


#### Examples
MAX_TIME, RESET,        CORRECT,        WRONG,   NO_ACTION
60,       ON_RESPONSE,  PELLET_VAR,     DN_PUNISH,    NONE

MAX_TIME, RESET, L_CONDITION_LT, R_CONDITION_LT, DES_L_LEVER_PRESS, DES_R_LEVER_PRESS, CORRECT, 	WRONG, NO_ACTION
3,      ON_RESPONSE,	  1,		  0,		  1,		    0,	       PELLET80,	PELLET20,  TONE1
3,      ON_RESPONSE,  	  0,		  1,		  0,		    1,	       PELLET80,	PELLET20,  TONE2


------
## [OPEN_EPHYS]

### OPEN_EPHYS_CONFIG_FILE 
- Needs to be before OPEN_EPHYS_PATH if used

### OPEN_EPHYS_PATH 
- Path to exe file (NEED)
------
## [TONE1]

### DURATION 
- How long tone is

### FREQ 
- freq of tone

### VOL 
- Scale of 0-1 (need to test to find db range)
------
## [TONE2]

Same as Tone 1
------
## [SHOCK] - Not tested

### DURATION 

### VOLTS

### AMPS
------
## [FREEZE]

### DURATION 
- How long "frozen" to be considered a freeze event.

### PIX 
- How many pixels need to change between frames

### ROI

##### GENERATE 
- asks user to create ROI

##### (x,y,h,w) (h,w needs to be tested, may be flipped)
------
## [TOUCHSCREEN]

### IMAGES_PATH
- = Path
- path where images are stored

### COORDS
- = (x,y):(x1,y1):...(Xn,Yn)
- coords for the images

#### RANDOM
- Puts images in random locations on the screen

#### BANDIT_TRAINING
- hard coded paradigm to train touching the screen
- UPDATE ME w/ exact paradigm

### IMG
- = img name(stored in IMAGES_PATH) : (probablity of reward OPTIONAL)
- examples: IMG1 = a.bmp
- examples: IMG2 = b.bmp(100x120) -- 100% chance of pellet for 120 trials.
- examples: IMG2 = b.bmp(80x60, 20x60) -- 80% chance of pellet for 60 trials then 20% for 60 trials

### TRAIN_TOUCH
- hard coded paradigm to train touching the screen
- UPDATE ME w/ exact paradigm

### TOUCH_BANDIT
- tells code to look for probablities of pellets based on img

------
## [BAR_PRESS]
- More specifics to add here

### VI
- = number
- variable interval

### BAR_PRESS_TRAIN
- = VI(a,b)
- Increments VI over time 
- a = initial VI for bar PRESS 
- b = final VI for session

------
## [STIM]
- daq addresses

### STIM_ADDRESS_X
- address to stim at. Defaults as first stim location 

### STIM_ADDRESS_Y
- address to stim at. Defaults as second stim location (sham in closed loop and second stim location in open look)
------
## [ERP]

### INTER_PULSE_WIDTH 
- Time between stims (default = 4)

### PULSE_VAR 
- Variation between IPW +- value (default = 1)

### NUM_PULSE 
- Num pulses at each location (default = 2)

### NUM_LOCATIONS 
- Num locations to ERP (default = 2)
------
## [PARAMETER_SWEEPING]

### INTENSITY

### DURATION

### DELAY

### DELAY_VAR

### SET_SIZE
------
## [OPEN_LOOP]

### PHASE_DELAY - ms between stim
------
## [CLOSED_LOOP]

### EVENTCHANNEL 
- channel to look for events (default  = 1)

### MICROAMPS 
- Amps to stim (Default = 100)

### STIM_LAG 
- how long between event occurence and stim (Default = 0)

### TIMEOUT 
- min time between stim events in seconds (Default = 1)

### TIMEOUT_VAR
 - +- varitation in timeout in seconds(Default = 0.2)
from RESOURCES.GUI_elements_by_flav import *

def NIDAQ_GUI_ELEMENTS(self, myscreen):
    #global boxes,circles,LEDs,labels,toggles,info_boxes,sliders

    # BOXES
    boxes = []
    boxes.append(My_Rimmed_Box(myscreen,180,360,100,90,self.black,self.darkgray)) # FEEDER

    # BUTTONS
    buttons = []
    #                      (myscreen,ID, x, y, w, h,"text"    , font size)
    buttons.append(MyButton(myscreen,0,10,5,50,20,"CABIN LT",12))  # 0
    buttons.append(MyButton(myscreen,5,10,32,50,20,"FAN",12))         # 5

    buttons.append(MyButton(myscreen,1,193,320,75,30,"EXTEND",12))  # 1 BOTH LEVERS
    buttons.append(MyButton(myscreen,9,160,320,30,30,"L",12))  # 1 BOTH LEVERS
    buttons.append(MyButton(myscreen,10,270,320,30,30,"R",12))  # 1 BOTH LEVERS


    buttons.append(MyButton(myscreen,4,205,500,50,20,"FEED",12))     # 4
    buttons.append(MyButton(myscreen,6,215, 280, 30,20,"REC",12))    # 6
    buttons.append(MyButton(myscreen,7,360, 545, 75,70,"START EXPT",12))    # 6
    buttons.append(MyButton(myscreen,8,195, 585, 70,30,"LOAD FILE",12))    # 6


    # LEVERS
    #def __init__(self, surface, index, x, y, w, h, text,fsize = 18):
    levers = []
    levers.append(MyLever(myscreen,0,50,340,50,20,"L LEVER",12))   # left
    levers.append(MyLever(myscreen,1,365,340,50,20,"R LEVER",12))   # right

    # CIRCLES (IF ANY)
    circles = []

    # LEDS (LIGHTS AND NOSE POKES)
    LEDs = []
    LEDs.append(MyLED(myscreen,0,45,70,30,"OFF", self.lightgray, self.darkgray)) # L LIGHTS
    LEDs.append(MyLED(myscreen,1,360,70,30,"OFF", self.lightgray, self.darkgray))# R LIGHTS

    LEDs.append(MyLED(myscreen,2,45,200,30,"OFF", self.lightpurple, self.darkpurple)) # NOSE POKES
    LEDs.append(MyLED(myscreen,3,360,200,30,"OFF", self.lightpurple, self.darkpurple))# NOSE POKES

    LEDs.append(MyLED(myscreen,4,170,395,10,"OFF", self.white, self.lightgray)) # FEEDER BOX
    LEDs.append(MyLED(myscreen,5,270,395,10,"OFF", self.white, self.lightgray)) # FEEDER BOX
    #LEDs.append(MyLED(myscreen,187,421,15,"OFF", self.red, gray))
    #LEDs.append(MyLED(myscreen,186,479,15,"OFF", self.red, gray))

    labels = []
    #labels.append(MyLabel(myscreen,108,290,50,20,"Label1",14))
    #labels.append(MyLabel(myscreen,242,289,50,20,"Label2",14))
    #labels.append(MyLabel(myscreen,245,369,50,20,"Label3",14))
    #labels.append(MyLabel(myscreen,107,369,50,20,"Label4",14))
    #labels.append(MyLabel(myscreen,43,318,50,20,"Label5",14))
    #labels.append(MyLabel(myscreen,237,422,50,20,"Label6",14))
    #labels.append(MyLabel(myscreen,236,480,50,20,"Label7",14))
    #labels.append(MyLabel(myscreen,235,539,50,20,"Label8",14))

    info_boxes = []
    #def __init__(self, surface,x, y, w, h, label_name,label_pos, text ,fsize = 12):
    info_boxes.append(InfoBox( myscreen,50,265,50,15,"L NOSE POKES",'BOTTOM','0'))
    info_boxes.append(InfoBox( myscreen,365,265,50,15,"R NOSE POKES",'BOTTOM','0'))
    info_boxes.append(InfoBox( myscreen,50,370,50,15,"L PRESSES",'BOTTOM','0'))
    info_boxes.append(InfoBox( myscreen,365,370,50,15,"R PRESSES",'BOTTOM','0'))
    info_boxes.append(InfoBox( myscreen,205,400,50,15,"EATEN",'BOTTOM','0'))
    info_boxes.append(InfoBox( myscreen,205,455,50,15,"PELLETS",'BOTTOM','0'))
    info_boxes.append(InfoBox( myscreen,20,730,420,250,"EVENT LOG",'TOP'," "))
    info_boxes.append(InfoBox( myscreen,20,600,70,17,"DATE",'RIGHT'," "))

    # USER INPUT BOXES
    user_inputs = []
    #def __init__(self, surface,x, y, w, h, label_name,label_pos, text ,fsize = 12):
    user_inputs.append(get_user_input( myscreen,170,25,20,15,"Spk(S)",'TOP','0'))
    user_inputs.append(get_user_input( myscreen,210,25,40,15,"Freq(Hz)",'TOP','0'))
    user_inputs.append(get_user_input( myscreen,270,25,20,15,"Vol(0-1)",'TOP','0'))

    user_inputs.append(get_user_input(myscreen,190,195,20,15,"Shck(S)",'BOTTOM','0'))
    user_inputs.append(get_user_input(myscreen,220,195,20,15,"V",'BOTTOM','0'))
    user_inputs.append(get_user_input(myscreen,250,195,20,15,"Amps",'BOTTOM','0'))


    user_inputs.append(get_user_input( myscreen,20,525,70,17,"EXPT",'RIGHT'," "))
    user_inputs.append(get_user_input( myscreen,20,550,70,17,"SUBJECT",'RIGHT'," "))
    user_inputs.append(get_user_input( myscreen,20,575,70,17,"TRIAL",'RIGHT'," "))


    user_inputs.append(get_user_input( myscreen,20,650,420,15,"EXPT PATH",'TOP'," "))
    user_inputs.append(get_user_input( myscreen,20,690,420,15,"EXPT FILE NAME",'TOP'," "))
    # TOGGLES
    toggles = []

    return buttons, levers, boxes, circles, LEDs, toggles, sliders, info_boxes, user_inputs, labels


def setupGUI(self):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20,40)
    self.myscreen = pygame.display.set_mode((460,990),pygame.RESIZABLE,32)
    self.UMNlogo = pygame.image.load(r'.\RESOURCES\UMNlogo.png')
    pygame.display.set_icon(UMNlogo)
    self.TNElogo = pygame.image.load(r'.\RESOURCES\TNE logo.jpg')
    self.TNElogo = pygame.transform.scale(self.TNElogo, (70, 50))
    pygame.display.set_caption('Behavioral Chamber Control 1.0 by F. da Silva and M. Shatza Oct. 30, 2018') # Enter your window caption here
    #by Flavio J.K. da Silva and Mark Shatza Oct. 30, 2018') #
    pygame.init()

    #############
    #
    #  Create Menu GUI elements
    #
    #############

    self.red         = (255,0,0)
    self.green       = (0,255,0)
    self.blue        = (0,0,255)
    self.gray        = (100,100,100)
    self.darkgray    = (50,50,50)
    self.lightgray   = (200,200,200)
    self.black       = (0,0,0)
    self.white       = (255,255,255)
    self.yellow      = (255,255,0)
    self.lightpurple  = (160,12,75)
    self.darkpurple  = (51,5,25)


    # FLAGS
    self.NEW_BUTTON = False
    self.LEFT_MOUSE_DOWN = False
    self.BUTTON_SELECTED = False
    self.LBL_SELECTED = False
    self.LED_SELECTED = False
    self.BOX_SELECTED = False
    self.CIRC_SELECTED = False
    self.SLIDER_SELECTED = False

    self.CORNER_SET = False
    self.DELETE_ITEM = False

    self.buttons,self.levers,self.boxes,self.circles,self.LEDs,self.toggles,self.sliders,self.info_boxes,self.user_inputs,self.labels = NIDAQ_GUI_ELEMENTS(myscreen,buttons,levers,boxes,circles,LEDs,toggles,sliders,info_boxes,user_inputs,labels)
    print(len(buttons), " buttons")
    print(len(levers), " levers")
    print(len(boxes), " boxes")
    print(len(circles), " circles")
    print(len(LEDs), " LEDs")
    print(len(toggles), " toggles" )
    print(len(sliders), " sliders")
    print(len(labels), " labels")
    print(len(info_boxes), " info_boxes")
    print(len(info_boxes), " user_imputs")
    # USER INPUTS DEFAULT VALUES
    for user_input in user_inputs:
        if user_input.label == "EXPT":
             user_input.text = str(self.Expt_Name)
        elif user_input.label == "SUBJECT":
             user_input.text = str(self.Subject)
        elif user_input.label == "TRIAL":
             user_input.text  = str(self.trial_num)
        elif user_input.label == "EXPT PATH":
             user_input.text = str(self.datapath)
        elif user_input.label == "EXPT FILE NAME":
             user_input.text = str(self.expt_file_name)
        elif user_input.label == "Spk(S)":
             user_input.text  = str(self.Tone1_Duration)
        elif user_input.label == "Freq(Hz)":
             user_input.text  = str(self.Tone1_Freq)
        elif user_input.label == "Vol(0-1)":
             user_input.text  = str(self.Tone1_Vol)
        elif user_input.label == "Shck(S)":
             user_input.text = str(self.Shock_Duration)
        elif user_input.label == "V":
             user_input.text = str(self.Shock_V)
        elif user_input.label == "Amps":
             user_input.text = str(self.Shock_Amp)

    # MAIN LOOP
    self.clk_time_start = time.perf_counter()
    print (clk_time_start)
    self.FAN_0N = False
    self.CAB_LIGHT_ON = False
    self.Background_color = (darkgray)
    self.FEEDER_LT_ON = False

    START_TIME = time.perf_counter()
    self.LEVER_PRESS_TIME = START_TIME
    self.NOSE_POKE_TIME = START_TIME
    self.TONE_TIME = START_TIME
    self.SHOCK_TIME = START_TIME

    self.num_L_nose_pokes = 0
    self.num_R_nose_pokes = 0
    self.num_L_lever_preses = 0
    self.num_R_lever_preses = 0

    self.num_eaten = 0
    self.NOSE_POKED_L = False
    self.NOSE_POKED_R = False
    self.LEVER_PRESSED_L = False
    self.LEVER_PRESSED_R = False
    self.ACTION_TAKEN = False
    self.SHOCK_ON = False
    self.CAMERA_ON = False
    self.RECORDING = False

    self.events.append(("StartTime: " + str(START_TIME)))

    self.PREVIOUSLY_FROZEN = False #Used to prevent 'unfrozen' from being logged prior to first 'frozen' event
    self.FROZEN_ALREADY_LOGGED = False #Used for "DEBOUNCING" Frozen msg from video
    self.UNFROZEN_ALREADY_LOGGED = False #Used for "DEBOUNCING" Frozen msg from video
    self.cur_time =  time.perf_counter()

    self.START_EXPT = False
    self.PAUSE_STARTED = False

    self.Protocol_ln_num = 0
    self.loop = 0
    self.Protocol_loops = 0
    self.LOOP_FIRST_PASS = True
    self.CONDITONS_NOT_SET = True
    self.CONDITION_STARTED = False

    self.Expt_Count = 0

    self.TOUCH_IMAGES_SENT = False

    # Open ephys stuff
    self.snd = zmqClasses.SNDEvent(5556, recordingDir = 'C:\\Users\\Ephys\\Desktop\\RecDir', prependText = 'CHANGE ME') # subject number or something

    self.openEphysBack_q = Queue()
    # Start thread
    open_ephys_rcv = threading.Thread(target=eventRECV.rcv, args=(openEphysBack_q,), kwargs={'flags' : [b'event']})
    open_ephys_rcv.start()

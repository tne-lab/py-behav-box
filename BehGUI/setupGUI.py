from RESOURCES.GUI_elements_by_flav import *
import zmqClasses
from queue import Queue
import eventRECV
import experiment

def checkForTouch(self):
    if self.EXPT_LOADED:
        if self.expt.TOUCHSCREEN_USED:
            return True
        else:
            return False
    else:
        return False

def NIDAQ_GUI_ELEMENT(self, myscreen):
    #global boxes,circles,LEDs,labels,toggles,info_boxes,sliders

    # BOXES
    boxes = []

    if checkForTouch(self):
        boxes.append(My_Rimmed_Box(myscreen,395,380,80,62,self.black,self.darkgray)) # FEEDER
        boxes.append(My_Rimmed_Box(myscreen,40,320,256,192,0,self.black)) # future touch screen
        boxes.append(My_Rimmed_Box(myscreen,40,450,256,63,self.lightgray,self.black)) # future touch screen Dead zon
    else: boxes.append(My_Rimmed_Box(myscreen,200,360,100,90,self.black,self.darkgray)) # FEEDER
    # BUTTONS
    buttons = []
    #                      (myscreen,ID, x, y, w, h,"text"    , font size)
    buttons.append(MyButton(myscreen,0,10,5,50,20,"CABIN LT",12))  # 0
    buttons.append(MyButton(myscreen,5,10,32,50,20,"FAN",12))         # 5
    

    if checkForTouch(self):
        buttons.append(MyButton(myscreen,4,315,390,50,20,"FEED",12))     # 4
        buttons.append(MyButton(myscreen,6,235, 270, 30,20,"REC",12))    # 6
        buttons.append(MyButton(myscreen,7,400, 560, 75,50,"START EXPT",12))  # 7
        buttons.append(MyButton(myscreen,8,215, 600, 70,30,"LOAD FILE",12))   # 8

    else:
        buttons.append(MyButton(myscreen,1,213,320,75,30,"EXTEND",12))  # 1 BOTH LEVERS
        buttons.append(MyButton(myscreen,9,180,320,30,30,"L",12))  # 1 BOTH LEVERS
        buttons.append(MyButton(myscreen,10,290,320,30,30,"R",12))  # 1 BOTH LEVERS
        buttons.append(MyButton(myscreen,4,225,500,50,20,"FEED",12))     # 4
        buttons.append(MyButton(myscreen,6,235, 280, 30,20,"REC",12))    # 6
        buttons.append(MyButton(myscreen,7,400, 560, 75,50,"START EXPT",12))  # 7
        buttons.append(MyButton(myscreen,8,215, 600, 70,30,"LOAD FILE",12))   # 8





    # LEVERS
    #def __init__(self, surface, index, x, y, w, h, text,fsize = 18):
    levers = []
    if not checkForTouch(self):
        levers.append(MyLever(myscreen,0,50,300,50,20,"L LEVER",12))   # left
        levers.append(MyLever(myscreen,1,405,300,50,20,"R LEVER",12))   # right

    # CIRCLES (IF ANY)
    circles = []

    # LEDS (LIGHTS AND NOSE POKES)
    LEDs = []
    LEDs.append(MyLED(myscreen,0,45,60,30,"OFF", self.lightgray, self.darkgray)) # L LIGHTS
    LEDs.append(MyLED(myscreen,1,400,60,30,"OFF", self.lightgray, self.darkgray))# R LIGHTS

    LEDs.append(MyLED(myscreen,2,45,130,30,"OFF", self.lightpurple, self.darkpurple)) # NOSE POKES
    LEDs.append(MyLED(myscreen,3,400,130,30,"OFF", self.lightpurple, self.darkpurple))# NOSE POKES

    if checkForTouch(self):
        LEDs.append(MyLED(myscreen,4,385,400,10,"OFF", self.white, self.lightgray)) # FEEDER BOX
        LEDs.append(MyLED(myscreen,5,465,400,10,"OFF", self.white, self.lightgray)) # FEEDER BOX

    else:
        LEDs.append(MyLED(myscreen,4,190,395,10,"OFF", self.white, self.lightgray)) # FEEDER BOX
        LEDs.append(MyLED(myscreen,5,290,395,10,"OFF", self.white, self.lightgray)) # FEEDER BOX

    LEDs.append(MyLED(myscreen,6,430,530,10,"OFF", self.green, self.lightgray,False)) # EXPERIMENT STARTED
    #LEDs.append(MyLED(myscreen,187,421,15,"OFF", self.red, gray))
    #LEDs.append(MyLED(myscreen,186,479,15,"OFF", self.red, gray))

    labels = []
    #labels.append(MyLabel(myscreen,108,290,50,20,"Label1",14))
    #labels.append(MyLabel(myscreen,242,289,50,20,"Label2",14))

    info_boxes = []
    #def __init__(self, surface,x, y, w, h, label_name,label_pos, text ,fsize = 12):
    info_boxes.append(InfoBox( myscreen,50,200,50,15,"L NOSE POKES",'BOTTOM','0'))
    info_boxes.append(InfoBox( myscreen,405,200,50,15,"R NOSE POKES",'BOTTOM','0'))

    if not checkForTouch(self):
        info_boxes.append(InfoBox( myscreen,50,330,50,15,"L PRESSES",'BOTTOM','0'))
        info_boxes.append(InfoBox( myscreen,405,330,50,15,"R PRESSES",'BOTTOM','0'))
        info_boxes.append(InfoBox( myscreen,225,400,50,15,"EATEN",'BOTTOM','0'))
        info_boxes.append(InfoBox( myscreen,225,455,50,15,"PELLETS",'BOTTOM','0'))
        info_boxes.append(InfoBox( myscreen,290,502,40,17,"VI CountDn",'RIGHT',"0"))
    else:
        info_boxes.append(InfoBox( myscreen,415,420,40,15,"EATEN",'BOTTOM','0'))
        info_boxes.append(InfoBox( myscreen,320,420,40,15,"PELLETS",'BOTTOM','0'))

    info_boxes.append(InfoBox( myscreen,20,730,460,250,"EVENT LOG",'TOP'," "))
    info_boxes.append(InfoBox( myscreen,20,620,70,17,"DATE",'RIGHT'," "))
    info_boxes.append(InfoBox( myscreen,401,620,75,17,"TIME",'LEFT',"0.0"))

    #buttons.append(MyButton(myscreen,7,360, 525, 75,70,"START EXPT",12))  # 7
    # USER INPUT BOXES
    user_inputs = []
    #def __init__(self, surface,x, y, w, h, label_name,label_pos, text ,fsize = 12):
    user_inputs.append(get_user_input( myscreen,190,25,30,17,"Spk(S)",'TOP','0'))
    user_inputs.append(get_user_input( myscreen,230,25,45,17,"Freq(Hz)",'TOP','0'))
    user_inputs.append(get_user_input( myscreen,290,25,30,17,"Vol(0-1)",'TOP','0'))

    user_inputs.append(get_user_input(myscreen,200,195,30,17,"Shck(S)",'BOTTOM','0'))
    user_inputs.append(get_user_input(myscreen,235,195,30,17,"V",'BOTTOM','0'))
    user_inputs.append(get_user_input(myscreen,270,195,30,17,"Amps",'BOTTOM','0'))


    user_inputs.append(get_user_input( myscreen,20,545,120,17,"EXPT",'RIGHT'," "))
    user_inputs.append(get_user_input( myscreen,20,570,70,17,"SUBJECT",'RIGHT'," "))
    user_inputs.append(get_user_input( myscreen,20,595,70,17,"TRIAL",'RIGHT'," "))


    user_inputs.append(get_user_input( myscreen,20,650,460,17,"EXPT PATH",'TOP'," "))
    user_inputs.append(get_user_input( myscreen,20,690,460,17,"EXPT FILE NAME",'TOP'," "))
    # TOGGLES
    toggles = []
    # SLIDERS
    sliders = []
    sliders.append( MyVerticalSlider(myscreen,490,730,0,250, 18, 10))
    20,730,460,250
    #class class MyVerticalSlider:  def __init__(self,surface,x, y, sliderYpos,slotL, bw, bh, fsize = 12):

    return buttons, levers, boxes, circles, LEDs, toggles, info_boxes, user_inputs, labels, sliders


def setupExpt(self):
    print('starting expt')
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20,40)
    self.myscreen = pygame.display.set_mode((500,990),pygame.RESIZABLE,32)
    #self.myscreen = pygame.display.set_mode((500,990),32)
    self.UMNlogo = pygame.image.load(r'.\RESOURCES\UMNlogo.PNG')
    pygame.display.set_icon(self.UMNlogo)
    self.TNElogo = pygame.image.load(r'.\RESOURCES\TNE logo.jpg')
    self.TNElogo = pygame.transform.scale(self.TNElogo, (70, 50))
    pygame.display.set_caption('Behavioral Chamber Control 1.0 by F. da Silva and M. Shatza Oct. 30, 2018') # Enter your window caption here
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

    self.events = []

    # MAIN LOOP
    self.start_line = len(self.events)
    #self.y_per_line = int(self.sliders[0].slotL / 14.0)

    self.clk_time_start = time.perf_counter()
    self.FAN_0N = False
    self.CAB_LIGHT_ON = False
    self.Background_color = (self.darkgray)
    self.FEEDER_LT_ON = False

    START_TIME = time.perf_counter()
    self.LEVER_PRESS_TIME = START_TIME
    self.NOSE_POKE_TIME = START_TIME
    self.TONE_TIME = START_TIME
    self.SHOCK_TIME = START_TIME

    self.NOSE_POKED_L = False
    self.NOSE_POKED_R = False
    self.LEVER_PRESSED_L = False
    self.LEVER_PRESSED_R = False
    self.FOOD_EATEN = False
    self.ACTION_TAKEN = False
    self.SHOCK_ON = False
    self.CAMERA_ON = False
    self.RECORDING = False
    self.FREEZE_DETECTION_ENABLED = False

    self.EXPT_LOADED = False
    self.Expt_Name = ''
    self.Subject = ''
    self.prev_Subject = ''
    self.NAME_OR_SUBJ_CHANGED = False
    self.START_EXPT = False
    self.RESTART_EXPT = False
    self.events = []

    time.sleep(0.5)

    self.expt = experiment.Experiment(self)
    print('done starting')
    self.buttons,self.levers,self.boxes,self.circles,self.LEDs,self.toggles,self.info_boxes,self.user_inputs,self.labels,self.sliders = NIDAQ_GUI_ELEMENT(self, self.myscreen )
    self.feederBox = self.boxes[0]
    self.new_slider_y = self.sliders[0].slotL # SETUPGUI
    ##    print(len(self.buttons), " buttons")
    ##    print(len(self.levers), " levers")
    ##    print(len(self.boxes), " boxes")
    ##    print(len(self.circles), " circles")
    ##    print(len(self.LEDs), " LEDs")
    ##    print(len(self.toggles), " toggles" )
    ##    print(len(self.labels), " labels")
    ##    print(len(self.info_boxes), " info_boxes")
    ##    print(len(self.info_boxes), " user_imputs")
    # USER INPUTS DEFAULT VALUES
    for user_input in self.user_inputs:
        if user_input.label == "EXPT":
             user_input.text = str(self.Expt_Name)
        elif user_input.label == "SUBJECT":
             user_input.text = str(self.Subject)
        elif user_input.label == "TRIAL":
             user_input.text = "0"
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

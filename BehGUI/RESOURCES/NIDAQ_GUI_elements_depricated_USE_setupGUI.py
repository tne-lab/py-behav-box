from RESOURCES.GUI_elements_by_flav import *
## Be sure GUI_elements_by_flav exists in a directory called"RESOURCES" just below your current working directory

buttons = []
levers = []
boxes = []
circles = []
LEDs = []
labels = []
toggles = []
info_boxes = []
sliders = []
labels = []
#def NIDAQ_GUI_ELEMENTS():
def NIDAQ_GUI_ELEMENTS(myscreen, buttons, levers, boxes, circles, LEDs, toggles, sliders, info_boxes, user_inputs, labels):
    #global boxes,circles,LEDs,labels,toggles,info_boxes,sliders
    red         = (255,0,0)
    green       = (0,255,0)
    blue        = (0,0,255)
    gray        = (100,100,100)
    darkgray    = (50,50,50)
    lightgray   = (200,200,200)
    black       = (0,0,0)
    white       = (255,255,255)
    yellow      = (255,255,0)
    lightpurple  = (160,12,75)
    darkpurple  = (51,5,25)

    # BOXES
    boxes = []
    boxes.append(My_Rimmed_Box(myscreen,180,360,100,90,black,darkgray)) # FEEDER

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
    buttons.append(MyButton(myscreen,7,360, 525, 75,70,"START EXPT",12))    # 6
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
    LEDs.append(MyLED(myscreen,0,45,70,30,"OFF", lightgray, darkgray)) # L LIGHTS
    LEDs.append(MyLED(myscreen,1,360,70,30,"OFF", lightgray, darkgray))# R LIGHTS

    LEDs.append(MyLED(myscreen,2,45,200,30,"OFF", lightpurple, darkpurple)) # NOSE POKES
    LEDs.append(MyLED(myscreen,3,360,200,30,"OFF", lightpurple, darkpurple))# NOSE POKES

    LEDs.append(MyLED(myscreen,4,170,395,10,"OFF", white, lightgray)) # FEEDER BOX
    LEDs.append(MyLED(myscreen,5,270,395,10,"OFF", white, lightgray)) # FEEDER BOX

    LEDs.append(MyLED(myscreen,6,400,500,10,"OFF", green, lightgray,False)) # EXPERIMENT STARTED

    #LEDs.append(MyLED(myscreen,187,421,15,"OFF", red, gray))
    #LEDs.append(MyLED(myscreen,186,479,15,"OFF", red, gray))

    labels = []
    #labels.append(MyLabel(myscreen,108,290,50,20,"Label1",14))
    #labels.append(MyLabel(myscreen,242,289,50,20,"Label2",14))

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


import pygame, os, sys, time,copy, string
from pygame.locals import *
from pygame.sprite import Sprite
from random import randint, choice,randrange
import math
import numpy
from array import *
import threading

def exit_game():
    pygame.quit()
    sys.exit()
    #break

def diplay_fixation_point(screen,GAME_AREA,ctr_x,ctr_y):
    pygame.draw.rect(screen, (0, 0, 0), GAME_AREA, 0) #(0=fill)
    pygame.draw.line(screen,(255,255,255),(ctr_x-50,ctr_y),(ctr_x+50,ctr_y), 4)
    pygame.draw.line(screen,(255,255,255),(ctr_x,ctr_y-50),(ctr_x,ctr_y+50), 4)


def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def isInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def str2bool(v):
  #  from https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python
  return v.lower() in ("yes", "true", "t", "1")

from ast import literal_eval
#https://stackoverflow.com/questions/15357422/python-determine-if-a-string-should-be-converted-into-int-or-float
def convertString(s):
    if isinstance(s, str):
        # It's a string.  Does it represnt a literal?
        #
        try:
            val = literal_eval(s)
        except:
            # s doesn't represnt any sort of literal so no conversion will be
            # done.
            #
            val = s
    else:
        # It's already something other than a string
        #
        val = s

    ##
    # Is the float actually an int? (i.e. is the float 1.0 ?)
    #
    if isinstance(val, float):
        if val.is_integer():
            return int(val)

        # It really is a float
        return val

    return val

def play_sound(frequency, volume, duration):
    '''
    Play a frequency at a given volume
    This is run a a sepoarate thread so calling program can keep running
    '''
    print ("freq: ",frequency, "vol: ",volume, "Duration: ",duration)
    sample_rate = 22050 #  44100 #Hz or data points per sec
    bits = 16

    pygame.mixer.pre_init(sample_rate, -bits, 2)

    #n_samples = int(round(float(duration)*sample_rate)) # Number of sample to generate
    n_samples = int(sample_rate) # Number of sample to generate

    #setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
    buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
    #max_sample = 2**(bits - 1) - 1   # at 16 bits, max_sample = 16384
    max_sample =128.0
    for s in range(n_samples):
        t = float(s)/sample_rate    # time in seconds

        #grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
        buf[s][0] = int(round(max_sample*math.sin(2*math.pi*float(frequency)*t)))        # left
        buf[s][1] = int(round(max_sample*math.sin(2*math.pi*float(frequency)*t)))    # right

    sound = pygame.sndarray.make_sound(buf)
    #play once, then loop until duration time has passed
    sound.set_volume(float(volume)) # volume value 0.0 to 1.0
    playTime = int(duration *1000)  # Duration in sec, need millisec
    print("playtime: ",playTime, "millisec")
    sound.play(loops = -1,maxtime=playTime) # - 1 = loops forever, maxtime in millisec


def play_sound_file(music_file, volume=0.8):
    '''
    stream music with mixer.music module in a blocking manner
    this will stream the sound from disk while playing
    '''
    # set up the mixer
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # volume value 0.0 to 1.0
    pygame.mixer.music.set_volume(volume)
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file {} loaded!".format(music_file))
    except pygame.error:
        print("File {} not found! ({})".format(music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(1)



##def get_keyboard_input(screen,x,y):
##        text_input = ""
##        NEED_USER_INFO = True
##
##        while NEED_USER_INFO: #Just getting user physPinID
##            question= 'Enter Desired Label'
##            pygame.font.init()
##            font = pygame.font.Font(None, 18)
##            # INPUT AREA
##
####            RIM_REC = Rect(USER_INPUT_AREA.left-5,USER_INPUT_AREA.top-5,
####                           USER_INPUT_AREA.width+10,USER_INPUT_AREA.height+10)
##            RIM_REC = Rect(x,y+40,210,60)
##            USER_INPUT_AREA = Rect(x+5,y+45,200,50)
##
##            pygame.draw.rect(screen, (255, 255, 255), USER_INPUT_AREA, 0) #(0=fill)
##            pygame.draw.rect(screen, (255,0,0), RIM_REC, 5) #(1=outline)
##            # Write msg
##            my_font1 = pygame.font.SysFont('arial', 40)
##
##            start_msg = my_font1.render('Enter label', True, Color('white'))
##            msgHt1 = start_msg.get_height()
##            screen.blit(start_msg, (x+5,y+50,40,40)) #(x,y,w,h)
##
##            my_font2 = pygame.font.SysFont('arial', 20)
##            message = my_font2.render(text_input, True, Color('blue'))
##            msgHt2 =message.get_height()
##
##            for sys_event in pygame.event.get():
##                if sys_event.type == pygame.QUIT:
##                    exit_game()
##
##                elif sys_event.type == pygame.KEYDOWN:
##                    if sys_event.key == K_BACKSPACE:
##                        text_input = text_input[0:-1]
##                    elif sys_event.key == K_RETURN:
##                        #TURN ON GAME AFTER GETTING USER physPinID
##                        NEED_USER_INFO = False
##                        return text_input
##                        break
##
##                    else: #COLLECT ENTERRED CHARACTERS
##                        try:
##                            text_input += chr(sys_event.key)
##                            message = my_font2.render(text_input, True, Color('blue'))
##                        except:
##                            pass
##
##            screen.blit(message, USER_INPUT_AREA.move(20,  msgHt2/2))
##            pygame.display.flip()


def await_any_key(screen,SCREEN_WIDTH,SCREEN_HEIGHT,msg1,msg2 = 'PRESS ANY KEY TO CONTINUE.'):
        # PAUSE WHILE WAITING FOR ANY KEY
        pygame.font.init()
        ctr_x = SCREEN_WIDTH/2
        ctr_y = SCREEN_HEIGHT/2
        font = pygame.font.Font(None, 18)
        my_font1 = pygame.font.SysFont('arial', 30)
        message1 = my_font1.render(msg1, True, Color('white'))
        msgHt =message1.get_height()
        msgWd =message1.get_width()
        screen.blit(message1,(ctr_x-msgWd/2,ctr_y-2*msgHt))

        message2 = my_font1.render(msg2, True, Color('white'))
        msgHt =message2.get_height()
        msgWd =message2.get_width()
        screen.blit(message2,(ctr_x-msgWd/2,ctr_y+msgHt))

        AWAITING_INPUT = True
        while AWAITING_INPUT: #Just getting user physPinID
            for sys_event in pygame.event.get():
                if sys_event.type == pygame.QUIT:
                    exit_game()

                elif sys_event.type == pygame.KEYDOWN:
                    AWAITING_INPUT = False
                    return True

            pygame.display.flip()

def draw_plus_sign(surface, x, y, w, color):# (x,y is at center, w is width/2)
    pygame.draw.line(surface, color, (x-w, y), (x+w, y),1)
    pygame.draw.line(surface, color, (x, y-w), (x,  y+w),1)

def draw_cue(screen, rect, cue,mphysPinID_x,mphysPinID_y):
    my_font = pygame.font.SysFont('arial', 20)
    cue_sf = my_font.render(cue, True, Color('yellow'))
    lblHt =cue_sf.get_height()
    lblWt =cue_sf.get_width()
    screen.blit(cue_sf, rect.move(mphysPinID_x-lblWt/2, mphysPinID_y-lblHt/2))  #move within game area
    #screen.blit(cue_sf, rect.move(mphysPinID_x-lblWt/2, mphysPinID_y))  #move within game area

class MyHorizSlider:
    def __init__(self,surface,x, y, sliderXpos,slotL, bw, bh, fsize = 12):
        #(x,y) = where on page
        #(sliderX,slotL)location of slider along line, length of slot
        self.x = x
        self.y = y
        self.sliderX = sliderXpos - 0.5*bw    # location of slider
        self.slotL = slotL                # lenght of slot

        self.bw = bw # width of slider button
        self.bh = bh # Height of slider button
        #slider button
        self.rect = Rect(sliderXpos+x,y, bw,bh) # slider button face
        self.percent = (self.sliderX - self.x)/float(slotL) # percent (between 0 and 1.0)

        self.face_color = (150,150,150)
        self.surface = surface

    def draw(self):
        surface = self.surface
        x = self.x
        sliderX = self.sliderX
        bw = self.bw
        y = self.y
        bw = self.bw
        bh = self.bh
        self.percent = (sliderX - x)/float(self.slotL) # percent of motion (between 0 and 1.0)

        #draw Slider Chanel
        sy = y + 0.5* bh    # vertical location of slider slot line
        slotL = self.slotL # length of slot
        pygame.draw.line(surface, (0, 0, 0), (x,sy), (x+slotL,sy),3)
        pygame.draw.line(surface, (255, 255, 255), (x, sy+1), (x+slotL,  sy+1),1)

        #draw slider button
        self.rect = Rect(x+sliderX-.5*bw,y, bw,bh)
        face_color = self.face_color
        pygame.draw.rect(surface, face_color, self.rect)

        #Highlight
        self.pt1 = x+sliderX - .5*bw, y
        self.pt2 = x+sliderX + .5*bw, y   #(pt1,pt2 = top white line)
        self.pt3 = x+sliderX + .5*bw, y+bh #(pt2,pt3 = right white line)
        self.pt4 = x+sliderX - .5*bw, y+bh

        pygame.draw.line(surface, (255, 255, 255), (self.pt1), (self.pt2))#top white line
        pygame.draw.line(surface, (255, 255, 255), (self.pt2), (self.pt3))#right white line
        pygame.draw.line(surface, (100, 100, 100), (self.pt1), (self.pt4))#bot gray line
        pygame.draw.line(surface, (100, 100, 100), (self.pt4), (self.pt3))#left gray line



class MyVerticalSlider:
    def __init__(self,surface,x, y, sliderY, slotL, bw, bh):
        #(x,y) = where on page
        #(sliderY,slotL)location of slider along line, length of slot
        self.x = x
        self.y = y
        self.sliderY = sliderY #- 0.5*bh    # location of slider
        self.slotL = slotL                # lenght of slot

        self.bw = bw # width of slider button
        self.bh = bh # Height of slider button
        #slider button
        self.button_rect = Rect(x-0.5*bw, y+self.sliderY, bw,bh)
        #self.percent = (self.sliderY - self.y)/float(slotL) # percent (between 0 and 1.0)

        self.face_color = (150,150,150)
        self.surface = surface
        self.y_range = slotL - bh

    def draw(self):
        surface = self.surface
        x = self.x
        y = self.y
        bw = self.bw
        bh = self.bh
        #y_range = self.slotL - bh
        ############
        #if self.sliderY - 0.5*bh  <= 0:
        #    sliderY = 0.5*bh
        #elif self.sliderY + 0.5*bh > self.slotL:
        #    sliderY = self.slotL - 0.5*bh
        #else: sliderY = self.sliderY
        #print("sliderY: ",sliderY)
        ###########
        sliderY = self.sliderY
        #self.percent = (sliderY - y)/float(self.slotL) # percent of motion (between 0 and 1.0)
        self.button_rect = Rect(x-0.5*bw, y+self.sliderY, bw,bh)

        #draw Slider Chanel
        slotL = self.slotL # length of slot
        pygame.draw.line(surface, (0, 0, 0), (x,y), (x, y+slotL),3)
        pygame.draw.line(surface, (255, 255, 255), (x+1, y), (x+1,y+slotL),1)

        #draw slider button

        self.button_rect = Rect(int(x-0.5*bw), int(y + sliderY ) , bw, bh)
        face_color = self.face_color
        pygame.draw.rect(surface, face_color, self.button_rect)

        #Button Highlight
        self.pt1 = int(x-0.5*bw),  int(y+sliderY )
        self.pt2 = int(x+0.5*bw),  int(y+sliderY )
        self.pt3 = int(x+0.5*bw),  int(y+sliderY + bh)
        self.pt4 = int(x-0.5*bw),  int(y+sliderY + bh)

        pygame.draw.line(surface, (255, 255, 255), (self.pt1), (self.pt2))#top white line            p1    p2
        pygame.draw.line(surface, (255, 255, 255), (self.pt2), (self.pt3))#right white line          p4    p3
        pygame.draw.line(surface, (100, 100, 100), (self.pt1), (self.pt4))#bot gray line
        pygame.draw.line(surface, (100, 100, 100), (self.pt4), (self.pt3))#left gray line


class MyButton:
    """
    MyButton class
    button_state = "UP" or "DN"
    """
    def __init__(self, surface, index, x, y, w, h, text,fsize = 18):
        self.UP_DN = "UP"
        self.surface = surface
        self.index = index
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.text=text
        self.fsize = fsize
        self.rect = pygame.Rect(x-3,y-3,w+6,h+6) # Expand Rect

        self.face = pygame.Rect(x,y,w,h)
        self.pt1 = x,y
        self.pt2 = x+w,y
        self.pt3 = x+w,y+h
        self.pt4 = x,y+h

        self.face_color = (150,150,150)

    def draw(self):

        self.face = pygame.Rect(self.x,self.y,self.w,self.h)
        self.pt1 = self.x, self.y
        self.pt2 = self.x + self.w, self.y
        self.pt3 = self.x + self.w, self.y + self.h
        self.pt4 = self.x , self.y + self.h
        self.rect = Rect(self.x - 2, self.y - 2,
                         self.w + 4, self.h + 4)
        if self.UP_DN == "UP":
            self.draw_up()
        elif self.UP_DN == "DN":
            self.draw_down()

    def draw_up(self):
        self.UP_DN = "UP"
        surface = self.surface
        face_color = self.face_color
        ln_color=Color('black')
        lw = 4 #Line width
        #draw box
        pygame.draw.rect(surface, ln_color, self.rect)
        pygame.draw.rect(surface, face_color, self.face)
        #Highlight
        pygame.draw.line(surface, (255, 255, 255), (self.pt1), (self.pt2))
        pygame.draw.line(surface, (255, 255, 255), (self.pt2), (self.pt3))
        pygame.draw.line(surface, (100, 100, 100), (self.pt1), (self.pt4))
        pygame.draw.line(surface, (100, 100, 100), (self.pt4), (self.pt3))
        # WRITE LABEL
        my_font = pygame.font.SysFont('arial', self.fsize)
        msg_in_font = my_font.render(self.text, True, Color('white'))
        msgHt =msg_in_font.get_height()
        msgWd = msg_in_font.get_width()
        msgX = (self.rect.width - msgWd)/2
        msgY = (self.rect.height - msgHt)/2
        surface.blit(msg_in_font, self.rect.move(msgX,  msgY))

    def draw_down(self):
        self.UP_DN = "DN"
        surface = self.surface
        face_color = self.face_color
        ln_color=Color('black')
        lw = 4 #Line width
        #Draw Box
        pygame.draw.rect(surface, ln_color, self.rect)
        pygame.draw.rect(surface, face_color, self.face)
        #Highlight
        pygame.draw.line(surface, (255, 255, 255), (self.pt1), (self.pt4))
        pygame.draw.line(surface, (255, 255, 255), (self.pt4), (self.pt3))
        pygame.draw.line(surface, (100, 100, 100), (self.pt1), (self.pt2))
        pygame.draw.line(surface, (100, 100, 100), (self.pt2), (self.pt3))
        # WRITE LABEL text
        my_font = pygame.font.SysFont('arial', self.fsize)
        msg_in_font = my_font.render(self.text, True, Color('white'))
        msgHt =msg_in_font.get_height()
        msgWd = msg_in_font.get_width()
        msgX = (self.rect.width - msgWd)/2
        msgY = (self.rect.height - msgHt)/2
        surface.blit(msg_in_font, self.rect.move(msgX-1,  msgY+2))

class MyLever:
    """

    """
    def __init__(self, surface, index, x, y, w, h, text,fsize = 18):
        self.STATE = "IN" # IN, OUT, or DN.  Use these for GUI display only
        self.PRESSED = False # USE FOR LOGGING AND CONTROLS, NOT THE GUI!
        self.surface = surface
        self.index = index
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.text=text
        self.fsize = fsize
        self.rect = pygame.Rect(x-3,y-3,w+6,h+6) # Expand Rect

        self.face = Rect(x,y,w,h)
        self.pt1 = x,y
        self.pt2 = x+w,y
        self.pt3 = x+w,y+h
        self.pt4 = x,y+h

        self.face_color = (150,150,150)

    def draw(self):
        self.face = Rect(self.x,self.y,self.w,self.h)
        self.pt1 = self.x, self.y
        self.pt2 = self.x + self.w, self.y
        self.pt3 = self.x + self.w, self.y + self.h
        self.pt4 = self.x , self.y + self.h
        self.rect = Rect(self.x - 2, self.y - 2,
                         self.w + 4, self.h + 4)
        if self.STATE == "IN":    # Retracted
            self.draw_in()
        elif self.STATE == "OUT": # Extended
            self.draw_out()
        elif self.STATE == "DN":  # Pressed or "DN"
            self.draw_down()

    def draw_in(self):
        surface = self.surface
        face_color = self.face_color
        ln_color=Color('black')
        lw = 4 #Line width
        #draw box
        pygame.draw.rect(surface, ln_color, self.rect)
        pygame.draw.rect(surface, face_color, self.face)
        #Highlight
        pygame.draw.line(surface, (255, 255, 255), (self.pt1), (self.pt2))
        pygame.draw.line(surface, (255, 255, 255), (self.pt2), (self.pt3))
        pygame.draw.line(surface, (100, 100, 100), (self.pt1), (self.pt4))
        pygame.draw.line(surface, (100, 100, 100), (self.pt4), (self.pt3))
        # WRITE LABEL
        my_font = pygame.font.SysFont('arial', self.fsize)
        msg_in_font = my_font.render(self.text, True, Color('white'))
        msgHt =msg_in_font.get_height()
        msgWd = msg_in_font.get_width()
        msgX = (self.rect.width - msgWd)/2
        msgY = (self.rect.height - msgHt)/2
        surface.blit(msg_in_font, self.rect.move(msgX,  msgY))

    def draw_out(self):
        pt1 = self.x -2 , self.y +2
        pt2 = self.x + self.w-2, self.y +2
        pt3 = self.x + self.w-2, self.y + self.h +2
        pt4 = self.x -2, self.y + self.h +2

        surface = self.surface
        face_color = self.face_color
        ln_color=Color('black')
        lw = 4 #Line width
        #Draw Box
        pygame.draw.rect(surface, ln_color, self.rect)
        self.face = Rect(self.x-2,self.y+2,self.w,self.h)
        pygame.draw.rect(surface, face_color, self.face)
        # Diagonal Highlights
        pygame.draw.line(surface, (0, 0, 0), (self.pt1), (pt1))
        pygame.draw.line(surface, (0, 0, 0), (self.pt2), (pt2))
        pygame.draw.line(surface, (0, 0, 0), (self.pt3), (pt3))
        #Highlight
        pygame.draw.line(surface, (255, 255, 255), (pt1), (pt2))
        pygame.draw.line(surface, (255, 255, 255), (pt2), (pt3))
        pygame.draw.line(surface, (100, 100, 100), (pt1), (pt4))
        pygame.draw.line(surface, (100, 100, 100), (pt4), (pt3))

        # WRITE LABEL text
        my_font = pygame.font.SysFont('arial', self.fsize)
        msg_in_font = my_font.render(self.text, True, Color('white'))
        msgHt =msg_in_font.get_height()
        msgWd = msg_in_font.get_width()
        msgX = (self.rect.width - msgWd)/2
        msgY = (self.rect.height - msgHt)/2
        surface.blit(msg_in_font, self.rect.move(msgX-2,  msgY+2))

    def draw_down(self):
            pt1 = self.x -2 , self.y +5
            pt2 = self.x + self.w-2, self.y +5
            pt3 = self.x + self.w-2, self.y + self.h +5
            pt4 = self.x -2, self.y + self.h +5

            surface = self.surface
            face_color = self.face_color
            ln_color=Color('black')
            lw = 4 #Line width
            #Draw Box
            pygame.draw.rect(surface, ln_color, self.rect)
            self.face = Rect(self.x-2,self.y+5,self.w,self.h)
            pygame.draw.rect(surface, face_color, self.face)
            # Diagonal Highlights
            pygame.draw.line(surface, (0, 0, 0), (self.pt1), (pt1))
            pygame.draw.line(surface, (0, 0, 0), (self.pt2), (pt2))
            pygame.draw.line(surface, (0, 0, 0), (self.pt3), (pt3))
            #Highlight
            pygame.draw.line(surface, (255, 255, 255), (pt1), (pt2))
            pygame.draw.line(surface, (255, 255, 255), (pt2), (pt3))
            pygame.draw.line(surface, (100, 100, 100), (pt1), (pt4))
            pygame.draw.line(surface, (100, 100, 100), (pt4), (pt3))

            # WRITE LABEL text
            my_font = pygame.font.SysFont('arial', self.fsize)
            msg_in_font = my_font.render(self.text, True, Color('white'))
            msgHt =msg_in_font.get_height()
            msgWd = msg_in_font.get_width()
            msgX = (self.rect.width - msgWd)/2
            msgY = (self.rect.height - msgHt)/2
            surface.blit(msg_in_font, self.rect.move(msgX-2,  msgY+5))

class MyToggle:
    """
    MyButton class
    button_state = "LEFT" or "RIGHT"
    """
    def __init__(self, surface, physPinID,  x, y, w, h,visible, LR, text,fsize = 8):
        self.visible = visible
        self.LEFT_RIGHT = LR
        self.myscreen = surface
        self.physPinID = physPinID
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.text=text
        self.fsize = fsize
        self.rect = Rect(x,y,w,h)

    def draw(self):
        if self.visible == 'T':
            myscreen = self.myscreen
            self.rect = Rect(self.x,self.y,self.w,self.h)
            x = self.x
            y = self.y
            r = int(self.h/2)
            w = self.w
            h=self.h
            #draw slot
            black = (0,0,0)
            white = (255,255,255)
            pygame.draw.rect(myscreen, black, self.rect)
            pygame.draw.circle(myscreen, black, (x,y+r), r,0) #(0=fill, 1=outline)
            pygame.draw.circle(myscreen, black, (x+self.w,y+r), int(r),0) #(0=fill, 1=outline)
            if self.LEFT_RIGHT == "LEFT":
                # Switch
                pygame.draw.circle(myscreen, (100,100,100), (x+1,y+r), r-2,0) #(0=fill, 1=outline)
                pygame.draw.circle(myscreen, white, (x+1,y+r), r-2,1) #(0=fill, 1=outline)

            elif self.LEFT_RIGHT == "RIGHT":
                # Switch
                pygame.draw.circle(myscreen, (255,100,100), (x+self.w-1,y+r), r-2,0) #(0=fill, 1=outline)
                pygame.draw.circle(myscreen, white, (x+self.w-1,y+r), r-2,1) #(0=fill, 1=outline)

            # WRITE LABEL
            my_font = pygame.font.SysFont('arial', self.fsize)
            msg_in_font = my_font.render(self.text, True, Color('white'))
            msgHt =msg_in_font.get_height()
            msgWd = msg_in_font.get_width()
            msgX = (self.rect.width - msgWd)/2 - 1
            msgY = (self.rect.height - msgHt)/2 -1
            myscreen.blit(msg_in_font, self.rect.move(msgX,  msgY))


class MyButton2:
    """Button class based on the
    Command pattern."""

    def __init__(self, x, y, w, h, text):
        lw = 4 #line_width
        bw = 2
        self.text=text
        #self.rect = Rect(x-lw,y-lw,w+2*lw,h+2*lw)
        self.rect = Rect(x-bw+1,y-bw+1,w+2*bw,h+2*bw)
        self.face = Rect(x,y,w,h)
        self.pt1 = x,y
        self.pt2 = x+w,y
        self.pt3 = x+w,y+h
        self.pt4 = x,y+h
        self.button_pos = "UP"

    def draw(self,surface):
        if self.button_pos == "UP":
            self.draw_up(surface)
        else:
            self.draw_down(surface)

    def draw_up(self, surface):
        # You could of course use pictures here.
        # This method could also be implemented
        # by subclasses.
        face_color = (150,150,150)
        ln_color=Color('black')
        lw = 4 #Line width
        #pygame.draw.rect(surface,(100,100,100),self.rect)
        pygame.draw.rect(surface, ln_color, self.rect)
        pygame.draw.rect(surface, face_color, self.face)
        #Highlight
        pygame.draw.line(surface, (255, 255, 255), (self.pt1), (self.pt2))
        pygame.draw.line(surface, (255, 255, 255), (self.pt2), (self.pt3))
        pygame.draw.line(surface, (100, 100, 100), (self.pt1), (self.pt4))
        pygame.draw.line(surface, (100, 100, 100), (self.pt4), (self.pt3))
                # WRITE LABEL
        my_font = pygame.font.SysFont('arial', 20)
        msg_in_font = my_font.render(self.text, True, Color('white'))
        msgHt =msg_in_font.get_height()
        msgWd = msg_in_font.get_width()
        msgX = (self.rect.width - msgWd)/2
        msgY = (self.rect.height - msgHt)/2
        surface.blit(msg_in_font, self.rect.move(msgX,  msgY))

    def draw_down(self, surface):
        face_color = (150,150,150)
        ln_color=Color('black')
        lw = 4 #Line width
        #pygame.draw.rect(surface,(100,100,100),self.rect)
        pygame.draw.rect(surface, ln_color, self.rect)
        pygame.draw.rect(surface, face_color, self.face)
        #Highlight
        pygame.draw.line(surface, (255, 255, 255), (self.pt1), (self.pt4))
        pygame.draw.line(surface, (255, 255, 255), (self.pt4), (self.pt3))
        pygame.draw.line(surface, (100, 100, 100), (self.pt1), (self.pt2))
        pygame.draw.line(surface, (100, 100, 100), (self.pt2), (self.pt3))
        # WRITE LABEL
        my_font = pygame.font.SysFont('arial', 20)
        msg_in_font = my_font.render(self.text, True, Color('white'))
        msgHt =msg_in_font.get_height()
        msgWd = msg_in_font.get_width()
        msgX = (self.rect.width - msgWd)/2
        msgY = (self.rect.height - msgHt)/2
        surface.blit(msg_in_font, self.rect.move(msgX,  msgY+1))


def DISPLAY_LEVEL(screen, rect,level):
    my_font = pygame.font.SysFont('arial', 100)
    lvl = 'Level '+str(level)
    level_sf = my_font.render(lvl, True, Color('white'))
    lvlHt = level_sf.get_height()
    screen.blit(level_sf, rect.move(-450, lvlHt +30))  #move score to play area

class MyLED:
    def __init__(self,screen,index, x,y,radius, ONOFF, on_color, background_color, clickable = True):
        self.screen = screen
        self.index = index
        self.x = x
        self.y = y
        self.radius = radius
        diam = radius * 2
        self.diam = diam
        self.rect = Rect(x, y,diam,diam)
        self.ONOFF = ONOFF
        #self.visible = VIS
        self.on_color = on_color
        self.background_color = background_color
        self.off_color = (int(on_color[0]*.2),int(on_color[1]*.2),int(on_color[2]*.2))
        self.clickable = clickable

    def draw(self):
            screen = self.screen
            ONOFF = self.ONOFF
            #self.ONOFF = ONOFF
            x = self.x
            y = self.y
            #diam = self.diam
            radius = self.radius
            cx = x + radius #center x
            cy = y + radius #center y
            diam = 2*radius
            rect = Rect(x, y, diam, diam)
            self.rect = rect
            on_color = self.on_color
            off_color = self.off_color
            background_color = self.background_color

            if ONOFF == "ON":
                #circle(Surface, color, pos, radius, width=0) -> Rect
                #diam = diam + 10
                pygame.draw.circle(screen,on_color,(cx,cy),radius,0)#MAIN BULB
                pygame.draw.circle(screen,(255,255,255),(cx+int(.5*radius),cy+int(.5*radius)),int(.15*radius),0)#SPARKLE
                pygame.draw.circle(screen,(255,255,255),(cx,cy), radius-2,1) # white circle
                pygame.draw.circle(screen,(0,0,0),(cx,cy), radius + 2,4) # Black circle
            elif  ONOFF == "OFF":
                off_color = self.off_color
                pygame.draw.circle(screen,off_color,(cx,cy),radius,0) #MAIN BULB
                pygame.draw.circle(screen,(200,200,200),(cx+int(.5*radius),cy-int(.5*radius)),int(.1*radius),0) #SPARKLE

                pi = 3.141592
                shaddow_color = (int(off_color[0]*.8),int(off_color[1]*.8),int(off_color[2]*.8))
                shadow_w = int(0.5*radius)
                if shadow_w > 15:
                    shadow_w = 15
                shadow_rect = rect
                #shadow_rect = shadow_rect.inflate(3,3)
                pygame.draw.arc(screen, shaddow_color, shadow_rect, 190*pi/180, 270*pi/180, shadow_w) # SHADOW
                pygame.draw.circle(screen,(0,0,0),(cx,cy), radius + 2,3) # Black circle

class MyConditioningLights:
    def __init__(self,screen,index, x,y,radius, ONOFF, on_color, background_color, clickable = True):
        self.screen = screen
        self.index = index
        self.x = x
        self.y = y
        self.radius = radius
        diam = radius * 2
        self.diam = diam
        self.rect = Rect(x, y,diam,diam)
        self.ONOFF = ONOFF
        #self.visible = VIS
        self.on_color = on_color
        self.background_color = background_color
        self.off_color = (int(on_color[0]*.2),int(on_color[1]*.2),int(on_color[2]*.2))
        self.clickable = clickable

    def draw(self):
            screen = self.screen
            ONOFF = self.ONOFF
            #self.ONOFF = ONOFF
            x = self.x
            y = self.y
            #diam = self.diam
            radius = self.radius
            cx = x + radius #center x
            cy = y + radius #center y
            diam = 2*radius
            rect = Rect(x, y, diam, diam)
            self.rect = rect
            on_color = self.on_color
            off_color = self.off_color
            background_color = self.background_color

            if ONOFF == "ON":
                #circle(Surface, color, pos, radius, width=0) -> Rect
                #diam = diam + 10
                pygame.draw.circle(screen,on_color,(cx,cy),radius,0)#MAIN BULB
                pygame.draw.circle(screen,(255,255,255),(cx+int(.5*radius),cy+int(.5*radius)),int(.15*radius),0)#SPARKLE
                pygame.draw.circle(screen,(255,255,255),(cx,cy), radius-2,1) # white circle
                pygame.draw.circle(screen,(0,0,0),(cx,cy), radius + 2,4) # Black circle
            elif  ONOFF == "OFF":
                off_color = self.off_color
                pygame.draw.circle(screen,off_color,(cx,cy),radius,0) #MAIN BULB
                pygame.draw.circle(screen,(200,200,200),(cx+int(.5*radius),cy-int(.5*radius)),int(.1*radius),0) #SPARKLE

                pi = 3.141592
                shaddow_color = (int(off_color[0]*.8),int(off_color[1]*.8),int(off_color[2]*.8))
                shadow_w = int(0.5*radius)
                if shadow_w > 15:
                    shadow_w = 15
                shadow_rect = rect
                #shadow_rect = shadow_rect.inflate(3,3)
                pygame.draw.arc(screen, shaddow_color, shadow_rect, 190*pi/180, 270*pi/180, shadow_w) # SHADOW
                pygame.draw.circle(screen,(0,0,0),(cx,cy), radius + 2,3) # Black circle



class MyNosePokes:
    def __init__(self,screen,index, x,y,radius, ONOFF, on_color, background_color, clickable = True):
        self.screen = screen
        self.index = index
        self.x = x
        self.y = y
        self.radius = radius
        diam = radius * 2
        self.diam = diam
        self.rect = Rect(x, y,diam,diam)
        self.ONOFF = ONOFF
        #self.visible = VIS
        self.on_color = on_color
        self.background_color = background_color
        self.off_color = (int(on_color[0]*.2),int(on_color[1]*.2),int(on_color[2]*.2))
        self.clickable = clickable

    def draw(self):
            screen = self.screen
            ONOFF = self.ONOFF
            #self.ONOFF = ONOFF
            x = self.x
            y = self.y
            #diam = self.diam
            radius = self.radius
            cx = x + radius #center x
            cy = y + radius #center y
            diam = 2*radius
            rect = Rect(x, y, diam, diam)
            self.rect = rect
            on_color = self.on_color
            off_color = self.off_color
            background_color = self.background_color

            if ONOFF == "ON":
                #circle(Surface, color, pos, radius, width=0) -> Rect
                #diam = diam + 10
                pygame.draw.circle(screen,on_color,(cx,cy),radius,0)#MAIN BULB
                #pygame.draw.circle(screen,(255,255,255),(cx+int(.5*radius),cy+int(.5*radius)),int(.15*radius),0)#SPARKLE
                pygame.draw.circle(screen,(255,255,255),(cx,cy), radius-2,1) # white circle
                pygame.draw.circle(screen,(0,0,0),(cx,cy), radius + 2,4) # Black circle
            elif  ONOFF == "OFF":
                off_color = self.off_color
                pygame.draw.circle(screen,off_color,(cx,cy),radius,0) #MAIN BULB
                #pygame.draw.circle(screen,(200,200,200),(cx+int(.5*radius),cy-int(.5*radius)),int(.1*radius),0) #SPARKLE

                pi = 3.141592
                shaddow_color = (int(off_color[0]*.8),int(off_color[1]*.8),int(off_color[2]*.8))
                shadow_w = int(0.5*radius)
                if shadow_w > 15:
                    shadow_w = 15
                shadow_rect = rect
                #shadow_rect = shadow_rect.inflate(3,3)
                pygame.draw.arc(screen, shaddow_color, shadow_rect, 190*pi/180, 270*pi/180, shadow_w) # SHADOW
                pygame.draw.circle(screen,(0,0,0),(cx,cy), radius + 2,3) # Black circle



class MyLabel:
    """Label class based on the
    Types: label, display, default = button
    Command pattern."""

    def __init__(self, surface,  x, y, w, h, text, fsize = 20):
        self.surface = surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text=text
        self.fsize = fsize
        self.rect = Rect(x,y,w,h)

    def draw(self):
        x=self.x
        y=self.y
        w=self.w
        h=self.h
        surface = self.surface
        txt_color = (0,0,0)
        self.rect = Rect(x-2, y-2, w+4, h+4)

        # WRITE LABEL text
        msg_font = pygame.font.SysFont('arial', self.fsize)
        msg_in_font = msg_font.render(self.text, True, txt_color)
        msgHt = msg_in_font.get_height()
        msgWd = msg_in_font.get_width()
        msgX = (self.rect.width - msgWd)/2
        msgY = (self.rect.height - msgHt)/2
        #pygame.draw.rect(surface, txt_color, self.rect,1)
        surface.blit(msg_in_font, self.rect.move(msgX,  msgY+1))


class InfoBox:
    """
    """
    def __init__(self, surface,x, y, w, h, label,label_pos, text ,fsize = 14):
        self.surface = surface
        self.label_pos = label_pos # 'TOP','LEFT','RIGHT', or 'BOTTOM'
        self.surface_color = (255,255,255)
        lw = 1 #line_width
        bw = 2
        self.x,self.y,self.w,self.h = (x, y, w, h)
        self.label = label
        self.text=str(text)
        self.fsize = fsize
        #self.rect = Rect(x-lw,y-lw,w+2*lw,h+2*lw)
        self.rect = Rect(x,y,w,h)
        self.border = Rect(x-bw,y-bw,w+2*bw,h+2*bw)
        self.pt1 = x,y
        self.pt2 = x+w,y
        self.pt3 = x+w,y+h
        self.pt4 = x,y+h

    def draw(self):
        surface = self.surface
        #Draw Box
        pygame.draw.rect(surface, (0,0,0), self.border)
        pygame.draw.rect(surface, (255,255,255), self.rect)
        txt_color = (0,0,0)
        lw = 1 #Line width
        fsize = self.fsize

        # WRITE LABEL
        my_font = pygame.font.SysFont('arial', 14,bold=True)
        lbl_in_font = my_font.render(self.label, True, (0,0,0))
        lblHt =lbl_in_font.get_height()
        lblWd = lbl_in_font.get_width()
        if self.label_pos == 'BOTTOM':
            lblX = (self.rect.width - lblWd)/2 #Center in box
            lblY =  + 20 # Below Box
            #lblY = (self.face.y - lblHt)/2 + 20

        elif self.label_pos == 'TOP':
            lblX = (self.rect.width - lblWd)/2 #Center in box
            lblY =  - 20 #Above box
            #lblY = (self.face.y - lblHt)/2 - 20

        elif self.label_pos == 'LEFT':
            lblX = - lblWd -5
            lblY = (self.rect.height - lblHt)/2

        elif self.label_pos == 'RIGHT':
            #msgX = (self.rect.width - msgWd)/2 + msgWd +10
            lblX =  self.w +5
            lblY = (self.rect.height - lblHt)/2

        surface.blit(lbl_in_font, self.rect.move(lblX,  lblY+1))

        # WRITE TEXT
        lines_in_txt = len(self.text)
        if lines_in_txt > 0: #NOT EMPTY BOX, No info_boxes
            my_font = pygame.font.SysFont('arial', fsize)
            msg_in_font = my_font.render(self.text[0], True, (0,0,0))
            msgHt = msg_in_font.get_height()
            msgWd = msg_in_font.get_width()

            if lines_in_txt == 1: # simple info box
                msgX = (self.rect.width - msgWd)/2 # Center in box
            else: # lines_in_txt > 1:
                msgX = +5 # MULTIPLE LINE INFO BOX: Indent 5 pixels from box left

            ln_count = 0
            for line in self.text:
                msg_in_font = my_font.render(line, True, txt_color)
                msgY =  ln_count * msgHt - 2
                surface.blit(msg_in_font, self.rect.move(msgX,  msgY+1))
                ln_count +=1


class get_user_input:
    def __init__(self, surface,x, y, w, h, label,label_pos, text ,fsize = 14):
        self.TEXT_CHANGED = False
        self.surface = surface
        self.label_pos = label_pos # 'TOP','LEFT','RIGHT', or 'BOTTOM'
        self.surface_color = (255,255,255)
        self.border_color = (0,0,0)
        lw = 1 #line_width
        self.bw = bw = 2
        self.x,self.y,self.w,self.h = (x, y, w, h)
        self.label = label
        self.text=text
        self.fsize = fsize
        #self.rect = Rect(x-lw,y-lw,w+2*lw,h+2*lw)
        self.rect = Rect(x,y,w,h)
        self.border = Rect(x-bw,y-bw,w+2*bw,h+2*bw)
        self.pt1 = x,y     #Top left
        self.pt2 = x+w,y   #Top right
        self.pt3 = x+w,y+h #bottom right
        self.pt4 = x,y+h   #bottom left

    def draw(self):
        surface = self.surface
        #text_input = self.text
        #Draw Box

        pygame.draw.rect(surface, self.border_color, self.border)
        pygame.draw.rect(surface, self.surface_color, self.rect)
        txt_color = (0,0,0)
        lw = 1 #Line width
        fsize = self.fsize

        # WRITE LABEL
        my_font = pygame.font.SysFont('arial', 14,bold=True)
        lbl_in_font = my_font.render(self.label, True, (0,0,0))
        lblHt =lbl_in_font.get_height()
        lblWd = lbl_in_font.get_width()
        if self.label_pos == 'BOTTOM':
            lblX = (self.rect.width - lblWd)/2 #Center in box
            lblY =  + 20 # Below Box
        elif self.label_pos == 'TOP':
            lblX = (self.rect.width - lblWd)/2 #Center in box
            lblY =  - 20 #Above box
        elif self.label_pos == 'LEFT':
            lblX = self.w - msgWd -5
            lblY = (self.rect.height - lblHt)/2
        elif self.label_pos == 'RIGHT':
            lblX =  self.w +5
            lblY = (self.h - lblHt)/2
        surface.blit(lbl_in_font, self.rect.move(lblX,  lblY+1))

        # WRITE TEXT
        my_font2 = pygame.font.SysFont('arial', fsize, bold=True)
        txt_in_font = my_font2.render(self.text, True, Color('black'))
        txtHt = txt_in_font.get_height()
        txtWd = txt_in_font.get_width()
        txtX = (self.rect.width - txtWd)/2 #Center in box
        self.surface.blit(txt_in_font, self.rect.move(txtX,  -1))

    # Get user keyboard input

    def get_key_input(self):
        pygame.draw.rect(self.surface, (0,255,0), self.border)
        surface = self.surface
        fsize = self.fsize
        text_input = self.text
        x = self.x
        y=self.y
        w=self.w
        h=self.h
        bw = self.bw
        NEED_USER_INFO = True
        while NEED_USER_INFO: #Just getting each keypress until ENTER
            my_font2 = pygame.font.SysFont('arial', 14,bold=True)
            txt_in_font = my_font2.render(text_input, True, Color('blue'))
            txtHt = txt_in_font.get_height()
            txtWd = txt_in_font.get_width()

            #txt_in = input(self.txt)
            #print (txt_in)

            for sys_event in pygame.event.get():
                if (sys_event.type == pygame.MOUSEBUTTONDOWN ): #Mouse Clicked
                        # NOTE: LIKE PRESSING RETURN KEY
                        NEED_USER_INFO = False
                        self.text = text_input
                        self.TEXT_CHANGED = True
                        break
                ###################################
                # NEW
                if sys_event.type == pygame.KEYDOWN:
                    char = sys_event.unicode
                    #print(char)
                    if sys_event.key == K_BACKSPACE:
                        text_input = text_input[0:-1] #REMOVE LAST CHAR

                    elif sys_event.key == K_DELETE:
                        text_input = ''

                    elif sys_event.key == K_RETURN:
                        NEED_USER_INFO = False
                        self.text = text_input
                        self.TEXT_CHANGED = True
                        self.border_color = (0,0,0)
                        break

                    else: #COLLECT ENTERRED CHARACTERS
                        try:
                            text_input += char

                            #print (text_input)
                        except:
                            pass

                #######################################
                # OLD
##                if sys_event.type == pygame.KEYDOWN:
##                    #print(sys.event.key)
##                    if sys_event.key == K_BACKSPACE:
##                        text_input = text_input[0:-1] #REMOVE LAST CHAR
##
##                    elif sys_event.key == K_RETURN: # also K_ESCAPE, K_UP, K_DOWN, K_LEFT,K_SPACE, K_n
##                        NEED_USER_INFO = False
##                        self.text = text_input
##                        self.TEXT_CHANGED = True
##                        break
##
##                    else: #COLLECT ENTERRED CHARACTERS
##                        try:
##                            text_input += chr(sys_event.key)
##
##                            print (text_input)
##                        except:
##                            pass
                #######################################
            pygame.draw.rect(surface, (255,255,255), self.rect)
            txt_in_font = my_font2.render(text_input, True, Color('blue'))
            txtX = (self.rect.width - txtWd)/2 #Center in box
            self.surface.blit(txt_in_font,self.rect.move(txtX,-1))#, self.rect.move(txtWd/2,  txtHt/2 - 10))
            pygame.display.flip()


# Draws the playing field with black border, and the border/brown background
# for the messageboard
black = (0,0,0)
class My_Rimmed_Box:
    def __init__(self, surface, x, y, w, h, fill_color, line_color=black):
        self.surface = surface
        #self.physPinID = ID
        self.fill_color = fill_color
        self.line_color = line_color
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        """ Draw a rimmed box on the given surface.
        """
        myscreen = self.surface
        x = self.x
        y = self.y
        self.rect = Rect(x,y,self.w,self.h)
        if self.fill_color != 0:
            pygame.draw.rect(myscreen, self.fill_color , self.rect,  0) #(0=fill, 1=outline line thickness))
        pygame.draw.rect(myscreen, self.line_color , self.rect,  1)

class My_Rimmed_Circle:
    def __init__(self, surface,physPinID,x, y, radius, fill_color,line_color=(0,0,0)):
        self.surface = surface
        self.physPinID = physPinID
        self.fill_color = fill_color
        self.line_color = line_color
        self.x = x
        self.y = y
        cx = x + radius #center x
        cy = y + radius #center y
        self.radius = radius
        self.diam = 2*radius
        self.rect = Rect(x,y,self.diam,self.diam)

    def draw(self):

        """ Draw a rimmed box on the given surface.
        """
        myscreen = self.surface
        x = self.x
        y = self.y
        radius = self.radius
        cx = x + radius #center x
        cy = y + radius #center y
        diam = 2*radius
        rect = Rect(x, y, diam, diam)
        self.rect = rect

        pygame.draw.circle(myscreen, self.fill_color, (cx,cy), radius,0) #(0=fill, 1=outline)
        pygame.draw.circle(myscreen, self.line_color, (cx,cy), radius,2) #(0=fill, 1=outline)

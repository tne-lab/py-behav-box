#!/usr/bin/env python
# whisker/test_twisted.py

'''
ZMQ GUI Publisher

import zmq

# Create the socket
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://localhost:5559")

# Same as before
whiskerThread = threading.Thread(target = whiskerTouchZMQ.main args=(whiskerBack_q) kwargs=({'media_dir' : image_dir}))


# Send your command on socket
socket.send(dict/string of stuff)
'''
###

"""
===============================================================================

    Copyright (C) 2011-2018 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of the Whisker Python client library.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

===============================================================================

**Command-line tool to test the Whisker Twisted client.**

"""

import argparse
#import logging
import zmq
import json
import time
from twisted.internet import reactor

#from cardinal_pythonlib.logs import configure_logger_for_colour

from whisker.api import (
    Pen,
    PenStyle,
    BrushStyle,
    BrushHatchStyle,
    Brush,
    Rectangle,
    DocEventType,
)
from whisker.constants import DEFAULT_PORT
from whisker.twistedclient import WhiskerTwistedTask

DEFAULT_DISPLAY_NUM = 0
#DEFAULT_MEDIA_DIR = r"C:\Program Files (x86)\WhiskerControl\Client Media"
DEFAULT_MEDIA_DIR = r"C:\Users\ephys-2\Documents\GitHub\py-behav-box\TNEL-pyBox\BehGUI\RESOURCES"
DEFAULT_WAV = "telephone.wav"

DISPLAY = "display"
DOC = "doc"
AUDIO = "audio"

class MyWhiskerTask(WhiskerTwistedTask):
    """
    Class deriving from :class:`whisker.twistedclient.WhiskerTwistedTask`
    Creates a task on screen and sends info back to GUI
    """
    def __init__(self,
                 display_num,
                 media_dir,
                 back_q,
                 q
                 ) -> None:

        super().__init__()  # call base class init
        self.display_num = display_num
        self.media_dir = media_dir
        self.back_q = back_q
        self.q = q
        self.pics = []
        self.XYarray = []
        #Brushes + pens: NOTE: colors are (BGR)
        self.brush1 = Brush(
            colour=(0, 0, 0), bg_colour=(0, 255, 0),
            opaque=False)   #BLACK BACKGROUND
        self.brush2 = Brush(
            colour=(5, 5, 5), bg_colour=(0, 255, 0),
            opaque=False)   #Gray dead zone to prevent tail touches
        self.pen = Pen(width=3, colour=(0, 0, 0), style=PenStyle.solid)
        self.brush = Brush(
            colour=(255, 0, 0), bg_colour=(0, 255, 0),
            opaque=True, style=BrushStyle.hatched,
            hatch_style=BrushHatchStyle.bdiagonal) #
        self.background_ht = 0
        self.dead_zone_ht = 250


    def fully_connected(self) -> None: # RUNS ONCE WHEN FULLY CONNECTED
        """
        Called when the server is fully connected. Sets up the "task".
        """
        print("FULLY CONNECTED")
        self.whisker.report_name("Whisker Twisted Client for touchscreen Task")
        self.whisker.timestamps(True)
        # BP
        self.whisker.claim_display(number=self.display_num, alias=DISPLAY)
        #self.whisker.claim_audio(number=0, alias=AUDIO)
        self.whisker.set_media_directory(self.media_dir)
        self.display_size = self.whisker.display_get_size(DISPLAY)
        print('display size\n\n\n', self.display_size)
        self.whisker.display_event_coords(True)

        self.whisker.display_scale_documents(DISPLAY, True)
        bg_col = (0, 0, 100)
        self.whisker.display_blank(DISPLAY)
        # Draw stuff to finish up with setting up connection
        self.RECVFIRST()


    def draw(self):
        '''
        Draws current pics stored in self.pics, background and stop button
        Also creates events corresponding to all
        '''
        # Display stuff on screen
        # Create a new document everytime we draw a new screen. (otherwise we might be drawing stuff on top of eachother.. seems bad)
        self.whisker.display_create_document(DOC)
        self.whisker.display_show_document(DISPLAY, DOC)
        with self.whisker.display_cache_wrapper(DOC):
            # Draw background
            # Lock out botton 100 pixels of display to minimze tail Touches
            self.background_ht = self.display_size[1]-self.dead_zone_ht
            self.whisker.display_add_obj_rectangle(DOC, "background",
                Rectangle(left = 0, top = 0, width = self.display_size[0], height = self.background_ht),
                self.pen, self.brush1)

            # Draw dead zone at bottom of screen.
            # Lock out botton 100 pixels of display to minimze tail Touches
            self.whisker.display_add_obj_rectangle(DOC, "background",
                Rectangle(left = 0, top = self.background_ht, width = self.display_size[0], height = self.dead_zone_ht),
                self.pen, self.brush2)

            # Draw pictures
            for i in range(0,len(self.pics)):

                # Coordinates specified in protocol file
                # Note: Touchscreen is 1024 x (768-deadzone) = 1024 x 518. If we discount the deadzone, the
                #       screen is 1024 x 518.  For picture area to equal to active
                #       background area, picture must be 364 x 364

                bit = self.whisker.display_add_obj_bitmap(
                    DOC,"picture" + str(i), self.XYarray[i], filename=self.pics[i],
                    stretch = True , height =300, width = 300) # Returns T or F
                if not bit:
                    pass
            self.whisker.display_send_to_back(DOC, "background")
            self.setEvents()

    # Handle creation/deletion of picture Events
    def setEvents(self):
        # Set events for all pictures
        for i in range(0,len(self.pics)):
            print(self.pics)
            if self.pics[i] == "BLANK.BMP":
                print('LOOKING FOR UP\n\n')
                self.whisker.display_set_event(DOC, "picture" + str(i), self.pics[i], DocEventType.touch_up)
            else:
                self.whisker.display_set_event(DOC, "picture" + str(i), self.pics[i], DocEventType.touch_down)
        # Set event for background and end of task
        self.whisker.display_set_event(DOC, "background", "missedClick",DocEventType.touch_down)
        self.whisker.timer_set_event("checkZMQ", 5, -1)

    def clearEvents(self):
        # Clears events and DOC for all pictures to get ready for new ones
        for i in range(0,len(self.pics)):
            self.whisker.display_clear_event(DOC, "picture" + str(i))
        self.whisker.display_clear_event(DOC, "background")
        self.whisker.timer_clear_event("checkZMQ")
        self.whisker.display_delete_document(DOC)




    #############################################
    # NOW WE WAIT FOR REACTOR TO SEND US AN EVENT.  WHEN
    # When REACTOR sees an event, incoming_event runs
    # Handle event ***
    def incoming_event(self, event: str, timestamp: int = None) -> None:
        """
        Responds to incoming events from Whisker.
        """
        #print("Event: {e} (timestamp {t})".format(e=event, t=timestamp))
        try:
            event, x, y = event.split(' ')
            # Clicked background
            if "missedClick" == event:
                if int(y) <= self.background_ht:
                    sendDict = {'picture' : 'missed', 'XY' : (x,y)}
                    #print(sendDict)
                    self.back_q.put(sendDict)
                else:
                    print('deadzone hit')
                #self.whisker.audio_play_wav(AUDIO, DEFAULT_WAV)
            # Or a picture
            else:
                for picName in self.pics:
                    if picName == event:
                        sendDict = {'picture' : picName, 'XY' : (x,y)}
                        #print(sendDict)
                        self.back_q.put(sendDict)
                        self.RECVCMD()
        except ValueError:
            if "checkZMQ" in event:
                #print('echingQ')
                self.RECVCMD()

    ######## zmq ###############
    # Looks at the q for a message from GUI
    def RECVCMD(self):
        if not self.q.empty():
            self.parseMsg(self.q.get())

    # Need to wait for first msg from GUI before proceeding
    def RECVFIRST(self): # Note: runs once
        while True:
            time.sleep(0.01)
            if not self.q.empty():
                self.parseMsg(self.q.get())
                break

    # Parses JSON msg from GUI
    def parseMsg(self, msg):
        # Clear events and then look for msg

        # Parse msg
        if msg == 'STOP':
            reactor.stop()
            return
        elif msg == '':
            self.pics = []
            self.XYarray = []
        else:
            pics = []
            XYarray = []
            for img, coords in msg.items():
                #print(img,coords)
                pics.append(img)
                XYarray.append(coords)
            self.pics = pics
            self.XYarray = XYarray
        self.clearEvents()

        # Draw new screen
        self.draw()

def main(back_q, q, display_num = DEFAULT_DISPLAY_NUM, media_dir = DEFAULT_MEDIA_DIR, port = DEFAULT_PORT):
    '''
    Generates a touchscreen task.
    '''
    w = MyWhiskerTask(
        display_num=display_num,
        media_dir=media_dir,
        back_q = back_q,
        q = q
    )
    w.connect('localhost', port)

    while True:
        try:
            reactor.run() # starts Twisted and thus network processing
            break
        except: print('trying to start touchscreen, if stuck check whiskerTouch main')
    # ***
    # Note: This is BAD programming in my opinion. The logical flow is interrupted.
    # The Reactor is basically an event alarm. The program sits and waits until an event is
    # geneated by the reactor.  When a event is received, the incoming_event() is run,
    # but note that incomming event is not in any loop.  This is not a logical linear flow!
    # We aplolgize for doing it this way, but it the way Twisted and Whisker server work.

if __name__ == '__main__':
    main()

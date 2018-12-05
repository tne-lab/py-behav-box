#!/usr/bin/env python
# whisker/test_twisted.py

'''
!!!!!! MARKS COMMENTS !!!!!!
So our bmp file was too big. Made a tiny one in paint and it works. Only works with bmp files. It also
    gens events when you click on the picture which is sweet!
Sound works (Click right polygon to hear it). We had to claim the audio device first!
Videos don't work because of how whiskerserver is configured. They were orignally disabled, but even after
    changing that they still don't work. Not really important though..
Big problem to worry about now is why it doesn't work when called outside idle. Tried to use cmd while GUI was running,
    but throws some sort of socket module error. Something weird with naming of files and importing the wrong one I believe
    Probably will be tough to fix that. Might need to be clever in how we call this.
Also changed left polygon, will now close the program if you're confused why its closing.


Probably am going to send this to myself and make it pretty/easy to use tomorrow.
Use zmq or deque depending on if thread or separate process. thinking thread
!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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

from twisted.internet import reactor

#from cardinal_pythonlib.logs import configure_logger_for_colour
from whisker.api import (
    Pen,
    PenStyle,
    BrushStyle,
    BrushHatchStyle,
    Brush,
    Rectangle,
)
from whisker.constants import DEFAULT_PORT
from whisker.twistedclient import WhiskerTwistedTask

#log = logging.getLogger(__name__)

DEFAULT_DISPLAY_NUM = 0
DEFAULT_MEDIA_DIR = r"C:\Program Files (x86)\WhiskerControl\Client Media"
DEFAULT_WAV = "telephone.wav"

DISPLAY = "display"
DOC = "doc"
AUDIO = "audio"


class MyBanditTask(WhiskerTwistedTask):
    """
    Class deriving from :class:`whisker.twistedclient.WhiskerTwistedTask`
    Creates a bandit task on screen and sends info back to GUI
    """
    def __init__(self,
                 media_dir,
                 pics,
                 XYarray
                 ) -> None:
        
        super().__init__()  # call base class init
        self.display_num = 0
        self.media_dir = media_dir
        self.pics = pics
        self.XYarray = XYarray
        # ... anything extra here

    def fully_connected(self) -> None:
        """
        Called when the server is fully connected. Sets up the "task".
        """
        #self.whisker.get_network_latency_ms()
        self.whisker.report_name("Whisker Twisted Client for Bandit Task")
        self.whisker.timestamps(True)
        #self.whisker.timer_set_event("checkQ", 1000) # Want something like this to end task on no response(or between trials)

        # End of task timer
        self.whisker.timer_set_event("TmrEndOfTask", 30000) #creates a timer event! EndOfTask is a timer event, here 30,000 = 30 sec

        # Sets background, pen and brush color. Probably won't even use if we want pics.
        bg_col = (0, 0, 100)
        pen = Pen(width=3, colour=(255, 255, 150), style=PenStyle.solid)
        brush = Brush(
            colour=(255, 0, 0), bg_colour=(0, 255, 0),
            opaque=True, style=BrushStyle.hatched,
            hatch_style=BrushHatchStyle.bdiagonal)

        brush1 = Brush(
            colour=(0, 0, 0), bg_colour=(0, 255, 0),
            opaque=False)

        # BP
        self.whisker.claim_display(number=self.display_num, alias=DISPLAY)
        self.whisker.claim_audio(number=0, alias=AUDIO)
        self.whisker.set_media_directory(self.media_dir)
        display_size = self.whisker.display_get_size(DISPLAY)
        self.whisker.display_event_coords(True)

        self.whisker.display_scale_documents(DISPLAY, True)
        self.whisker.display_create_document(DOC)
        self.whisker.display_set_background_colour(DOC, bg_col)
        self.whisker.display_blank(DISPLAY)

        # Display stuff on screen
        self.whisker.display_show_document(DISPLAY, DOC)
        with self.whisker.display_cache_wrapper(DOC):
            # Draw background
##
##            brush1 = Brush(
##                colour=(0, 0, 0), bg_colour=(0, 255, 0),
##                opaque=False)
            
            self.whisker.display_add_obj_rectangle(DOC, "background",
                Rectangle(left = 0, top = 0, width = display_size[0], height = display_size[1]),
                pen,brush1)

            # Draw stop button (only for debugging)
            self.whisker.display_add_obj_rectangle(
                DOC, "rectangle",
                Rectangle(left=10, top=10, width=50, height=50),
                pen, brush)

            # Draw pictures
            for i in range(0,len(self.pics)):
                bit = self.whisker.display_add_obj_bitmap(
                    DOC,"picture" + str(i),self.XYarray[i],filename=self.pics[i],
                    stretch = False, height = 100, width = 100)
                if not bit:
                    print('failed drawing picture')
            self.whisker.display_send_to_back(DOC, "background")

        # Set events for all pictures
        for i in range(0,len(self.pics)):
            print("Self.pics: ", self.pics)
            self.whisker.display_set_event(DOC, "picture" + str(i), self.pics[i])
        # Set event for background and end of task
        self.whisker.display_set_event(DOC, "rectangle", "RectEndOfTask")
        self.whisker.display_set_event(DOC, "background", "missedClick")

    # Handle event
    def incoming_event(self, event: str, timestamp: int = None) -> None:
        """
        Responds to incoming events from Whisker.
        """
        print("Event: {e} (timestamp {t})".format(e=event, t=timestamp))
        try:
            event, x, y = event.split(' ')
            if "missedClick" == event:
                sendDict = {'picture' : 'missed', 'XY' : (x,y)}
                print(sendDict)
                #deque.append(sendDict)  a dict of current state
                self.whisker.audio_play_wav(AUDIO, DEFAULT_WAV)
            elif "EndOfTask" in event:
                reactor.stop()  
            else:
                for i in self.pics:
                    if i == event:
                        sendDict = {'picture' : str(i), 'XY' : (x,y)}
                        print(sendDict)
                        return
                    print('unhandled event')
        except ValueError:
            if "EndOfTask" in event:
                reactor.stop()
            if "checkQ" in event:
                try:
                    deque.pop()
                    #handle that
                except:
                    pass
        
                #deque.append(sendDict)  a dict of current state
        

# going to change this depending on how we want to use this
# Probably a different function(and class) for the different protocols (bandit...etc)
def bandit( media_dir = DEFAULT_MEDIA_DIR,
            pics = ['test.bmp', 'santa_fe.bmp'],
            XYarray = [(0,100),(250,100)]):
    '''
    Generates a bandit task. NO SPACES IN FILENAMES!
    '''
    w = MyBanditTask(
        media_dir=media_dir,
        pics = pics,
        XYarray = XYarray
    )
    w.connect('localhost', DEFAULT_PORT)
    reactor.run()

if __name__ == '__main__':
    bandit()

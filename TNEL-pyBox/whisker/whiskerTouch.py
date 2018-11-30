#!/usr/bin/env python
# whisker/test_twisted.py

'''
import whiskerTouch

whiskerThread = threading.Thread(target = whiskerTouch.main args=(whiskerQ,whiskerBack_q))

for i in range(0,trials-1):
    whiskerQ.put({'end' : False, 'next' : True, 'pics': ['santa_fe.bmp','test.bmp'], 'XYarray' : [(0,100),(250,100)]})


whiskerThread.start() 
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
import logging

from twisted.internet import reactor

from cardinal_pythonlib.logs import configure_logger_for_colour
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

log = logging.getLogger(__name__)

DEFAULT_DISPLAY_NUM = 0
DEFAULT_MEDIA_DIR = r"C:\Program Files (x86)\WhiskerControl\Client Media"
DEFAULT_WAV = "telephone.wav"

DISPLAY = "display"
DOC = "doc"
AUDIO = "audio"


class MyWhiskerTask(WhiskerTwistedTask):
    """
    Class deriving from :class:`whisker.twistedclient.WhiskerTwistedTask`
    Creates a bandit task on screen and sends info back to GUI
    """
    def __init__(self,
                 display_num,
                 media_dir,
                 pics,
                 XYarray,
                 trial_length,
                 ON_RESPONSE,
                 q,
                 back_q
                 ) -> None:

        super().__init__()  # call base class init
        self.display_num = display_num
        self.media_dir = media_dir
        self.pics = pics
        self.XYarray = XYarray
        self.trial_length = trial_length
        self.q = q
        self.back_q = back_q
        #Brushes + pens
        self.brush1 = Brush(
            colour=(0, 0, 0), bg_colour=(0, 255, 0),
            opaque=False)
        self.pen = Pen(width=3, colour=(255, 255, 150), style=PenStyle.solid)
        self.brush = Brush(
            colour=(255, 0, 0), bg_colour=(0, 255, 0),
            opaque=True, style=BrushStyle.hatched,
            hatch_style=BrushHatchStyle.bdiagonal)
        # ... anything extra here

    def fully_connected(self) -> None:
        """
        Called when the server is fully connected. Sets up the "task".
        """
        self.whisker.report_name("Whisker Twisted Client for touchscreen Task")
        self.whisker.timestamps(True)



        # BP
        self.whisker.claim_display(number=self.display_num, alias=DISPLAY)
        self.whisker.claim_audio(number=0, alias=AUDIO)
        self.whisker.set_media_directory(self.media_dir)
        display_size = self.whisker.display_get_size(DISPLAY)
        self.whisker.display_event_coords(True)

        self.whisker.display_scale_documents(DISPLAY, True)
        bg_col = (0, 0, 100)
        self.whisker.display_blank(DISPLAY)
        # Draw stuff to finish up with setting up connection
        self.draw()


    def draw(self):
        '''
        Draws current pics stored in self.pics, background and stop button
        Also creates events corresponding to all
        '''
        display_clear_event(doc: str, obj: str, event_type: whisker.api.DocEventType = <DocEventType.touch_down: 5>)
        display_set_event(doc: str, obj: str, event: str, event_type: whisker.api.DocEventType = <DocEventType.touch_down: 5>)
        # Display stuff on screen
        # Create a new document everytime we draw a new screen. (otherwise we might be drawing stuff on top of eachother.. seems bad)
        self.whisker.display_create_document(DOC)
        self.whisker.display_show_document(DISPLAY, DOC)
        with self.whisker.display_cache_wrapper(DOC):
            # Draw background
            self.whisker.display_add_obj_rectangle(DOC, "background",
                Rectangle(left = 0, top = 0, width = display_size[0], height = display_size[1]),
                self.pen, self.brush1)

            # Draw stop button (only for debugging)
            self.whisker.display_add_obj_rectangle(
                DOC, "rectangle",
                Rectangle(left=10, top=10, width=50, height=50),
                self.pen, self.brush)

            # Draw pictures
            for i in range(0,len(self.pics)):
                bit = self.whisker.display_add_obj_bitmap(
                    DOC,"picture" + str(i),self.XYarray[i],filename=self.pics[i],
                    stretch = False, height = 100, width = 100)
                if not bit:
                    print('failed drawing picture')
            self.whisker.display_send_to_back(DOC, "background")
            self.setPicEvents()

    # Handle creation/deletion of picture Events
    def setPicEvents(self):
        # Set event for trial length
        self.whisker.timer_set_event("TmrEndOfTrial", trial_length*1000)
        # Set events for all pictures
        for i in range(0,len(self.pics)):
            self.whisker.display_set_event(DOC, "picture" + str(i), self.pics[i])
        # Set event for background and end of task
        self.whisker.display_set_event(DOC, "rectangle", "RectEndOfTask")
        self.whisker.display_set_event(DOC, "background", "missedClick")
    def clearPicEvents(self):
        # Clears events for all pictures to get ready for new ones
        for i in range(0,len(self.pics)):
            self.whisker.display_clear_event(DOC, "picture" + str(i))
        self.whisker.display_clear_event(DOC, "rectangle")
        self.whisker.display_clear_event(DOC, "background")
        self.whisker.timer_clear_event("TmrEndOfTrial")
    #############################################

    # Handle event
    def incoming_event(self, event: str, timestamp: int = None) -> None:
        """
        Responds to incoming events from Whisker.
        """
        print("Event: {e} (timestamp {t})".format(e=event, t=timestamp))
        try:
            event, x, y = event.split(' ')
            # Clicked background
            if "missedClick" == event:
                sendDict = {'picture' : 'missed', 'XY' : (x,y)}
                print(sendDict)
                self.back_q.put(sendDict)
                self.whisker.audio_play_wav(AUDIO, DEFAULT_WAV)
            elif "EndOfTask" in event:
                # Remove this eventually when done debugging
                reactor.stop()
            # Or a picture
            else:
                for i in self.pics:
                    if i == event:
                        sendDict = {'picture' : str(i), 'XY' : (x,y)}
                        print(sendDict)
                        self.back_q.put(sendDict)
                        if self.ON_RESPONSE:
                            self.checkQ()
        except ValueError:
            if "EndOfTrial" in event:
                self.checkQ()

    def checkQ(self):
        if self.q.empty():
            print('nothing from GUI --- Stopping')
            reactor.stop()
        else:
            msg = self.q.get()
            if msg['end'] == True:
                reactor.stop()
            if msg['next'] == True:
                self.clearPicEvents()
                self.whisker.display_delete_document(DOC)
                self.pics = msg['pics']
                self.XYarray = msg['XYarray']
                self.draw()


def main(q, back_q, display_num = DEFAULT_DISPLAY_NUM, media_dir = DEFAULT_MEDIA_DIR,
    pics = ['test.bmp', 'santa_fe.bmp'], port = DEFAULT_PORT, XYarray = [(0,100),(250,100)],
    trial_length = 30, ON_RESPONSE = False):
    '''
    Generates a touchscreen task.
    NO SPACES IN FILENAMES!
    '''
    w = MyWhiskerTask(
        display_num=display_num,
        media_dir=media_dir,
        pics = pics,
        XYarray = XYarray,
        trial_length = trial_length,
        ON_RESPONSE = ON_RESPONSE,
        q = q,
        back_q = back_q
    )
    w.connect('localhost', port)
    reactor.run()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# whisker/test_twisted.py

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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!
**Command-line tool to test the Whisker Twisted client.**
Modified by Flavio J.K. daSilva and Mark Scatza on 11/29/2018
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
DEFAULT_AUDIO_NUM = 20
DEFAULT_INPUT_LINE = 0
DEFAULT_OUTPUT_LINE = 64
#DEFAULT_MEDIA_DIR = r"C:\Users\ephys-2\Desktop\BehChamGUI"
DEFAULT_MEDIA_DIR = r"C:\Program Files (x86)\WhiskerControl\Server Test Media"
DEFAULT_BITMAP = "santa_fe.bmp"
DEFAULT_VIDEO = "mediaexample.wmv"
DEFAULT_WAV = "telephone.wav"

AUDIO = "audio"
DISPLAY = "display"
DOC = "doc"
VIDEO = "_video"


class MyWhiskerTwistedTask(WhiskerTwistedTask):
    """
    Class deriving from :class:`whisker.twistedclient.WhiskerTwistedTask` to
    demonstrate the Twisted Whisker client.
    """
    def __init__(self,
                 display_num: int,
                 audio_num: int,
                 input_line: str,
                 output_line: str,
                 media_dir: str,
                 bitmap: str,
                 video: str,
                 wav: str
                 ) -> None:
        super().__init__()  # call base class init
        self.display_num = display_num
        self.input = input_line
        self.output = output_line
        ###
        self.media_dir = media_dir
        self.audio_num = audio_num
        self.input = input_line
        self.output = output_line
        self.media_dir = media_dir
        self.bitmap = bitmap
        self.video = video
        self.wav = wav
        # ... anything extra here
        print ("DISPLAY: ",display_num)
        print ("input line: ",input_line)
        print ("output_line: ",output_line)
        
    def fully_connected(self) -> None:
        """
        Called when the server is fully connected. Set up the "task".
        """
        print("SENDING SOME TEST/DEMONSTRATION COMMANDS")
        #self.whisker.get_network_latency_ms()
        #self.whisker.report_name("Whisker Twisted client prototype")
        self.whisker.timestamps(True)
        #---------------------------------------------------
        # Timer events
        #---------------------------------------------------
        #self.whisker.timer_set_event("TimerFired", 1000, 9)
        self.whisker.timer_set_event("TmrEndOfTask", 60000) #creates a timer event! EndOfTask is a timer event, here 30,000 = 30 sec
        #audio_play_wav(device: str, filename: str) 
        # ---------------------------------------------------------------------
        # Display
        # ---------------------------------------------------------------------
        bg_col = (0, 0, 100)
        pen = Pen(width=3, colour=(255, 255, 150), style=PenStyle.solid)
        brush1 = Brush(
            colour=(255, 0, 0), bg_colour=(0, 255, 0),
            opaque=True, style=BrushStyle.hatched,
            hatch_style=BrushHatchStyle.bdiagonal)
        brush2 = Brush(
            colour=(255, 0, 0), bg_colour=(0, 255, 0),
            opaque=True, style=BrushStyle.solid)        
        self.whisker.claim_display(number=self.display_num, alias=DISPLAY)
        display_size = self.whisker.display_get_size(DISPLAY)
        #log.info("display_size: {}".format(display_size))
        self.whisker.display_scale_documents(DISPLAY, True)
        self.whisker.display_create_document(DOC)
        self.whisker.display_set_background_colour(DOC, bg_col)
        self.whisker.display_blank(DISPLAY)
        self.whisker.display_show_document(DISPLAY, DOC)
        
        with self.whisker.display_cache_wrapper(DOC):

##            self.whisker.display_add_obj_line(
##                DOC, "_line", (25, 25), (200, 200), pen)
##            self.whisker.display_add_obj_arc(
##                DOC, "_arc",
##                Rectangle(left=100, top=100, width=200, height=200),
##                (25, 25), (200, 200), pen)
##            self.whisker.display_add_obj_bezier(
##                DOC, "_bezier",
##                (100, 100), (150, 100),
##                (150, 200), (100, 200),
##                pen)
##            self.whisker.display_add_obj_chord(
##                DOC, "_chord",
##                Rectangle(left=300, top=0, width=100, height=100),
##                (100, 150), (400, 175),
##                pen, brush)
##            self.whisker.display_add_obj_ellipse(
##                DOC, "_ellipse",
##                Rectangle(left=0, top=200, width=200, height=100),
##                pen, brush)
##            self.whisker.display_add_obj_pie(
##                DOC, "_pie",
##                Rectangle(left=0, top=300, width=200, height=100),
##                (10, 320), (180, 380),
##                pen, brush)
            poly = self.whisker.display_add_obj_polygon(
                DOC, "polygon1",
                [(400, 200), (450, 300), (400, 400), (300, 300)],
                pen, brush1, alternate=True)
            self.whisker.display_add_obj_polygon(
                DOC, "polygon2",
                [(100, 200), (150, 300), (100, 400), (0, 300)],
                pen, brush1, alternate=True)
            self.whisker.display_add_obj_rectangle(
                DOC, "rectangle",
                Rectangle(left=10, top=10, width=50, height=50),
                pen, brush2)
            self.whisker.display_add_obj_text(
                DOC, "_text", (20, 20), "STOP",
                italic=False,height=16)
            bitmap = self.whisker.display_add_obj_bitmap(
                DOC,"logo",(200,200),filename='test.bmp',
                stretch = False)#, height = 10, width = 10)

            print("POLY: ", poly,"BITMAP: ",bitmap)

        self.whisker.display_set_audio_device(DISPLAY, AUDIO)    
        self.whisker.display_set_obj_event_transparency(DOC, "_rectangle", False) 
        self.whisker.display_bring_to_front(DOC, "logo")
        #self.whisker.display_send_to_back(DOC, "_chord")
##            self.whisker.display_add_obj_roundrect(
##                DOC, "_roundrect",
##                Rectangle(left=500, top=200, width=100, height=200),
##                150, 250,
##                pen, brush)
##            self.whisker.display_add_obj_camcogquadpattern(
##                DOC, "_camcogquad",
##                (500, 400),
##                10, 10,
##                [1, 2, 4, 8, 16, 32, 64, 128],
##                [255, 254, 253, 252, 251, 250, 249, 248],
##                [1, 2, 3, 4, 5, 6, 7, 8],
##                [128, 64, 32, 16, 8, 4, 2, 1],
##                (255, 0, 0),
##                (0, 255, 0),
##                (0, 0, 255),
##                (255, 0, 255),
##                (100, 100, 100))
        self.whisker.display_set_event(DOC, "polygon1", "poly1_touched") # shape, name givien to event when shape touched
        self.whisker.display_set_event(DOC, "polygon2", "poly2_touched") # shape, name givien to event when shape touched

##        self.whisker.display_clear_event(DOC, "_polygon")
##        self.whisker.display_set_event(DOC, "_camcogquad", "play")
##        self.whisker.display_set_event(DOC, "_roundrect", "pause")
        self.whisker.display_set_event(DOC, "rectangle", "RectEndOfTask")
        self.whisker.display_set_event(DOC, "logo", "LOGO_pressed")
##        self.whisker.display_set_obj_event_transparency(DOC, "_rectangle", False)
##        self.whisker.display_bring_to_front(DOC, "_chord")
##        self.whisker.display_send_to_back(DOC, "_chord")
        self.whisker.display_keyboard_events(DOC)

        self.whisker.display_event_coords(True) # was         self.whisker.display_event_coords(False)

    def incoming_event(self, event: str, timestamp: int = None) -> None:
        """
        Responds to incoming events from Whisker.
        """
        print("Event: {e} (timestamp {t})".format(e=event, t=timestamp))
        if "EndOfTask" in event:
            reactor.stop()
        if "poly1_touched" in event:
            self.whisker.audio_play_wav(AUDIO, DEFAULT_WAV) 
def main() -> None:
    """
    Command-line parser.
    See ``--help`` for details.
    """
    logging.basicConfig()
    logging.getLogger("whisker").setLevel(logging.DEBUG)
    configure_logger_for_colour(logging.getLogger())  # configure root logger
    # print_report_on_all_logs()

    parser = argparse.ArgumentParser("Test Whisker raw socket client")
    parser.add_argument('--server', default='localhost',
                        help="Server (default: localhost)")
    parser.add_argument('--port', default=DEFAULT_PORT, type=int,
                        help="Port (default: {})".format(DEFAULT_PORT))
    parser.add_argument(
        '--display_num', default=DEFAULT_DISPLAY_NUM, type=int,
        help="Display number to use (default: {})".format(DEFAULT_DISPLAY_NUM))
    parser.add_argument(
        '--audio_num', default=DEFAULT_AUDIO_NUM, type=int,
        help="Audio device number to use (default: {})".format(
            DEFAULT_AUDIO_NUM))
    parser.add_argument(
        '--input', default=DEFAULT_INPUT_LINE, type=int,
        help="Input line number to use (default: {})".format(
            DEFAULT_INPUT_LINE))
    parser.add_argument(
        '--output', default=DEFAULT_OUTPUT_LINE, type=int,
        help="Output line number to use (default: {})".format(
            DEFAULT_OUTPUT_LINE))
    parser.add_argument(
        '--media_dir', default=DEFAULT_MEDIA_DIR, type=str,
        help="Media directory to use (default: {})".format(
            DEFAULT_MEDIA_DIR))
    parser.add_argument(
        '--bitmap', default=DEFAULT_BITMAP, type=str,
        help="Bitmap to use (default: {})".format(DEFAULT_BITMAP))
    parser.add_argument(
        '--video', default=DEFAULT_VIDEO, type=str,
        help="Video to use (default: {})".format(DEFAULT_VIDEO))
    parser.add_argument(
        '--wav', default=DEFAULT_WAV, type=str,
        help="WAV file to use (default: {})".format(DEFAULT_WAV))
    ###
    args = parser.parse_args()
    print("\n.................................")
    print("\nModule run explicitly. Running a Whisker test.")
    w = MyWhiskerTwistedTask(
        display_num=args.display_num,
        audio_num=args.audio_num,
        input_line=args.input,
        output_line=args.output,
        media_dir=args.media_dir,
        bitmap=args.bitmap,
        video=args.video,
        wav=args.wav,
    )
    w.connect(args.server, args.port)
    reactor.run() # imported from twisted.internet 


if __name__ == '__main__':
    main()

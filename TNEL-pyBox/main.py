# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 12:35:01 2018

@author: Ephys
"""

import daqAPI


def main():
    #Set Address and pulse enable bit(Maybe only need to do this once because nonlatching)
    daqAPI.startUpBox()
    
    leftOrRight = 'Right'
    
    try:
        while True:
            daqAPI.pushOutLevers()
            
            #Loop waiting for press to occur
            press = daqAPI.detectPress()
            
            #Increment left/right press
            daqAPI.pullInLevers()
            
            #Check if pressed correct 
            if (press == leftOrRight):
                daqAPI.giveFood()
                
    except KeyboardInterrupt:
        pass
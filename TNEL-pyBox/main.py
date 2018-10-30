# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 12:35:01 2018
@author: Ephys
"""

import daqAPI
import time

def leverTest():
    #Push out levers
    leverOutput = daqAPI.leverOutputSetup()
    leverOutput.sendDByte(3)

    #Check for press
    [checkPressLeft, checkPressRight] = daqAPI.leverInputSetup()
    press = daqAPI.detectPress(checkPressLeft,checkPressRight)
    #Pull Levers in
    leverOutput.sendDByte(0)

    print(press)

def main():
    leverTest()


main()

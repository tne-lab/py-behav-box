# BehavioralChamber

In development python based GUI used to manage rat behavioral box's with customizable GUI and protocol format.

![TNEL Logo](/images/TNELogo.jpg)

## Installation
WIP.

### Dependencies
python3+ (untested but probably 3.5+)

opencv

whisker

zmq

## Usage
We use a batch file to open the GUI.
```
cd PATH_TO_GUI
python BEH_GUI_MAIN.py
```

![GUI Image](/images/pyBox.png)


### Edit Box details
daqAPI.py correlates port numbers to input/output responses.

### Protocols
See "all about protocols" file in PROTOCOLS folder.

Basic Overview:

[EXPERIMENT] set path and naming

Then specific box items

[SETUP] is used for various switches to be set

[PROTOCOL] The experimental parameters, runs similar to a for loop

[Conditions]
correlates an input from chamber to an output along with timing

## Coding style overview
Two classes: GUI and Experiment

Gui holds GUI information and handles communication with behavioral box. Only to be updated if new GUI element needed to either show a new box input/output or if want to show new information.

Experiment handles running the testing. Should be changed to add new options in protocol.

## Info

This is being actively developed by the TNE-Lab at the University of Minnesota - Twin Cities.

Contact dasilvaf@umn.edu or schat107@umn.edu for more information

# Py-Behav-Box Developement Guide v1.0

## Overview
I view this code as split into two main classes with helper functions and one big helper function to load in files. BEH_GUI_MAIN creates a GUI class instance. Only one is created everytime you open the program and handles all interaction with the user. experiment creates a new expt class instance for every new experiment started. The user doesn't really directly interact with the expt class. The loadProtocol function is how we go from a txt file with the protocol and variables needed to something that the expt class can read. I've split this guide into three parts for each of those. 

## BEH_GUI_MAIN
This is our main file where the program starts. It starts by setting globals and loading in a basic protocol. Then it loops through the drawScreen(), checkSystemEvents(), and checkNIDAQEvents() functions until the GUI is closed. Note all functions here are pretty solid and unless adding in new functionality to GUI or user interaction it should work as is. Mostly Flavio's work, so reach out to him if any questions on these things.

#### setGUIGlobals())
Global variables for exterior inputs (lever presses, fans, etc) and very basic time/date things.

TODO: Move Tone/Shock to loadProtocol. Probably move camera stuff as well. Handle TouchScreen better. 

#### setupExpt()
Gets called any time a new experiment is loaded in. Sets up GUI based upon inputs being used and creates a new experiment class instance.

#### DrawScreen()
Draws and updates GUI according to state of the experiment or button clicks.

#### checkSystemEvents()
Looks for computer events. Mostly button clicks and keyboard presses.

#### checkNidaqEvents()
Checks if anything has happened in the behavioral chamber. Sets values accordingly so experiment can be notified.

## loadProtocol
When a new protocol is loaded in this function takes care of setting up the experimental variables needed. Read all about protocols doc to learn more.

This function runs line by line through the txt file. # lines are considered comments. We use a name value pair 'name=value'. Name value pairs are held within subclasses to make creating new variables easy to understand. Adding in new features is very easy here. First create a new subclass using the '\[NEW_CLASS]' format. Add an 'elif \[NEW_CLASS]' to notify you are currently in that subclass. Then add an 'elif currentlySetting == \[NEW_CLASS]'. Check if current line says '\[NEW_CLASS]' and create your default values here. Then list your name value pairs to be set. Be sure to set numbers using float() or int() as everything is read in as a string.

## experiment
This class runs your experiment. When adding in new functionality to your protocols most often you will want to edit this class. Everytime a new experiment is created a new experiment instance is created as well. This ensures everything is reset back to default. 

#### checkStatus() and checkQueues() and log_event()
Check status gets analog information from the GUI class (bar presses). Check queues looks at the multitude of queues that are running to communicate with threads. Everything that happens is logged with log_event. Make sure to log everything that is done your new tasks. Shoudldn't need any changes. 

TODO: Remove TTL here. Done in zmqClasses now

#### runSetup()
Simple things that should be done before the expt is "started". Turn fan and camera on. Wait until all this is done before time 0 is set.

#### runExpt()
Similar to loadProtocol most changes can be made by adding in a new subclass in the runExpt() function. This function goes line by line through the protocol file. We normally use a true/false paradigm to distinguish between states. These can be modified to what you need. Once a line is handled, the self.Protocol_ln_num += 1 causes the program to proceed to the next line. This allows us control over where we are in the protocol file. You could easily make a function that goes back or skips lines as well. A special case of runExpt is for conditions.

#### runConditions()
This function gets passed the condition you want to run (number 0-n). You can list as many as you want. Conditions are set at the bottom of the protocol. These are setup to look for a response from a certain location. Either touchscreen, nosepoke, lever etc. A correct or incorrect response can be made. On correct a certain reponse is given(normally food) and incorrect a different response is given(punishment). The code wants for a response and will then assess whether it is correct.

TODO: I don't love this setup and think there could be a better way to do this.

## Other important functions

#### zmqClasses()
Facilitates communcation with Open Ephys. Both send and receieve.

#### whiskerTouch()
Function running the touchscreen in our boxes. Initializes everything and that waits for events from the touchscreen (presses). Then we send this touches back to the experiment through a q. Right now we send back x,y coordinates and the name of the picture that was hit.

#### video_function
Handles our cameras and recordings. 

TODO: This is very vloated because it does a variety of freezing behavior tasks. I think the freezing thing could be outsourced (to another file/class) to make this easier to understand and work with. 

#### stimmer.pyx
Cythonized code so it will run faster and have a smaller latency. A few different routines to run our different stim paradigms. 

#### helperFunc
Has some functions that help detect behavior input.


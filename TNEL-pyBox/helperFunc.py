import daqAPI

'''
Use to check presses on Levers
Needs Interface class as inputs
'''
def detectPress(checkPressLeft,checkPressRight):
        leftPress = checkPressLeft.rcvDI()
        rightPress = checkPressRight.rcvDI()
        if rightPress[0]:
            print('right')
            return 'Right'
        elif leftPress[0]:
            print('left')
            return 'Left'
        else:
            return False

'''
Push levers out, needs task with both levers lines
'''
def leversOut(levers):
    # Set pins 0 and 1 to True
    levers.sendDByte(3)

'''
Pull levers in, needs task with both levers lines
'''
def leversIn(levers):
    # Set pins 0 and 1 to False
    levers.sendDByte(0)

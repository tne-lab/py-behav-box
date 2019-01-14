import daqAPI

'''
Use to check presses on Levers
Needs Interface class as inputs
'''

prev_leftPress = False
prev_rightPress = False
REPEAT_RP = False
REPEAT_LP = False
def detectPress(checkPressLeft,checkPressRight):
        global prev_rightPress,REPEAT_RP,prev_leftPress,REPEAT_LP
        leftPress = checkPressLeft.rcvDI()
        rightPress = checkPressRight.rcvDI()
        # RIGHT
        if prev_rightPress  and rightPress: # prev and current are BOTH True
               REPEAT_RP = True
        else: REPEAT_RP = False
        prev_rightPress = rightPress

        if rightPress and REPEAT_RP == False:
                print('Right')
                return 'Right'
        else: return False

        # LEFT
        if prev_leftPress  and leftPress: # prev and current are BOTH True
               REPEAT_LP = True
        else: REPEAT_LP = False
        prev_leftPress = leftPress

        if leftPress:
            print('left')
            return 'Left'
        else: return False

prev_foodEaten = False
REPEAT_FE = False
def checkFoodEaten(eaten):
        global prev_foodEaten, REPEAT_FE
        foodEaten = eaten.rcvDI()
        if prev_foodEaten  and foodEaten: # prev and current are BOTH True
               REPEAT_FE = True
        else: REPEAT_FE = False
        prev_foodEaten = foodEaten
        if foodEaten and REPEAT_FE == False:
                return True
        else: return False

prev_R_nose_poke = False
REPEAT_RNP = False
def checkRightNosePoke(R_nose_poke):
        global prev_R_nose_poke, REPEAT_RNP
        nose_poked_R = R_nose_poke.rcvDI()
        if prev_R_nose_poke  and nose_poked_R: # prev and current are BOTH True
               REPEAT_RNP = True
        else: REPEAT_RNP = False
        prev_R_nose_poke = nose_poked_R
        if nose_poked_R and REPEAT_RNP == False:
                return True
        else: return False

prev_L_nose_poke = False
REPEAT_LNP = False
def checkLeftNosePoke(L_nose_poke):
        global prev_L_nose_poke, REPEAT_LNP
        nose_poked_L = L_nose_poke.rcvDI()
        if prev_L_nose_poke  and nose_poked_L: # prev and current are BOTH True
               REPEAT_LNP = True
        else: REPEAT_LNP = False
        prev_L_nose_poke = nose_poked_L
        if nose_poked_L and REPEAT_LNP == False:
                return True
        else: return False
'''
Push levers out, needs task with both levers lines
'''
def leversOut(levers):
    # Set pins 0 and 1 to True
    levers.sendDByte(3)
    daqAPI.enablePulse()

'''
Pull levers in, needs task with both levers lines
'''
def leversIn(levers):
    # Set pins 0 and 1 to False
    levers.sendDByte(0)
    daqAPI.enablePulse()

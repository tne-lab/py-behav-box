import time

def food(give_food):
    give_food.sendDBit(True)
    time.sleep(.7)
    give_food.sendDBit(False)

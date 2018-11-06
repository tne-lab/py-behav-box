import time

def run(c):
    for i in range(0,5):
        print('child ', c.pop(), '\n\n')
        time.sleep(2)
    return

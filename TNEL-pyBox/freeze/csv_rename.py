import pandas as pd

csv = pd.read_csv("FR1_freezing.csv")

def splitTime(s):
    s = s.replace(".",":")
    hours, minutes, seconds, milliseconds = s.split(":")
    print(int(hours)*60*60*1000 + int(minutes)*60*1000 + int(seconds)*1000 + int(milliseconds))

for i in range(0,100):
    splitTime(csv['Time'][i])

import pandas
import ast

### !!!!!!!!! NEED TO ADD CONTITION NUMBER TO LOG FILE/ PARSER HERE !!!!! ####
# Might be way easier to read in conditions beforehand and have all condition info from that..?


### This is what you're looking for !! ##############
# My log file is in format "time, event" ("0.01, levers out")
# So split[0] is time and split[1] is the event
def parseLog():
    trials = []
    i = -1
    with open('log.txt','r') as f:
        #Iterate through file line by line
        for line in f:
            #Remove \n
            line = line.strip()
            #Split lines
            split = line.split(',')
            #Checks for start of trial
            if 'trial' in split[1]:
                i+=1
                #Create a new dictionary when we get to a new trial
                trials.append({split[1][1:] : float(split[0])})
            else:
                #if "conditioInfo", it has a lot more data attached to it so make a dictionary value for each piece
                if split[1]==' conditionInfo':
                    for j in range(2, len(split), 2):
                        trials[i][split[j][1:]] = split[j+1][1:]
                else:
                    #Get timestamp and event
                    #Has [1:] because my log file has a space in front of the word.
                    trials[i][split[1][1:]] = float(split[0])
    #returns a list of dicts that correspond to each trial
    return trials
################


## Pandas wants a dictionary with lists as the values to create csv files
# So we need to go from a list of dictionaries to a dictionary of lists. Maybe could do this all in the parser func?
# We want to save different information than a bunch of logged events though, so works for now
def parseTrials(trials):
    #columns of future csv file
    data = {'trial number': [], 'response' : [],'correct response' : [],'outcome' : [],'time_from_start' : []}
    i = 0
    for trial in trials:
        startTime = 0

        for key in trial.keys():
            #if new trial create a new entry in the trial number list and record start time of trial
            if 'trial' in key:
                data['trial number'].append(key[-1])
                startTime = trial[key]
            # If a response from rat, record it and check if it was correct or inccorect
            if key == 'lever press right' or key == 'lever press left':
                data['response'].append(key)
                data['time_from_start'].append(trial[key] - startTime)
                if key == trial['desired response']:
                    data['correct response'].append('True')
                else:
                    data['correct response'].append('False')
            # If outcome just output it.
            if key == 'food' or key == 'shock':
                data['outcome'].append(key)
        i+=1
    return data


def main():
    trials = parseLog()
    data = parseTrials(trials)
    print(trials)
    print(data)
    df = pandas.DataFrame(data,columns = data.keys())#, index = 'trial number')
    df.index.name = 'Index'
    df.to_csv('ex.csv')

main()

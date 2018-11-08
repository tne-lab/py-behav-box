import pandas
import ast

def parseLog():
    trials = []
    i = -1
    with open('log.txt','r') as f:
        for line in f:
            line = line.strip()
            split = line.split(',')
            if 'trial' in split[0]:
                i+=1
                trials.append({split[0] : float(split[1])})
            else:
                if split[0]=='conditionInfo':
                    trials[i][split[0]] = ast.literal_eval(split[1])
                else:
                    trials[i][split[0]] = float(split[1])
    return trials

def parseTrials(trials):
    data = {'trial number': [], 'response' : [],'correct response' : [],'outcome' : [],'time from start' : []}
    i = 0
    for trial in trials:
        startTime = 0

        for key in trial.keys():
            if 'trial' in key:
                data['trial number'].append(key[-1])
                startTime = trial[key]
            if key == trial['conditionInfo']['desired response']:
                data['correct response'].append('True')
            if key == 'lever-press-right' or key == 'lever-press-left':
                data['response'].append(key)
                data['time from start'].append(trial[key] - startTime)
                if len(data['correct response']) == i+1:
                    continue
                else:
                    data['correct response'].append('False')

            if key == 'food' or key == 'shock':
                data['outcome'].append(key)
        i+=1
    return data


def main():
    trials = parseLog()
    data = parseTrials(trials)

    df = pandas.DataFrame(data,columns = ['response','correct response','outcome','time from start'], index = data['trial number'])
    df.index.name = 'Trial Number'
    df.to_csv('ex.csv')

main()

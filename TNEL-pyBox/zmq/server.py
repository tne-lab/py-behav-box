import zmqClasses

def main():
    snd = zmqClasses.SNDEvent(5556, recordingDir = 'C:\\Users\\Ephys\\Desktop\\RecDir')

    for i in range(0,3):
        snd.send()

main()

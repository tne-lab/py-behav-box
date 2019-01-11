import os
from multiprocessing import Process

def main():
    p = Process(target=os.system, args=('C:/Users/Ephys/Documents/Github/OE/plugin-GUI/Builds/VisualStudio2013/x64/Release64/bin/open-ephys.exe',))
    p.start()
    p.join()

if __name__ == "__main__":
    main()

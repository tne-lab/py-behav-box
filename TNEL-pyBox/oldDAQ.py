#OUTPUTS
def sendDBit(address,TF): #TF = 'True' or 'False'
     with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(address)
        task.write(TF)
        #enablePulse()

def sendDByte(address,bits):
     with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(
            address,
            line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

        task.write(bits)

def rcvDI(address):
    with nidaqmx.Task() as task:
        task.di_channels.add_di_chan(address,
                                     line_grouping=LineGrouping.CHAN_PER_LINE)
        print('reading', task.read())
        return task.read()

### Tasks
def startTask(address):
    task = nidaqmx.Task()
    task.do_channels.add_do_chan(
            address,
            line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
    task.start()
    return task

def endTask(task):
    task.stop()

def startUpBox():
    address = dev + '/port0/line0:3'
    serviceRequest = dev +'/port9/line0:7'
    print('Setting Up')
    sendDByte(address,0)
    sendDByte(serviceRequest,1)
    enablePulse()

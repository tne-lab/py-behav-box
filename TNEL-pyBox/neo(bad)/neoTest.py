from neo import io
import numpy as np
from matplotlib import pyplot as plt

#KWIK FORMAT WHICH WE DONT DO.... :(
data = io.KwikIO(filename = 'G:\\Team Drives\\TNEL - UMN\\Closed Loop\\Recordings\\pilot_runs\\2017-08-09\\OP7-ERP_2017-08-09_10-54-50_closed_loop\\session_info.kwik')
block = data.read()
print(block[0].segments)
for seg in block[0].segments:
    print("Analyzing segment %d" % seg.index)

    avg = np.mean(seg.analogsignals[0], axis=1)

    plt.figure()
    plt.plot(avg)
    plt.title("Peak response in segment %d: %f" % (seg.index, avg.max()))

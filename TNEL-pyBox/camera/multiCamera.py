import numpy as np
from datetime import datetime
import time
def run(q):
    while True:
        if q.empty() == False:
            y = q.get()
            print('Camera process', str(time.perf_counter() -y['hello']) )

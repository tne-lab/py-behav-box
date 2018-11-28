from neo.io import OpenEphysIO
import numpy as np
from matplotlib import pyplot as plt

#KWIK FORMAT WHICH WE DONT DO.... :(
reader = OpenEphysIO(dirname='D:\\OP7_cl_test_2018-02-07_14-57-25_closed_loop')
seg = reader.read_segment()
anasig = seg.analogsignals[0]
print(anasig.name, anasig.shape, anasig.units)

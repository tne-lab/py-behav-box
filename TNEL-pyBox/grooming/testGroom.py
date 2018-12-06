from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import argparse
import imutils
import time
import cv2

cap = cv2.VideoCapture('/home/ephys/Documents/groom.avi')

from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
# https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/

class Grooming():
    def __init__(self, maxDisappeared = 50):

        self.leftCoords = (0,0)
        self.rightCoords = (0,0)
        self.listCoords = [self.leftCoords, self.rightCoords]
        self.leftDisappeared = 0
        self.rightDisappeared = 0

        self.maxDisappeared = maxDisappeared

        self.setupHands()

    def setupHands(self):
        self.leftCoords = (0,0)
        self.rightCoords = (0,0)

    def update(self, rects):
        if len(rects) = 0:
            # No hands detected..
            self.leftDisappeared += 1
            self.rightDisappeared += 1

            return

        if not init hands..:
            initHands()
        inputCentroids = np.zeroes((lens(rects), 2), dtype="int")

        for(i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        D = dist.cdist(np.array(self.listCoords), inputCentroids)

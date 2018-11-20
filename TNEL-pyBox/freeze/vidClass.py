import cv2

class Vid:
    def __init__(self, videoPath, winName):
        self.cap = cv2.VideoCapture(videoPath)
        self.startFrame = 0
        self.fps = int((1/self.cap.get(cv2.cv2.CAP_PROP_FPS))*1000)
        self.cap.set(1,self.startFrame)
        self.winName = winName
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cv2.namedWindow(self.winName)
        self.min = 0

    def trackBar(self,winName,trackName,min, max):
        cv2.createTrackbar(trackName, winName,min,max,
        lambda x: self.picFrame(x, self))

    def picFrame(x, frame, self):
        self.startFrame = frame
        self.cap.set(1,self.startFrame)

    def run(self):
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.imshow(self.winName,gray)

            self.startFrame+=1
            print(self.startFrame)
            if cv2.waitKey(self.fps) & 0xFF == ord('q'):
                break
    def close(self):
        self.cap.release()
        cv2.destroyWindow(self.winName)

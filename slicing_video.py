# Author        : Ahmed Najibe
# Python        : 3.11.0
# OS            : Windows 11 Pro 22H2
# OS Build      : 22621.963

from threading import Thread 
import cv2 as cv
import time


class readingframes :
    def __init__(self,videos_path ):
        self.videos_path = videos_path 
        
        self.vcap= cv.VideoCapture(self.videos_path)

        self.grabbed , self.frame = self.vcap.read()
        if self.grabbed is False :
            print('[Exiting] No more frames to read')
            exit(0)

        self.stopped = True
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True 

    def start(self):
        self.stopped = False
        self.t.start()

    def update(self):
        while True :
            if self.stopped is True :
                break
            self.grabbed , self.frame = self.vcap.read()
            if self.grabbed is False :
                print('[Exiting] No more frames to read')
                self.stopped = True
                break 
        self.vcap.release()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

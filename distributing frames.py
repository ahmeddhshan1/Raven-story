# Author        : Ahmed Najibe
# Python        : 3.11.0
# OS            : Windows 11 Pro 22H2
# OS Build      : 22621.963

import threading, time
import cv2 as cv
import queue
from detecting import *
from report import *
import matplotlib.pyplot as plt 

class distributing_frames(threading.Thread):
    def __init__(self, video_path , queue):
        threading.Thread.__init__(self)
        self.video_path = video_path
        self.queue = queue

    def run(self):
        vidoe_capt=cv.VideoCapture(self.video_path)
        while True:
            ret, frame = vidoe_capt.read()
            if  ret==False: break
            frame=cv.rotate(frame,cv.ROTATE_180)
            self.queue.put(frame)


class subtract_frames(threading.Thread):
    def __init__(self,queue,object_path):
        threading.Thread.__init__(self)
        self.queue = queue
        self.object_path=object_path
        self.distance = None
        self.x = None
        self.y = None

    def run(self):
        count=0
        back_sub=cv.createBackgroundSubtractorMOG2(history=90,varThreshold=90,detectShadows=False)
        location=detectings()
        reporting=report()
        x_center=[]
        y_center=[]
        hittings=[]

        time.sleep(5)
        while  True:
            time.sleep(.005)
            if self.queue.empty():break
            frame=self.queue.get()
            prepared_frame = back_sub.apply(frame)
            _,prepared_frame=cv.threshold(prepared_frame,254,255,cv.THRESH_BINARY)
            prepared_frame=cv.GaussianBlur(prepared_frame,(5,5),0)
            # print(self.queue.qsize())
            contours,_=cv.findContours(prepared_frame,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
            if len(contours) <=1 :continue
            area=cv.contourArea(max(contours,key=cv.contourArea))
            if area<=7000: continue
            x_bird,y_bird,w_bird,h_bird=location.bird_location(contours)
            x_center.append(x_bird)
            y_center.append(y_bird)

            if count % 60 == 0 :
                obj_x,obj_y,obj_w,obj_h =location.detect_objects(frame,self.object_path)

            

            hittings.append(reporting.hit_object(obj_x,obj_y,obj_w,obj_h,x_bird,y_bird,w_bird,h_bird))

            count+=1
        print(count)
        print(hittings)

        move_sumition=reporting.travel_distance(x_center,y_center)
        
        self.distance=move_sumition
        self.x=x_center
        self.y=y_center


if __name__ == '__main__':
    video_path = r"F:/raven project/project videos/T.M/CHRONIC/team 9/chronic myna 2nd blue tool making TS 9 spontaneously perform.mp4"
    object_path = r"E:\New folder"
    branch_path = r"E:\frame100.jpg"
    queue = queue.Queue(1000)
    th1=distributing_frames(video_path,queue)
    th2=subtract_frames(queue,object_path)
    th1.start()
    th2.start()
    th2.join()
    distance=th2.distance
    x=th2.x
    y=th2.y
    plt.plot(x,y)
    plt.show()
    print(distance)
    branch_detection= detectings()
    branch_detection.detect_branch(branch_path)
    




import threading, time
from threading import Timer
import cv2 as cv

import queue


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
            cv.imshow("or",cv.resize(frame,(405,720)))
            cv.waitKey(20)
            self.queue.put(frame)
            time.sleep(0.025)
        cv.destroyAllWindows()



class subtract_frames(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        count=0
        back_sub=cv.createBackgroundSubtractorMOG2(history=90,varThreshold=90,detectShadows=False)
        while  True:
            if self.queue.empty():break
            frame=queue.get()
            count+=1
            prepared_frame = back_sub.apply(frame)
            prepared_frame=cv.GaussianBlur(prepared_frame,(5,5),0)
            cv.imshow("pre",prepared_frame)
            cv.waitKey(20)
            contours,_=cv.findContours(prepared_frame,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)

        cv.destroyAllWindows()



if __name__ == '__main__':
    video_path = r"F:/raven project/project videos/T.M/CHRONIC/team 9/chronic myna 2nd blue tool making TS 9 spontaneously perform.mp4"
    queue = queue.Queue()
    th1=distributing_frames(video_path,queue)
    th2=subtract_frames(queue)
    th1.start()
    # time.sleep(5)
    th2.start()
    # t1.join()
    # time.sleep(0.025)


    # t1.join()

    # distributing_frames(video_path, queue)
    # subtract_frames(queue)








# q = queue.Queue()


# def processing():

#     while True:

#         frame=q.get()


#         time.sleep(0.025)

#         if cv2.waitKey(1) & 0xFF == ord('q'):

#             break

#     return



# cap = cv2.VideoCapture("F:/raven project/project videos/T.M/CHRONIC/team 9/chronic myna 2nd blue tool making TS 9 spontaneously perform.mp4")

# t = threading.Thread(target=processing)

# t.start()


# count=0

# while True:
#     ret, frame = cap.read()
#     if ret == False:
#         break
#     count+=1

#     q.put(frame)

#     time.sleep(0.025)

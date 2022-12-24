# Author        : Ahmed Najibe
# Python        : 3.11.0
# OS            : Windows 11 Pro 22H2
# OS Build      : 22621.963

import cv2 as cv
import os 
import numpy as np

class detectings:
    @staticmethod

    # def __init__(self,frame,object_path , branch_pass):
    #     '''
    #         Constructor
    #         self.video_path = video_path
    #         self.object_path = object_path
    #         self.branch_pass = branch_pass
    #     '''
    #     self.frame = frame
    #     self.object_path = object_path
    #     self.branch = branch_pass

    def detect_objects(frame,object_path):
        '''
            :param frame: the path to the folder
            :param tem_path: the path to the objects
            :return: four lists of x axis , y axis ,width , height of the object center
        '''
        gray_img=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

        objects=[]
        maxes=[]

        for i in os.listdir(object_path):
            pl=cv.imread(object_path+'\\'+i,0)
            objects.append(pl)
            # print(i)

        for j in range(len(objects)):
            wid,hig=objects[j].shape[::-1]
            result=cv.matchTemplate(gray_img,objects[j],cv.TM_CCOEFF_NORMED)
            Max=np.amax(result)
            maxes.append(Max)

            threshold=maxes[-1]
            loc=np.where(result>=threshold)

            for pt in zip(*loc[::-1]):
                x_center=pt[0]+wid/2
                w_center=pt[1]+hig/2

        return x_center,w_center,wid/2,hig/2
    
    def detect_branch(branch):
        '''
            :param tem: is the path of the woden branch for this vedio
            :return: the width and height
        '''
        tem=cv.imread(branch,0)
        wid,hig=tem.shape[::-1]
        return wid,hig
# Author        : Ahmed Najibe
# Python        : 3.11.0
# OS            : Windows 11 Pro 22H2
# OS Build      : 22621.963

import cv2 as cv
import os 
import numpy as np

class detectings:
    # @staticmethod

    def __init__(self):
        pass
    
    def detect_objects(self,frame,object_path):
        '''
            :param frame: the path to the folder
            :param tem_path: the path to the objects
            :return: four lists of x axis , y axis ,width , height of the object center
        '''
        gray_img=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

        objects=[]
        maxes=[]
        centers_x=[]
        centers_y=[]
        object_w=[]
        object_h=[]

        for i in os.listdir(object_path):
            pl=cv.imread(object_path+'\\'+i,0)
            objects.append(pl)
            # print(i)

        for j in range(len(objects)):
            wid,hig=objects[j].shape[::-1]
            result=cv.matchTemplate(gray_img,objects[j],cv.TM_CCOEFF_NORMED)
            Max=np.amax(result)
            x=False
            for i in maxes:
                if Max==i:
                    x=True
                    break
                
            if x:continue

            # if Max==maxes[-1]:continue
            maxes.append(Max)
            threshold=maxes[-1]
            loc=np.where(result==threshold)

            for pt in zip(*loc[::-1]):
                x_center=pt[0]+wid/2
                y_center=pt[1]+hig/2
                centers_x.append(x_center)
                centers_y.append(y_center)
                object_w.append(wid/2)
                object_h.append(hig/2)

                

        return centers_x,centers_y,object_w,object_h
    
    def detect_branch(self,branch):
        '''
            :param tem: is the path of the woden branch for this vedio
            :return: the width and height
        '''
        tem=cv.imread(branch,0)
        wid,hig=tem.shape[::-1]
        return wid,hig

    def bird_location(self,contours):
        '''
            :param contours: the contours of the bird
            :return: the center of the bird
        '''

        for con in contours:
                area= cv.contourArea(con)
                if area < 7000 :
                    continue
                max_contour=max(contours,key=cv.contourArea)
                x,y,w,h=cv.boundingRect(max_contour)
                new_x=x+(w/2)
                new_y=y+(h/2)  

        return new_x,new_y,w/2,h/2

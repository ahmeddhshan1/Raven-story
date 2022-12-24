# Author        : Ahmed Najibe
# Python        : 3.11.0
# OS            : Windows 11 Pro 22H2
# OS Build      : 22621.963
import cv2 as cv
import math
import matplotlib.pyplot as plt 

class report:
    @staticmethod
    def travel_distance(frame,contours):
        '''
        :param contours: the detected movements in the video.
        this function return the total distance that the bird walked
        :return sum_distance: the total distance walked by bird
        '''
        detect_x=[]
        detect_y=[]
        distance=[]

        for con in contours:
            area= cv.contourArea(con)
            if area < 1000 :
                continue
            if len(contours) !=0:
                max_con = max(contours, key = cv.contourArea)
                x,y,w,h = cv.boundingRect(max_con)
                cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,100),3)
                new_x=x+(w/2)
                new_y=y+(h/2)
                detect_x.append(new_x)
                detect_y.append(new_y)

        for i in range(len(detect_x)):
            if i==0:
                continue
            distance.append(math.sqrt(pow((detect_x[i]-detect_x[i-1]),2)+pow((detect_y[i]-detect_y[i-1]),2)))
        
        sum_distance=sum(distance)

        return detect_x,detect_y,sum_distance

    
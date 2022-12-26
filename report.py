# Author        : Ahmed Najibe
# Python        : 3.11.0
# OS            : Windows 11 Pro 22H2
# OS Build      : 22621.963

import cv2 as cv
import math


class report:
    # @staticmethod
    def __init__(self):
        pass

    def travel_distance(self,x_center, y_center):
        '''
        :param contours: the detected movements in the video.
        this function return the total distance that the bird walked
        :return sum_distance: the total distance walked by bird
        '''
        distance=[]

        for i in range(len(y_center)):
            if i==0:
                continue
            distance.append(math.sqrt(pow((x_center[i]-x_center[i-1]),2)+pow((y_center[i]-y_center[i-1]),2)))
        
        sum_distance=sum(distance)

        return sum_distance

    

    def hit_object(self,x_object, y_object,object_w,object_h,x_bird, y_bird,bird_w,bird_h):
        '''
            :param x_object: list of objects x_axis
            :param y_object: list of objects y_axis
            :param x_bird: list of bird x_axis
            :param y_bird: list of bird y_axis
            :param object_w: list of object width
            :param object_h: list of object height
            :param bird_w: bird width
            :param bird_h: bird height
            :return: bool list of hittings object
        '''
        hit=[]
        d=[]
        for i in range(len(x_object)):
            d.append(math.sqrt(pow((x_object[i]-x_bird),2)+pow((y_object[i]-y_bird),2)))

        h= math.sqrt(pow(bird_w,2)+pow(bird_h,2))
            
        for i in range(len(d)):
            for j in range(len(object_w)):
                if y_object[j]+object_h[j] <= y_bird :
                    if d[i]<=object_h[j]+h:
                        hit.append(True)
                    else:
                        hit.append(False)
                # elif y_object[i]-object_h[i] > y_bird:
                #     if d[i]<object_h+bird_h:
                #         hit.append(True)
                #     else:
                #         hit.append(False)
                else:
                        if d[i]<=object_w[j]+h:
                            hit.append(True)
                        else:
                            hit.append(False)
        return hit
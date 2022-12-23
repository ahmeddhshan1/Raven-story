# Author        : Ahmed Najibe
# Python        : 3.11.0
# OS            : Windows 11 Pro 22H2
# OS Build      : 22621.963

import cv2 as cv
import math
import os 
import numpy as np
import matplotlib.pyplot as plt 


class Birdie():

    def __init__(self,video_path,object_path , branch_pass):
        '''
            Constructor
            self.video_path = video_path
            self.object_path = object_path
            self.branch_pass = branch_pass
        '''
        self.video_path = video_path
        self.object_path = object_path
        self.branch = branch_pass
    
    def start(self):
        print(self.detect_branch())
        video_capture=cv.VideoCapture(self.video_path)
        back_sub=cv.createBackgroundSubtractorMOG2(history=90,varThreshold=90,detectShadows=False)
        h=0
        frame_count=0
        detect_x=[]
        detect_y=[]
        hit_object=[]
        while True:
            succeeded,frame=video_capture.read()
            x=True    
            if(succeeded==False): break
            frame_count+=1
            
            # frame=cv.rotate(frame,cv.ROTATE_180)
            
            prepared_frame=back_sub.apply(frame)
            
            prepared_frame=cv.GaussianBlur(prepared_frame,(5,5),0)
            
            contours,_=cv.findContours(prepared_frame,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
            # print(contours)
            # cv.imshow("1",cv.resize(frame,(405,720)))
            # cv.waitKey(30)

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
                else:
                    x=True
            if x: continue
            # print("hhhhhh")
            obj_x,obj_y,w_object,h_object=self.detect_objects(frame,self.object_path)
            hitting=self.hit_object(obj_x,obj_y,new_x,new_y,w_object,h_object,w/2,h/2)
            hit_object.append(hitting)
            print(frame_count)
            
        travel_distance=self.travel_distance(detect_x,detect_y)
        print(travel_distance)


    def hit_object(self,x_object, y_object,x_bird, y_bird,object_w,object_h,bird_w,bird_h):
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
        for i in range(len(d)):
            if y_object[i]+object_h[i] <= y_bird :
                if d[i]<object_h+bird_h:
                    hit.append(True)
                else:
                    hit.append(False)
            # elif y_object[i]-object_h[i] > y_bird:
            #     if d[i]<object_h+bird_h:
            #         hit.append(True)
            #     else:
            #         hit.append(False)
            else:
                    if d[i]<object_w+bird_w:
                        hit.append(True)
                    else:
                        hit.append(False)
        return hit

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
                w_centers=pt[0]+wid/2
                h_centers=pt[1]+hig/2
                centers_x.append(w_centers)
                centers_y.append(h_centers)

        return centers_x,centers_y,wid/2,hig/2

    def detect_branch(self):
        '''
            :param tem: is the path of the woden branch for this vedio
            :return: the width and height
        '''
        tem=cv.imread(self.branch,0)
        wid,hig=tem.shape[::-1]
        return wid,hig
    
    def travel_distance(self,x_axis,y_axis):
        '''
        :param x_axis: the X axis points of the wanted pixels.
        :param y_axis: the Y axis points of the wanted pixels.
        this function return the total distance that the bird walked
        :return sum_distance: the total distance walked by bird
        '''
        distance=[]
        for i in range(len(x_axis)):
            if i==0:
                continue
            distance.append(math.sqrt(pow((x_axis[i]-x_axis[i-1]),2)+pow((y_axis[i]-y_axis[i-1]),2)))
        
        sum_distance=sum(distance)
        plt.plot(x_axis,y_axis)
        plt.show()
        return sum_distance
    


if __name__ == '__main__':
    # video_path =input("Enter your video path\n")
    # video_path=video_path.replace("\\", "/")
    # folder_path =input("Enter your folder path\n")
    # folder_path=folder_path.replace("\\", "/")
    # branch_path =input("Enter your branch path\n")
    # branch_path=branch_path.replace("\\", "/")
    video_path = r"C:\Users\ahmed\Videos\Acute Myna Ceo Water Displacement.m4v"
    object_path = r"E:\New folder"
    branch_path = r"E:\frame100.jpg"
    obj=Birdie(video_path,object_path,branch_path)
    obj.start()


r'''
    "E:\frame100.jpg"
    "E:\New folder"
    "F:\raven project\project videos\T.M\ACUTE\tool making Ceo acute myna .MOV"
'''
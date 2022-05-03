#!/usr/bin/env python3 

import cv2
import numpy as np
import time

import rospy 

import submodules.topics as topics
from submodules.Depth_functions import *
from submodules.two_dimensions_function import *


objet=0
nbr_classes=180
seuil=20
move = 1
iteration = 10
term_criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, iteration, move)
mode=0
frame_size = [1280,480]

line_thickness = 2 
line_color = (0,255,0)
fontScale = 1.5
color = (255, 0, 0)
thickness = 1


polynome = get_polynome_depth('left',3)

# Place to put the tomato
x1,y1,z1 = 0.06058, 0.3063, 0.1321

# Initial position
x2,y2,z2 = -0.1452, 0.05863, 0.45

rospy.init_node('RosCameraNode', anonymous=True)

tomato_pixels = topics.Tomato_pixels()
tomato_pixels.change_value(0,0,0)
tomato_pixels.publish_topic()
etat = topics.Etat()
hand = topics.Hand()
point_robot = topics.Position_Robot() 
depth = topics.Depth()



def roi_function ():
    global roi_x,roi_y,roi_h,roi_w,roi_hist,frame_left,objet,roi,red_roi

    roi_x, roi_y, roi_w, roi_h = cv2.selectROI("ROI", frame_left, fromCenter=False,showCrosshair=False)
    roi=frame_left[roi_y: roi_y + roi_h, roi_x: roi_x + roi_w]
    roi_x -=10
    roi_y -=10
    roi_w +=20
    roi_h +=20
    hsv_roi=cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    roi_hist=cv2.calcHist([hsv_roi], [0], None, [nbr_classes], [0, nbr_classes])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    cv2.destroyWindow('ROI')
    objet = 1

Camera=cv2.VideoCapture(2)
Camera.set(3, frame_size[0])
Camera.set(4, frame_size[1])
cv2.namedWindow('Camera')

while True:
    ret, frame=Camera.read()
    
    frame_left = frame[:,:int(frame_size[0]/2)]
    # frame_right = fraqe[:,int(frame_size[0]/2):frame_size[0]]


    if objet:

        hsv=cv2.cvtColor(frame_left, cv2.COLOR_BGR2HSV)
        mask=cv2.calcBackProject([hsv], [0], roi_hist, [0, nbr_classes], 1)
        _, mask=cv2.threshold(mask, seuil, 255, cv2.THRESH_BINARY)
        mask=cv2.erode(mask, None, iterations=3)
        mask=cv2.dilate(mask, None, iterations=3)
        

        _, rect=cv2.meanShift(mask, (roi_x, roi_y, roi_w, roi_h), term_criteria)
        roi_x, roi_y, w, h=rect
        x,y = roi_x+w/2,roi_y+h/2
        tomato_pixels.change_value(x,y,0.0)
        tomato_pixels.publish_topic()

        if np.sum(mask[roi_y:roi_y+roi_h,roi_x:roi_x+roi_w]) == 0:
            objet = 0
            tomato_pixels.change_value(0,0,0)
            tomato_pixels.publish_topic()
    
        cv2.rectangle(frame_left, (roi_x, roi_y), (roi_x + w, roi_y + h), (255, 255, 255), 2)
        cv2.imshow("Mask", mask)
        cv2.putText(frame_left, "mode : {}  mode[o]:{}".format(etat.etat.data, "CamShift" if mode else "meanshift",), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
    
    if etat.etat.data == 3:
        point_robot.change_value(x1,y1,z1)
        point_robot.publish_topic()
        time.sleep(2)
        hand.open()
        time.sleep(1)
        etat.etat.data = 6
        etat.publish_topic()
        
    elif etat.etat.data== 6 :
        point_robot.change_value(x2,y2,z2)
        point_robot.publish_topic()

    elif etat.etat.data == 2:
        hand.close()
        etat.change_etat(6)
    
    elif etat.etat.data == 4:
        z = compute_distance(roi_x,roi_y,roi_x+w,roi_y+h,polynome)
        cv2.line(frame_left, (roi_x, roi_y), (roi_x+w, roi_y+h), line_color, thickness=line_thickness)
        cv2.putText(frame_left, f'{int(z)} cm', (roi_x+5, roi_y-10), 1, 
                    fontScale, color, thickness, cv2.LINE_AA)
        depth.change_etat(z/100)
        depth.publish_topic()
    
    elif etat.etat.data == 0:
        pass

    cv2.imshow("Camera", frame_left)

    key=cv2.waitKey(10)&0xFF
   
   #arret
    if key & 0XFF == ord('q'):  #If stnnatement to stop loop,Letter 'q' is the escape key
        etat.change_etat(5)
        etat.publish_topic()
        break                     #get out of loop   

    #deplacement
    if key & 0xFF == ord('d'):
        etat.change_etat(1)
        etat.publish_topic()

    # attraper
    elif key & 0xFF == ord('a'):
        etat.change_etat(2)
        etat.publish_topic()

    #poser 
    elif key & 0xFF == ord('p'):
        etat.change_etat(3)
        etat.publish_topic()
    
    #zero
    elif key & 0xFF == ord('z'):
        etat.change_etat(6)
        etat.publish_topic()   

    # depth
    elif key & 0xFF == ord('n'):
        roi_function()
        etat.change_etat(4)
        etat.publish_topic()   
    
    elif key == ord('s'):
        roi_function()
    
Camera.release()
cv2.destroyAllWindows()

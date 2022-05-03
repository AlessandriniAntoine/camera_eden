#!/usr/bin/env python3 
# license removed for brevity

import cv2
import rospy 
from topics import *

frame_size = [1280,480]
camera_id = 2

etat = Etat()
hand = Hand()
hand_string = "open"
etat_string = "neutral"
n= 0

rospy.init_node('camera', anonymous=True)

Camera=cv2.VideoCapture(camera_id)
Camera.set(3, frame_size[0])
Camera.set(4, frame_size[1])
cv2.namedWindow('Camera')

while True:
    ret, frame=Camera.read()
    
    cv2.putText(frame, "state: {} hand: {} ".format(etat_string,hand_string), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)
    cv2.rectangle(frame, (420, 380), (460 , 420), (255, 255, 255), 2)
    cv2.rectangle(frame, (860, 380), (900 , 420), (255, 255, 255), 2)

    cv2.imshow("Camera", frame)

    key=cv2.waitKey(10)&0xFF
   
   #arret
    if key & 0XFF == ord('q'):  #If stnnatement to stop loop,Letter 'q' is the escape key
        break

    if etat.etat.data == 1 :
        etat_string = "moving"
    
    if etat.etat.data == 3 :
        etat_string = "drop"
    
    if etat.etat.data == 5 :
        etat_string ="zero"
    
    if etat.etat.data == 0:
        etat_string = "neutral"
    
    if hand.state.data :
        n+=1
        hand_string = "open"
    
    if not hand.state.data and n>1:
        hand_string = "close"
    
Camera.release()
cv2.destroyAllWindows()
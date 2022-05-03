#!/usr/bin/env python3

import rospy
import sys
from geometry_msgs.msg import Point
from std_msgs.msg import Int16, Bool,Float32

class Tomato_pixels:

    def __init__(self):
        self.pub = rospy.Publisher("Tomato/state",Point, queue_size = 10)
        self.angles = Point()
        self.angles.x = 0
        self.angles.y = 0
        self.angles.z = 0

    def change_value(self,x,y,z):       
        self.angles.x = x
        self.angles.y = y
        self.angles.z = z

    def publish_topic(self):
        self.pub.publish(self.angles)

class Etat:

    def __init__(self):
        self.pub = rospy.Publisher("etat",Int16, queue_size = 10)
        self.etat = Int16()
        self.etat.data = 0
        self.publish_topic()


    def change_etat(self,etat):
        self.etat.data = etat       
    
    def publish_topic(self):
        self.pub.publish(self.etat.data)

# 0 : neutre
# 1 : deplacement 
# 2 : attraper
# 3 : poser 
# 4 : z
# 5 : arret
# 6 : position zero

class Hand:

    def __init__(self):
        self.pub = rospy.Publisher("Hand/state",Bool, queue_size = 10)
        self.etat = Bool()
        self.etat.data = 0


    def open(self):
        self.etat.data = 1
        self.publish_topic()

    def close(self):
        self.etat.data = 0   
        self.publish_topic()  
    
    def publish_topic(self):
        self.pub.publish(self.etat)


class Position_Robot:
    
    def __init__(self):
        self.pub = rospy.Publisher("Robot/state",Point, queue_size = 10)
        self.position = Point()

    def change_value(self,x,y,z):       
        self.position.x = x
        self.position.y = y
        self.position.z = z
    
    def publish_topic(self):
        self.pub.publish(self.position)

class Depth:

    def __init__(self):
        self.pub = rospy.Publisher("Depth/state",Float32, queue_size = 10)
        self.depth = Float32()
        self.depth.data = 0
        self.publish_topic()


    def change_etat(self,etat):
        self.depth.data = etat       
    
    def publish_topic(self):
        self.pub.publish(self.depth.data)
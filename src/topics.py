#!/usr/bin/env python3

import numpy as np
import rospy
import sys
from geometry_msgs.msg import Quaternion, Point
from std_msgs.msg import String, Bool


class angles_joint:

    def __init__(self,x,y,z,w):
        self.sub = rospy.Subscriber("Angles/ref",Quaternion,self.callback)
        self.angles = Quaternion()
        self.angles.x = x
        self.angles.y = y
        self.angles.z = z
        self.angles.w = w

    def callback(self,data):       
        self.angles = data

class angles_reference:

    def __init__(self,x,y,z,w):
        self.pub = rospy.Publisher("AnglesRef/state",Quaternion, queue_size = 10)
        self.angles = Quaternion()
        self.angles.x = x
        self.angles.y = y
        self.angles.z = z
        self.angles.w = w

    def change_value(self,x,y,z,w):       
        self.angles.x = x
        self.angles.y = y
        self.angles.z = z
        self.angles.w = w

    def publish_topic(self):
        self.pub.publish(self.angles)

class Position_Camera:
    
    def __init__(self):
        self.pub = rospy.Publisher("Camera/state",Point, queue_size = 10)
        self.position = Point()

    def change_value(self,x,y,z):       
        self.position.x = x
        self.position.y = y
        self.position.z = z
    
    def publish_topic(self):
        self.pub.publish(self.position)

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


class Etat:

    def __init__(self):
        self.pub = rospy.Publisher("etat",String, queue_size = 10)
        self.etat = String()
        self.etat.data = "deplacement"


    def change_etat(self,etat):
        self.etat.data = etat       
    
    def publish_topic(self):
        self.pub.publish(self.etat.data)

class Hand:

    def __init__(self):
        self.pub = rospy.Publisher("Hand/state",Bool, queue_size = 10)
        self.state = Bool()
        self.state.data = 0


    def open(self):
        self.state.data = 1
        self.publish_topic()

    def close(self):
        self.state.data = 0   
        self.publish_topic()  
    
    def publish_topic(self):
        self.pub.publish(self.state)
import numpy as np
import math

def compute_distance(x1,y1,x2,y2,polynome):
    # Calcul distance in cm
    distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
    distanceCM = polynome(distance)
    return distanceCM

def difference(frame,x1,y1,x2,y2):
    [x_center_object, y_center_object] = [(x1+x2)/2,(y1+y2)/2]
    [x_center_image,y_center_image] = (frame.shape[1]/2,frame.shape[0]/2)
    difference = [x_center_object-x_center_image,y_center_object-y_center_image]
    return difference

def position_2D(z,difference,image,polynome_x,polynome_y):
    if image == 'right':
        x  = difference[0]/polynome_x(z)
        y = difference[1]/polynome_y(z)
    elif image == 'left':
        x  = difference[0]/polynome_x(z)
        y = difference[1]/polynome_y(z)
    return (x,y)

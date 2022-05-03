import numpy as np
import csv
import os

################ Data for distance ################

def get_polynome_depth(image,degres):

    # Left Camera
    coefficiant = []
    dir_path = os.path.dirname(os.path.realpath(__file__))    
    print(dir_path)
    filename = dir_path+'/Data_base/depth.csv'
    with open( filename, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            coefficiant.append(row)

    coefficiant=[list(map(float, x)) for x in coefficiant]
    coefficiant = np.array(coefficiant)

    distance = coefficiant[:,0]
    pixel = coefficiant[:,1]

    coff = np.polyfit(pixel, distance, degres)  # y = Ax^2 + Bx + C
    polynome = np.poly1d(coff)

    return polynome
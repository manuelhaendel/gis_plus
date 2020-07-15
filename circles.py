# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:31:05 2020

@author: Brigitte Häuser, Guilherme Arruda, Manuel Händel
"""

import numpy as np
import math
from neighborhoods import *

def get_angle(row_processing, col_processing, row, col):
    
    x = col - col_processing  
    y = row_processing - row
    dist = math.sqrt(abs(row_processing - row)**2 +
                                              abs(col_processing - col)**2)
    
    # same cell
    if x == 0 and y == 0:
        return 0
    
    # quadrant upper right
    if x > 0 and y >= 0:
        return math.degrees(math.asin(y / dist))
    
    # quadrant upper left
    if x <= 0 and y > 0:
        return 180 - math.degrees(math.asin(y / dist))
    
    # quadrant bottom left
    if x < 0 and y <= 0:
        return 180 - math.degrees(math.asin(y / dist))
    
    # quadrant bottom right
    if x >= 0 and y < 0:
        return 360 + math.degrees(math.asin(y / dist))



def get_values(data, neighborhood, row_processing, col_processing):
    """
    Selects cells for the neighborhood window.

    Parameters
    ----------
    position : array
        Two dimensional array, giving the x- and y-position of the processing 
        cell.
    shape : string
        Defines the neighborhood type.
    

    Returns
    -------
    None.

    """
    
    if isinstance(neighborhood, rectangle):
        x = col_processing - math.floor((neighborhood.width -1)/2)
        y = row_processing - math.floor((neighborhood.height -1)/2)
        values = data[y:y+neighborhood.height, x:x+neighborhood.width]
    
    if isinstance(neighborhood, circle):
        
        distance = np.copy(data)
        
        for col in range(np.size(data, 1)): # columns
            for row in range(np.size(data, 0)):  # rows
            
                distance[row,col] = math.sqrt(abs(row_processing - row)**2 + 
                                              abs(col_processing - col)**2)
        
        window = np.where(distance <= neighborhood.radius)
        values = data[window]
    
    if isinstance(neighborhood, wedge):
        
        distance = np.copy(data)
        angle = np.copy(data)
        
        for col in range(np.size(data, 1)): # columns
            for row in range(np.size(data, 0)):  # rows
            
                distance[row,col] = math.sqrt(abs(row_processing - row)**2 +
                                              abs(col_processing - col)**2)
                
                angle[row,col] = round(get_angle(row_processing, col_processing, row, col), 2)
        
        # return angle
        window = np.where((distance <= neighborhood.radius) & 
                          (angle >= neighborhood.start) &
                          (angle <= neighborhood.end))
        
        """
        The angle of the processing cell is always set to 0°. But when the 
        start and end angle don't encompass 0°, the processing cell would not
        be included in the window. Therefore it has to be appended manually.
        """
        window = (np.append(window[0], row_processing),
                  np.append(window[1], col_processing)) 
        
        values = data[window]
    
    return values


"""
a = np.array([[1, 2], [3, 4]])
np.pad(a.astype(float), 2, constant_values = None)

       
# round(get_angle((4,4), 5, 7), 2)
  

test = np.arange(60).reshape(6,10)
print(test)
window = create_window(test, (3,4), "wedge", start_angle = 0, end_angle = 90)
#print(window)
test[window] = 0
print(test)

print(max(test[dist]))
test[dist] = 0
print(test)
"""
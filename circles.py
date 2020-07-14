# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:31:05 2020

@author: Manuel
"""

import numpy as np
import math

def get_angle(position, row, col):
    
    x = col - position[1]  
    y = position[0] - row
    dist = math.sqrt(abs(position[0] - row)**2 +
                                              abs(position[1] - col)**2)
    
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



def create_window(data, position, shape, radius = 3, start_angle = 0, end_angle = 90):
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
    
    if shape not in ('square', 'circle', 'retangle', 'wedge'):
        raise ValueError('Not a implemented shape.')
    
    distance = data.astype(float)
    angle = data.astype(float)
    
    if shape == 'circle':
        
        for col in range(np.size(data, 1)): # columns
            for row in range(np.size(data, 0)):  # rows
            
                distance[row,col] = math.sqrt(abs(position[0] - row)**2 + 
                                              abs(position[1] - col)**2)
        
        window = np.where(distance <= radius)
    
    if shape == 'wedge':
        
        for col in range(np.size(data, 1)): # columns
            for row in range(np.size(data, 0)):  # rows
            
                distance[row,col] = math.sqrt(abs(position[0] - row)**2 +
                                              abs(position[1] - col)**2)
                
                angle[row,col] = round(get_angle(position, row, col), 2)
        
        # return angle
        window = np.where((distance <= radius) & 
                          (angle >= start_angle) &
                          (angle <= end_angle))
        
        """
        The angle of the processing cell is always set to 0°. But when the 
        start and end angle don't encompass 0°, the processing cell would not
        be included in the window. Therefore it has to be appended manually.
        """
        window = (np.append(window[0], position[0]),
                  np.append(window[1], position[1])) 
    
    return window




a = np.array([[1, 2], [3, 4]])
np.pad(a.astype(float), 2, constant_values = None)

       
# round(get_angle((4,4), 5, 7), 2)
  

test = np.arange(60).reshape(6,10)
print(test)
window = create_window(test, (3,4), "wedge", start_angle = 30, end_angle = 190)
#print(window)
test[window] = 0
print(test)
"""
print(max(test[dist]))
test[dist] = 0
print(test)
"""
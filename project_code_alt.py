# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 21:38:26 2020

@author: Brigitte Häuser, Guilherme Arruda, Manuel Händel
"""


import numpy as np
import math
from neighborhoods import *

# main function
def focal_statistics(in_data,
                     neighborhood = rectangle(3,3),
                     statistic    = "mean",
                     NoData       = True):
    
    if not isinstance(neighborhood, (rectangle, circle, wedge)):
        raise ValueError('Neighborhood class not implemented.')
    
    if statistic not in ('min', 'max', 'mean', 'dev', 'var'):
        raise ValueError('Statistic not implemented.')
    
    # add padding to the input array
    if isinstance(neighborhood, rectangle):
        p = max(neighborhood.width, neighborhood.height)
        
    if isinstance(neighborhood, (circle, wedge)):
        p = neighborhood.radius
    
    in_data = np.pad(in_data.astype(float), p, constant_values = None)
    out_data = np.copy(in_data)
    
    # determine indices of rows and columns of the input array inside the
    # padded array
    nrows = np.size(in_data, 0)
    index_rows = range(0,nrows)[p:-p]
    ncols = np.size(in_data, 1)
    index_cols = range(0,ncols)[p:-p]
    
    # loop through cells
    for row in index_rows:
        for col in index_cols:
            
            values = get_values(in_data, neighborhood, row, col)
            """if row == 5 and col == 5:
                return(values)"""
        #values = in_data[window]
            if NoData:
                values = values[(np.isnan(values) == False)]
                out_data[row, col] = function[statistic](values)
            elif np.isnan(values).any():
                out_data[row, col] = None
            else:
                out_data[row, col] = function[statistic](values)
    
    return(out_data[p:-p, p:-p])


# helper functions
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

# dictionary with summary statistics
function = {
    "min": np.min,
    "max": np.max,
    "mean": np.mean}
    


######## code to test the functions
file = np.arange(60).reshape(10, 6) 
print(file)

out = focal_statistics(file, rectangle(4,3), 'max', False)
print('rectang buffer border \n', out)
out = focal_statistics(file, rectangle(4,3), 'max', True)
print('rcetang default border \n', out)
  

out = focal_statistics(file, circle(3), "max")
print('circle default border \n', out)

import matplotlib.pyplot as plt

plt.imshow(out)
plt.show()
"""
print(out)
#print(vals)
print(win)
#print(row, col)
"""
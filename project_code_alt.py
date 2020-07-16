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
        out_data = rectangfun(in_data, neighborhood.height,
                              neighborhood.width, NoData)
        
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
        
        out_data = out_data[p:-p, p:-p]
    
    return(out_data)


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


# helper function for rectangles
def rectangfun(data, height, width, NoData):
    data = np.array(data)
    
    if height%2 == 0: # even height
        
        if width%2 == 0: # and even width
            
            top_wsize = int((height-2)/2)
            bot_wsize = int((height)/2)
            left_wsize = int((width-2)/2)
            right_wsize = int((width)/2)
            
            newdata = bordercases(data, wsize_top = top_wsize, wsize_left = left_wsize, 
                              wsize_bot = bot_wsize, wsize_right = right_wsize, NoData = NoData)
        
        else: # and odd width
            
            top_wsize = int((height-2)/2)
            bot_wsize = int((height)/2)
            width_wsize = int((width-1)/2)
           
            newdata = bordercases(data, wsize_top = top_wsize, wsize_left = width_wsize, 
                              wsize_bot = bot_wsize, wsize_right = width_wsize, NoData = NoData)
        
    else: # odd height
        
        if width%2 == 0: # and even width
            
            height_wsize = int((height-1)/2)
            left_wsize = int((width-2)/2)
            right_wsize = int((width)/2)
            
            newdata = bordercases(data, wsize_top = height_wsize, wsize_left = left_wsize, 
                              wsize_bot = height_wsize, wsize_right = right_wsize, NoData = NoData)
            
            
        else: # and odd width
            height_wsize = int((height-1)/2)
            width_wsize = int((width-1)/2)
            
            newdata = bordercases(data, wsize_top = height_wsize, wsize_left = width_wsize, 
                              wsize_bot = height_wsize, wsize_right = width_wsize, NoData = NoData)
    
    return newdata


# border cases for rectangles
def bordercases(data, wsize_top, wsize_left, wsize_bot, wsize_right, NoData): 
    
    # filling newdata array with zeros
    newdata = np.zeros(data.shape)
    
    if NoData:
    
        for col in range(np.size(data, 1)): # rows
                for row in range(np.size(data, 0)):  # columns
    
    
    
                    ### border cases ###
    
                    # all corners:
                    if col < wsize_left and row < wsize_top: # topleft
                        window = data[:row+wsize_bot+1, :col+wsize_right+1]
                        #print('bot in topleft case \n', bot)
    
                    elif col < wsize_left and row >= np.size(data, 0)-wsize_bot: # botleft
                        window = data[row-wsize_top:, :col+wsize_right+1]
                        #print('top in botleft case \n', top)
    
    
                    elif col >= np.size(data, 1)-wsize_right and row < wsize_top: # topright
                        window = data[:row+wsize_bot+1, col-wsize_left:]
                        #print('bot in the topright case \n', bot)
    
                    elif col >= np.size(data, 1)-wsize_right and row >= np.size(data, 0)-wsize_bot: # botright
                        window = data[row-wsize_top:, col-wsize_left:]
                        #print('top in the botright case \n', top)
    
    
                    # all borders:
                    elif col < wsize_left: # left border
                        window = data[row-wsize_top:row+wsize_bot+1, :col+(wsize_right)+1]
                        #print('left border case: \n', middle)
    
                    elif row >= np.size(data, 0)-wsize_bot: # bot border
                        window = data[row-wsize_top:, col-wsize_left:col+wsize_right+1]
                        #print('bot border case \n', middle)
    
                    elif col >= np.size(data, 1)-wsize_right: # right border
                        window = data[row-wsize_top:row+wsize_bot+1, col-wsize_left:]
                        #print('right border case \n', middle)
    
                    elif row < wsize_top: # top border
                         window = data[:row+wsize_bot+1, col-wsize_left:col+wsize_right+1]
                        #print('top border case \n', middle)
    
    
    
                    else: # normal case
                        window = data[row-wsize_top:row+wsize_bot+1, col-wsize_left:col+wsize_right+1]
                        #print('normal case \n', middle)
    
    
                    # finding the maximum
                    newdata[row, col] = np.max(window)
                    #print(newdata)    
                    
    else:
        
        for col in range(np.size(data, 1)): # rows
            for row in range(np.size(data, 0)):        
        
                if  row < np.size(data, 0)-wsize_bot and row >= wsize_top and col < np.size(data, 1)-wsize_right and col >= wsize_left: # normal case
                    window = data[row-wsize_top:row+wsize_bot+1, col-wsize_left:col+wsize_right+1]
                    
                    newdata[row, col] = np.max(window)
                    
                else: # buffer zone
                    newdata[row, col] = None
            
    
    return newdata

# dictionary with summary statistics
function = {
    "min": np.min,
    "max": np.max,
    "mean": np.mean
    "variance": np.var,
    "standard deviation": np.std}
    


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
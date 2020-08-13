# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 21:38:26 2020

@author: Brigitte Häuser, Guilherme Arruda, Manuel Händel

Function definitions for the focal statistics project. The main function
'focal_statistics()' calls the helper functions: 'get_values()',
'get_angle()', 'get_newdata()' and 'rectangfun()'. The dictionary
'function' stores the different statistics that can be applied to the
cell values.
"""

import math
import numpy as np

from classes import Rectangle, Circle, Wedge

# main function
def focal_statistics(in_data,
                     neighborhood  = Rectangle(3, 3),
                     statistic     = "mean",
                     ignore_nodata = True
                     ):
    """

    Parameters

    ----------
    in_data : numpy array
        The array to perform the focal statistics calculations on.
    neighborhood : neighborhood class, optional
        The Neighborhood class dictates the shape of the area around
        each cell used to calculate the statistic.
        
        The different types of neighborhood available are Rectangle,
        Circle and Wedge. The default is Rectangle(3,3).
    statistic : string, optional
        The statistic type to be calculated.
        
        mean — Calculates the mean (average value) of the cells in the
               neighborhood. This is the default.
        max  — Calculates the maximum (largest value) of the cells
               in the neighborhood.
        min  — Calculates the minimum (smallest value) of the cells
               in the neighborhood.
        std  — Calculates the standard deviation of the cells in the
               neighborhood.
        var  — Calculates the variance of the cells in the neighborhood.
    ignore_nodata : boolean, optional
        Denotes whether NoData values are ignored by the statistic
        calculation.
        
        True  — Specifies that if a NoData value exists within a
                neighborhood, the NoData value will be ignored. Only cells
                within the neighborhood that have data values will be
                used in determining the output value. This is the default.
        False — Specifies that if any cell in a neighborhood has a value
                of NoData, the output for the processing cell will be
                NoData. With this option, the presence of a NoData value
                implies that there is insufficient information to
                determine the statistic value for the neighborhood.

    Returns
    -------
    out_data : numpy array
        The output focal statistics array.

    """
    
    if not isinstance(neighborhood, (Rectangle, Circle, Wedge)):
        raise ValueError('Neighborhood class not implemented.')
    
    if statistic not in ('min', 'max', 'mean', 'dev', 'var'):
        raise ValueError('Statistic not implemented.')
    
    # add padding to the input array
    if isinstance(neighborhood, Rectangle):
        out_data = rectangfun(in_data, neighborhood.height,
                              neighborhood.width, statistic, ignore_nodata)
        
    if isinstance(neighborhood, (Circle, Wedge)):
        p = neighborhood.radius
    
        in_data = np.pad(in_data.astype(float), p, constant_values=None)
        out_data = np.copy(in_data)
    
        # determine indices of rows and columns of the input array
        # inside the padded array
        nrows = np.size(in_data, 0)
        index_rows = range(0, nrows)[p:-p]
        ncols = np.size(in_data, 1)
        index_cols = range(0, ncols)[p:-p]
    
        # loop through cells
        for row in index_rows:
            for col in index_cols:
            
                values = get_values(in_data, neighborhood, row, col)

                if ignore_nodata:
                    values = values[np.invert(np.isnan(values))]
                    out_data[row, col] = function[statistic](values)
                
                elif np.isnan(values).any():
                    out_data[row, col] = None
                
                else:
                    out_data[row, col] = function[statistic](values)
        
        out_data = out_data[p:-p, p:-p]
    
    return out_data



# helper functions for Circle and Wedge neighborhood
def get_values(data, neighborhood, row_processing, col_processing,
               show_window=False):
    """
    Returns the values of the cells determined by the neighborhood.

    Returns
    -------
    values : numpy.array

    """
    
    if isinstance(neighborhood, Circle):
        
        distance = np.copy(data.astype(float))
        
        for col in range(np.size(data, 1)): 
            for row in range(np.size(data, 0)):
            
                distance[row, col] = math.sqrt((row_processing - row)**2
                                               + (col_processing - col)**2)
        
        # to avoid rounding errors
        distance = np.round(distance, 2)
        
        # selecting cells that fall into the window.
        window = np.where(distance <= neighborhood.radius)
        
        # debugging feature
        if show_window:
            values = np.copy(data)
            values[window] = show_window
        
        else:
            values = data[window]
    
    if isinstance(neighborhood, Wedge):
        
        distance = np.copy(data.astype(float))
        angle = np.copy(data.astype(float))
        
        
        
        for col in range(np.size(data, 1)):
            for row in range(np.size(data, 0)):
            
                distance[row, col] = math.sqrt((row_processing - row)**2
                                               + (col_processing - col)**2)
                
                angle[row, col] = get_angle(row_processing, col_processing,
                                            row, col)
        
        # to avoid rounding errors
        distance = np.round(distance, 2)
        angle = np.round(angle, 2)
        
        # When the positive x-axis is included in the wedge, the end
        # angle is smaller than the start angle. In this case all the
        # angles between 0° and the end angle must be increased by 360°
        # so the condition for selecting the window works as intended.
        if neighborhood.start > neighborhood.end:
                    
            condition = (angle >= 0) & (angle <= neighborhood.end)
            angle = np.where(condition, angle + 360, angle)
            neighborhood.end = neighborhood.end + 360
        
        # The positive x-axis has an angle of 0°. It must be set
        # to 360°, when the end angle is exactly 360°, so the condition
        # for selecting the window works as intended.
        if neighborhood.end == 360:
            angle = np.where(angle == 0, 360, angle)
        
        # selecting cells that fall into the window.
        window = np.where((distance <= neighborhood.radius)
                          & (angle >= neighborhood.start)
                          & (angle <= neighborhood.end))
        
        # The angle of the processing cell is always set to 0°. But when
        # the start and end angle don't encompass 0°, the processing
        # cell would not be included in the window. Therefore it has to
        # be appended manually.
        window = (np.append(window[0], row_processing),
                  np.append(window[1], col_processing))
        
        # debugging feature
        if show_window:
            values = np.copy(data)
            values[window] = show_window
            values = (values, distance, angle)
        
        else:
            values = data[window]
            
    return values


def get_angle(row_processing, col_processing, row, col):
    """
    Returns the angle in arithmetic degrees, between the processing cell
    and the cell of the current loop iteration. The angle extends
    counterclockwise from 0 to 360, where 0 is on the positive x-axis.

    Returns
    -------
    angle : float
    """
    
    
    x = col - col_processing
    y = row_processing - row
    dist = math.sqrt((row_processing - row)**2
                     + (col_processing - col)**2)
    
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



# Helper functions for Rectangle neighborhood.
def rectangfun(data, height, width, statistic, ignore_nodata):
    
    
    """
    Helper function for rectangle neighborhood with different calculations
    for even and odd heights / widths.

    Parameters
    ----------
    data :         numpy array
                   The array to perform the focal statistics calculations on.
        
    height:        height of the rectangular in pixels
    
    width          width of the rectangular in pixels

    statistic:     The statistic type to be calculated.
                   mean, max, min, std or var
    
    ignore_nodata: Denotes whether NoData values are ignored by the statistic
                   calculation.
         

    Returns
    -------
    out_data : numpy array
        The output focal statistics array.

    """
    
    
    data = np.array(data)
    
    if height%2 == 0: # even height
        
        if width%2 == 0: # and even width
            
            top_wsize = int((height-2)/2)
            bot_wsize = int((height)/2)
            left_wsize = int((width-2)/2)
            right_wsize = int((width)/2)
            
            newdata = get_newdata(data,
                                  wsize_top     = top_wsize,
                                  wsize_left    = left_wsize,
                                  wsize_bot     = bot_wsize,
                                  wsize_right   = right_wsize,
                                  statistic     = statistic,
                                  ignore_nodata = ignore_nodata)
        
        else: # and odd width
            
            top_wsize = int((height-2)/2)
            bot_wsize = int((height)/2)
            width_wsize = int((width-1)/2)
           
            newdata = get_newdata(data,
                                  wsize_top     = top_wsize,
                                  wsize_left    = width_wsize,
                                  wsize_bot     = bot_wsize,
                                  wsize_right   = width_wsize,
                                  statistic     = statistic,
                                  ignore_nodata = ignore_nodata)
        
    else: # odd height
        
        if width%2 == 0: # and even width
            
            height_wsize = int((height-1)/2)
            left_wsize = int((width-2)/2)
            right_wsize = int((width)/2)
            
            newdata = get_newdata(data,
                                  wsize_top     = height_wsize,
                                  wsize_left    = left_wsize,
                                  wsize_bot     = height_wsize,
                                  wsize_right   = right_wsize,
                                  statistic     = statistic,
                                  ignore_nodata = ignore_nodata)
            
            
        else: # and odd width
            height_wsize = int((height-1)/2)
            width_wsize = int((width-1)/2)
            
            newdata = get_newdata(data,
                                  wsize_top     = height_wsize,
                                  wsize_left    = width_wsize,
                                  wsize_bot     = height_wsize,
                                  wsize_right   = width_wsize,
                                  statistic     = statistic,
                                  ignore_nodata = ignore_nodata)
    
    return newdata



def get_newdata(data, wsize_top, wsize_left,
                wsize_bot, wsize_right, statistic, ignore_nodata): 
    
    """
    Calculates the values of the cells determined by a specific function
    from a rectangle neighborhood

    Parameters
    ----------
    data :         numpy array
                   The array to perform the focal statistics calculations on.
        
    wsize_top:     The window size top; distance in pixels from central pixel to
                   top end of the neighborhood.
    
    wsize_left:    The window size left; distance in pixels from central pixel to
                   left end of the neighborhood.
                
    wsize_bot:     The window size bot; distance in pixels from central pixel to
                   bottom end of the neighborhood.
                
    wsize_right:   The window size right; distance in pixels from central pixel to
                   right end of the neighborhood.
                 
    statistic:     The statistic type to be calculated.
                   mean, max, min, std or var
    
    ignore_nodata: Denotes whether NoData values are ignored by the statistic
                   calculation.
         

    Returns
    -------
    out_data : numpy array
        The output focal statistics array.

    """  
    
    # filling newdata array with zeros
    newdata = np.zeros(data.shape)
    
    if ignore_nodata:
    
        for col in range(np.size(data, 1)):
            for row in range(np.size(data, 0)):
                
                ### edge cases ###
                
                # all corners:
                if col < wsize_left and row < wsize_top: # topleft
                    window = data[:row+wsize_bot+1, :col+wsize_right+1]
    
                elif (col < wsize_left
                      and row >= np.size(data, 0)-wsize_bot): # botleft
                    window = data[row-wsize_top:, :col+wsize_right+1]
    
                elif (col >= np.size(data, 1)-wsize_right
                      and row < wsize_top): # topright
                    window = data[:row+wsize_bot+1, col-wsize_left:]
    
                elif (col >= np.size(data, 1)-wsize_right
                      and row >= np.size(data, 0)-wsize_bot): # botright
                    window = data[row-wsize_top:, col-wsize_left:]
    
    
                # all edges:
                elif col < wsize_left: # left edge
                    window = data[row-wsize_top:row+wsize_bot+1,
                                  :col+(wsize_right)+1]
    
                elif row >= np.size(data, 0)-wsize_bot: # bot edge
                    window = data[row-wsize_top:,
                                  col-wsize_left:col+wsize_right+1]
    
                elif col >= np.size(data, 1)-wsize_right: # right edge
                    window = data[row-wsize_top:row+wsize_bot+1,
                                  col-wsize_left:]
    
                elif row < wsize_top: # top edge
                    window = data[:row+wsize_bot+1,
                                  col-wsize_left:col+wsize_right+1]
    
    
    
                else: # normal case
                    window = data[row-wsize_top:row+wsize_bot+1,
                                  col-wsize_left:col+wsize_right+1]
    
    
                newdata[row, col] = function[statistic](window)
                       
                    
    else:
        
        for col in range(np.size(data, 1)): # rows
            for row in range(np.size(data, 0)):

                    # without NAs in the neighborhood
                    if (wsize_top <= row < np.size(data, 0)-wsize_bot and
                            wsize_left <= col < np.size(data, 1)-wsize_right): # normal case
                        window = data[row-wsize_top:row+wsize_bot+1,
                                      col-wsize_left:col+wsize_right+1]

                        if np.isnan(window).any(): # if NAs in the neighborhood -> set value to NA
                            newdata[row, col] = None
                        else:
                            newdata[row, col] = function[statistic](window)

                    else: # buffer zone
                        newdata[row, col] = None
            
    
    return newdata



# dictionary with summary statistics
function = {
    "min": np.min,
    "max": np.max,
    "mean": np.mean,
    "var": np.var,
    "std": np.std}

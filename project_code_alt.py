# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 21:38:26 2020

@author: Brigitte Häuser, Guilherme Arruda, Manuel Händel
"""


import numpy as np
import math
from circles import *
from neighborhoods import *
from functions import *

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
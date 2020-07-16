# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:26:11 2020

@author: Brigitte Häuser, Guilherme Arruda, Manuel Händel

This script demonstrates the usage of the focal_statistics functions. 
The input dialog can be exchanged with a hard coded directory to the
necessary modules. To inspect the functions and classes open the
corresponding scripts or display their documentation in the console.
"""

import numpy as np
import os
path = input(("Enter the path to the working directory\n"
              "(location of focal_statistics modules):\n"), )
os.chdir(path)

from functions import (focal_statistics, get_values,
                       get_angle, get_newdata, rectangfun)
from classes import Rectangle, Circle, Wedge

# run the focal_statistics with some example code
file = np.arange(150).reshape(15, 10) 
print(file)
out = focal_statistics(file, Rectangle(4,3), 'max')
print('rectang default border \n', out)

out = focal_statistics(file, Circle(3), "max")
print('circle default border \n', out)

out = focal_statistics(file, Wedge(3, 0, 90), "max")
print('wedge default border \n', out)


out = get_values(file, Wedge(3, 45, 180), 7, 5, show_window = 1)
print('Display window \n', out[0])
print('Display distance \n', out[1])
print('Display angle \n', out[2])



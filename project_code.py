# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:26:22 2020

@author: Brigitte Häuser, Guilherme Arruda, Manuel Händel
"""


import numpy as np


def bordercases(data, wsize_top, wsize_left, wsize_bot, wsize_right): 
    
    # filling newdata array with zeros
    newdata = np.zeros(data.shape)
    
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
                
    return newdata


                
                
                
####################################### SHAPE FUNCTIONS ##############################################

# SQUARE #

def squarefun(data, diameter):
    data = np.array(data) 
    
    
              
    # diameter even -> central pixel is topleft
    if diameter%2==0:
        
        #small window size
        small_wsize = int((diameter-2)/2) # for top and left window
        big_wsize = int((diameter)/2) # for right and bot window
        
        newdata = bordercases(data, wsize_top = small_wsize, wsize_left = small_wsize, 
                              wsize_bot = big_wsize, wsize_right = big_wsize)
        
    
    else: # odd diameter
        

        # window size
        wsize = int((diameter-1)/2)
        
        newdata = bordercases(data, wsize, wsize, wsize, wsize) # for all sides the same window size


    return newdata
    
    
    
    
    
#################
#  Endfunction  #- so far only works with square as a shape :)
#################
def focsta(data, diameter, shape='square', start_angle=False, end_angle=False):
    
    data = np.array(data)
    
    if shape not in ('square', 'circular', 'retangular', 'wedge'):
        raise ValueError('Not a implemented shape.')
        
    
    if shape == 'square':
        return squarefun(data, diameter)
        
        
        
    elif shape == 'circular':
        pass
    
    
    elif shape == 'retangular':
        pass
        
        
    elif shape == 'wedge':
        pass


    
file = np.arange(60).reshape(10, 6) 
file2 = np.arange(start=60, stop=0, step=-1).reshape(10, 6) 

print(file)
print(focsta(file, diameter=3)) # please test other files and diameters boys!! :)

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:26:22 2020

@author: Brigitte Häuser, Guilherme Arruda, Manuel Händel
"""


import numpy as np


def bordercases(data, wsize_top, wsize_left, wsize_bot, wsize_right, border = 'default'): 
    
    # filling newdata array with zeros
    newdata = np.zeros(data.shape)
    
    if border == 'default':
    
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
                    
    elif border == 'buffer':
        
        for col in range(np.size(data, 1)): # rows
            for row in range(np.size(data, 0)):        
        
                if  row < np.size(data, 0)-wsize_bot and row >= wsize_top and col < np.size(data, 1)-wsize_right and col >= wsize_left: # normal case
                    window = data[row-wsize_top:row+wsize_bot+1, col-wsize_left:col+wsize_right+1]
                    
                    newdata[row, col] = np.max(window)
                    
                else: # buffer zone
                    newdata[row, col] = None
            
    
    else:
        raise ValueError('Not a border option')
        
                
    return newdata


                
                
                
####################################### SHAPE FUNCTIONS ##############################################

# SQUARE #

def squarefun(data, diameter, border):
    data = np.array(data) 
    
    
              
    # diameter even -> central pixel is topleft
    if diameter%2 == 0:
        
        #small window size
        small_wsize = int((diameter-2)/2) # for top and left window
        big_wsize = int((diameter)/2) # for right and bot window
        
        newdata = bordercases(data, wsize_top = small_wsize, wsize_left = small_wsize, 
                              wsize_bot = big_wsize, wsize_right = big_wsize, border = border)
        
    
    else: # odd diameter
        

        # window size
        wsize = int((diameter-1)/2)
        
        newdata = bordercases(data, wsize, wsize, wsize, wsize, border) # for all sides the same window size


    return newdata
    
# RETANGULAR #

def retangfun(data, height, width, border):
    data = np.array(data)
    
    if height%2 == 0: # even height
        
        if width%2 == 0: # and even width
            
            top_wsize = int((height-2)/2)
            bot_wsize = int((height)/2)
            left_wsize = int((width-2)/2)
            right_wsize = int((width)/2)
            
            newdata = bordercases(data, wsize_top = top_wsize, wsize_left = left_wsize, 
                              wsize_bot = bot_wsize, wsize_right = right_wsize, border = border)
        
        else: # and odd width
            
            top_wsize = int((height-2)/2)
            bot_wsize = int((height)/2)
            width_wsize = int((width-1)/2)
           
            newdata = bordercases(data, wsize_top = top_wsize, wsize_left = width_wsize, 
                              wsize_bot = bot_wsize, wsize_right = width_wsize, border = border)
        
    else: # odd height
        
        if width%2 == 0: # and even width
            
            height_wsize = int((height-1)/2)
            left_wsize = int((width-2)/2)
            right_wsize = int((width)/2)
            
            newdata = bordercases(data, wsize_top = height_wsize, wsize_left = left_wsize, 
                              wsize_bot = height_wsize, wsize_right = right_wsize, border = border)
            
            
        else: # and odd width
            height_wsize = int((height-1)/2)
            width_wsize = int((width-1)/2)
            
            newdata = bordercases(data, wsize_top = height_wsize, wsize_left = width_wsize, 
                              wsize_bot = height_wsize, wsize_right = width_wsize, border = border)
    
    return newdata

    
#################
#  Endfunction  #
#################
def focsta(data, diameter=False, shape='square', height=False, width=False, border = 'default', start_angle=False, end_angle=False):
    
    data = np.array(data)
    
    if shape not in ('square', 'circular', 'retangular', 'wedge'):
        raise ValueError('Not a implemented shape.')
        
    
    if shape == 'square':
        return squarefun(data, diameter, border)
        
        
        
    elif shape == 'circular':
        pass
    
    
    elif shape == 'retangular':
        
        return retangfun(data, height, width, border)
        
        
    elif shape == 'wedge':
        pass


    
file = np.arange(60).reshape(10, 6) 
file2 = np.arange(start=60, stop=0, step=-1).reshape(10, 6) 
print(file)

print('retang \n', focsta(file, shape='retangular', height=3, width=4, border='buffer'))
#print('dia = 5 \n', focsta(file2, diameter=5))

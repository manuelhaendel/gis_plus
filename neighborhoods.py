# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 21:52:45 2020

@author: Manuel
"""

class Rectangle:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Circle:
    
    def __init__(self, radius):
        self.radius = radius

class Wedge:
    
    def __init__(self, radius, start, end):
        self.radius = radius
        self.start = start
        self.end = end
        

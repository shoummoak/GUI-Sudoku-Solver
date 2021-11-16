#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 06:34:59 2020

@author: raisin
"""

class PotentialContainer:
    
    def __init__(self, pot_list):
        
#        fill the list with Nodes
        self.pots = [pot for pot in pot_list]
        self.size = len(self.pots)                
        self.pointer = 0
    
#    the iterator of the pots list  
#    modulo makes sure pointer always returns to 0 after after the last index
    def move_pointer(self):
        self.pointer += 1
        self.pointer %= 5
      
    def __str__(self):
        return str(self.pots)
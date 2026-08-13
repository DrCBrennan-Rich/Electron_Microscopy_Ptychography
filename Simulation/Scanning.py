# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.size': 40})

from Physics.Microscope import MicroscopeForward

'''
def Make_Scan_Positions(ObjectSize, ProbeSize, Step, Jitter = 0):

    ScanPositions = []

    for x in range(0, ObjectSize-ProbeSize+1, Step):
        for y in range(0, ObjectSize-ProbeSize+1, Step):
            
            #Create the jitter value centered on 0
            JitterX = np.random.normal(0, Jitter)
            JitterY = np.random.normal(0, Jitter)
            
            PositionX = x + JitterX
            PositionY = y + JitterY
            
            ScanPositions.append((PositionX, PositionY))

    return ScanPositions
'''

def Make_Scan_Positions(ObjectSize, ProbeSize, Step, Jitter=0.0):

    ScanPositions = []
    
    Padding = 2 
    
    #Restricts us to coordinates that are within bounds
    Margin = ProbeSize//2 + Padding + 4*Jitter

    PositionX = np.arange(Margin, ObjectSize-Margin, Step)

    PositionY = np.arange(Margin, ObjectSize-Margin, Step)

    for x in PositionX:
        for y in PositionY:
            
            #Create the jitter value centered on 0
            JitterX = np.random.normal(0, Jitter)
            JitterY = np.random.normal(0, Jitter)

            ActualX = x + JitterX
            ActualY = y + JitterY

            ScanPositions.append((ActualX, ActualY))

    return np.array(ScanPositions)

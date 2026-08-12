# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.size': 40})

from Physics.Microscope import MicroscopeForward

def Simulate_Ptychography(obj, Probe, ScanPositions, MicroscopeInstance,
                          Dose = None):

    DiffractionPatterns = []
    psize = Probe.shape[0]

    for x,y in ScanPositions:

        ObjectPatch = obj[x:x+psize, y:y+psize]

        ExitWave = ObjectPatch*Probe

        DetectorWave = MicroscopeForward(ExitWave, MicroscopeInstance)

        Intensity = np.abs(DetectorWave)*np.abs(DetectorWave)
        
        if Dose is not None:

           ExpectedCounts = Dose*Intensity

           Intensity = np.random.poisson(ExpectedCounts)/Dose

        DiffractionPatterns.append(Intensity)

    return np.array(DiffractionPatterns)


def Make_Scan_Positions(ObjectSize, ProbeSize, Step):

    ScanPositions = []

    for x in range(0, ObjectSize-ProbeSize+1, Step):
        for y in range(0, ObjectSize-ProbeSize+1, Step):

            ScanPositions.append((x, y))

    return ScanPositions
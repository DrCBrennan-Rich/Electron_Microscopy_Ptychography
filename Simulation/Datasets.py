# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
from Physics.Microscope import MicroscopeForward
from Simulation.Objects import  Extract_Object_Patch

def Add_Poisson_Noise(Intensity, Dose):
    #Insert Poisson statistics into the data to modify the original intensity
    
    if Dose <= 0: #Check that the dose is positive
        raise ValueError("A dose must be positive.")
    
    ExpectedCounts = Dose*Intensity
    
    Intensity = np.random.poisson(ExpectedCounts)/Dose
    
    return Intensity

def Simulate_Ptychography(Object, Probe, ScanPositions, MicroscopeInstance,
                          Dose = None):

    DiffractionPatterns = []
    psize = Probe.shape[0]

    for Position, (x, y) in enumerate(ScanPositions):

        ObjectPatch = Extract_Object_Patch(Object,x,y,psize)

        ExitWave = ObjectPatch*Probe

        DetectorWave = MicroscopeForward(ExitWave, MicroscopeInstance)

        Intensity = np.abs(DetectorWave)*np.abs(DetectorWave)
        
        if Dose is not None:

           Intensity = Add_Poisson_Noise(Intensity, Dose)

        DiffractionPatterns.append(Intensity)

    return np.array(DiffractionPatterns)

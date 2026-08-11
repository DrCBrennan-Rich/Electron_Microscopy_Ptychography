# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.size': 40})

def Reconstruction_Error(ObjectTrue, ObjectReconstructed):

    ObjectAligned = Align_Global_Phase(ObjectTrue, ObjectReconstructed)

    Difference = ObjectAligned - ObjectTrue
    
    #Calculate the normalised Frobenius norm
    Error = (np.linalg.norm(Difference)/np.linalg.norm(ObjectTrue))

    return Error


def Align_Global_Phase(ObjectTrue, ObjectReconstructed):

    #Inner product of original and reconstructed object then take angle
    PhaseOffset = np.angle(np.vdot(ObjectReconstructed, ObjectTrue))

    #Rotate by the correct angle to remove global phase
    ObjectAligned = ObjectReconstructed*np.exp(1j*PhaseOffset)

    return ObjectAligned

def Consistency_Error(
        ObjectReconstructed,
        ProbeReconstructed,
        Patterns,
        ScanPositions,
        Microscope,
        MicroscopeForward):

    ProbeSize = ProbeReconstructed.shape[0]

    Numerator = 0.0
    Denominator = 0.0

    for Position, (x, y) in enumerate(ScanPositions):

        # Extract object region illuminated by the probe
        ObjectPatch = ObjectReconstructed[x:x+ProbeSize,y:y+ProbeSize]

        # Current reconstructed exit wave
        ExitWave = ObjectPatch*ProbeReconstructed

        # Propagate to detector
        DetectorWave = MicroscopeForward(ExitWave, Microscope)

        # Predicted and measured amplitudes
        CalculatedAmplitude = np.abs(DetectorWave)
        MeasuredAmplitude = np.sqrt(Patterns[Position])

        # Accumulate squared error
        Numerator += np.sum((CalculatedAmplitude - MeasuredAmplitude)**2)

        Denominator += np.sum(MeasuredAmplitude**2)

    Error = np.sqrt(Numerator / Denominator)

    return Error
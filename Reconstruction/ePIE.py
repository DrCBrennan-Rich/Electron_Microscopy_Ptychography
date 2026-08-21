# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
from Physics.Microscope import MicroscopeForward, MicroscopeBackward
from Analysis.Metrics import Reconstruction_Error, Consistency_Error
from Simulation.Objects import  Extract_Object_Patch, Insert_Object_Patch

def ePIE(ObjectGuess,
         ProbeGuess,
         Patterns,
         ScanPositions,
         Microscope,
         Beta,
         BetaProbe,
         Iterations,
         ObjectTrue = None):
    
    ReconstructionErrors = []
    ConsistencyErrors = []
    ProbeSize = ProbeGuess.shape[0]
    
    for Iteration in range(Iterations):

        for Position,(x,y) in enumerate(ScanPositions):

            ObjectPatch = Extract_Object_Patch(ObjectGuess,x,y,ProbeSize)

            ExitWave = ProbeGuess*ObjectPatch

            DetectorWave = MicroscopeForward(ExitWave, Microscope)

            MeasuredAmplitude = np.sqrt(Patterns[Position])

            DetectorWaveUpdated = (MeasuredAmplitude*np.exp(1j*np.angle(DetectorWave)))

            ExitWaveUpdated = MicroscopeBackward(DetectorWaveUpdated, Microscope)

            Difference = ExitWaveUpdated - ExitWave
            
            # Object update
            ProbeMaximum = np.max(np.abs(ProbeGuess)**2)
            
            ObjectUpdate = (
                Beta*np.conj(ProbeGuess)/(ProbeMaximum+1E-15)*Difference)
            
            ObjectGuess = Insert_Object_Patch(ObjectGuess, ObjectUpdate, 
                                              x, y, ProbeSize)

            # Probe update
            ObjectMaximum = np.max(np.abs(ObjectPatch)**2)

            ProbeGuess += (
                BetaProbe*np.conj(ObjectPatch)/(ObjectMaximum+1E-15)*Difference)
            

        # Plot progress
        if Iteration %((Iterations+1)//3) == 0:

            plt.figure(figsize=(9,9))
            plt.imshow(
                np.abs(ObjectGuess),
                cmap="inferno"
            )
            plt.title(f"Iteration {Iteration}")
            plt.colorbar()
            plt.show()
            
        # Calculate consistency error
        ConsistencyError = Consistency_Error(
           ObjectGuess,
           ProbeGuess,
           Patterns,
           ScanPositions,
           Microscope,
           MicroscopeForward)
        
        ConsistencyErrors.append(ConsistencyError)
            
        # Calculate reconstruction error
        if ObjectTrue is not None:

            Error = Reconstruction_Error(
                ObjectTrue,
                ObjectGuess
            )

            ReconstructionErrors.append(Error)
            
    return ObjectGuess, ProbeGuess, ReconstructionErrors, ConsistencyErrors
            
    

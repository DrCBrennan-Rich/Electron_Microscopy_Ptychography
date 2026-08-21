# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
from Physics.Microscope import MicroscopeForward, MicroscopeBackward
from Analysis.Metrics import Reconstruction_Error, Consistency_Error
from Simulation.Objects import  Extract_Object_Patch

def rPIE(ObjectGuess,
         ProbeGuess,
         Patterns,
         ScanPositions,
         Microscope,
         Beta,
         BetaProbe,
         Iterations,
         alpha,
         ObjectTrue = None):
    
    ReconstructionErrors = []
    ConsistencyErrors = []
    ProbeSize = ProbeGuess.shape[0]
    
    #Safety parameter
    epsilon = 1E-15
    
    for Iteration in range(Iterations):
        
        ProbeMaximum = np.max(np.abs(ProbeGuess)**2)

        for Position,(x,y) in enumerate(ScanPositions):

            ObjectPatch = Extract_Object_Patch(ObjectGuess,x,y,ProbeSize)
            
            ObjectMaximum = np.max(np.abs(ObjectPatch)**2)
            
            ExitWave = ProbeGuess*ObjectPatch

            DetectorWave = MicroscopeForward(ExitWave, Microscope)

            MeasuredAmplitude = np.sqrt(Patterns[Position])

            DetectorWaveUpdated = (MeasuredAmplitude*np.exp(1j*np.angle(DetectorWave)))

            ExitWaveUpdated = MicroscopeBackward(DetectorWaveUpdated, Microscope)

            Difference = ExitWaveUpdated - ExitWave
            
            #rPIE object update
            ObjectGuess[x:x+ProbeSize,y:y+ProbeSize] += (
                Beta*np.conj(ProbeGuess)/((1-alpha)*np.abs(ProbeGuess)**2+alpha*ProbeMaximum+epsilon)*Difference)
            
            #rPIE probe update
            ProbeGuess += (
                BetaProbe*np.conj(ObjectPatch)/((1-alpha)*np.abs(ObjectPatch)**2+alpha*ObjectMaximum+epsilon)*Difference)

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
            
    

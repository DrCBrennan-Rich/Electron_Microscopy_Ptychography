# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.size': 40})

ElectronCharge = 1.60217663E-19 #Charge on the electron in Coulombs
ElectronMass = 9.1093837E-31 #Mass of electron in kg
SpeedOfLight = 299792458 #Speed of light in a vacuum
PlankConstant = 6.62607015E-34 #Plank constant

def Voltage_To_Wavelength(Voltage, ReturnError = None):
    #Voltage in eV 
    
    RestMassEnergy = ElectronMass*SpeedOfLight*SpeedOfLight
    
    #Energy in Joules
    Energy = Voltage*ElectronCharge + RestMassEnergy
    
    Momentum = np.sqrt(Energy*Energy-RestMassEnergy*RestMassEnergy)/SpeedOfLight
    
    Wavelength = PlankConstant/Momentum
    
    if ReturnError is not None:
        
        ClassicalWavelength = PlankConstant/np.sqrt(2*ElectronMass*Voltage*ElectronCharge)
        
        ClassicalError = (ClassicalWavelength - Wavelength)/Wavelength
        
        return Wavelength, ClassicalError
    
    return Wavelength
    



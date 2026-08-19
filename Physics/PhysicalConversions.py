# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
from scipy import constants

ElectronCharge = constants.e #Charge on the electron in Coulombs
ElectronMass = constants.m_e #Mass of electron in kg
SpeedOfLight = constants.c #Speed of light in a vacuum
PlankConstant = constants.h #Plank constant

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
    



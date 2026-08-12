# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.size': 40})

def Make_Probe(Size, Sigma, Defocus=0, Aberration=False):

    x = np.arange(Size)-Size//2
    y = np.arange(Size)-Size//2

    X,Y = np.meshgrid(x,y)

    R2 = X*X+Y*Y

    Amplitude = np.exp(-R2/(2*Sigma*Sigma))
    Phase = np.zeros_like(Amplitude)

    if Defocus != 0:
        Phase += (np.pi*Defocus*(R2))
        
    Probe = Amplitude*np.exp(1j*Phase)

    return Probe
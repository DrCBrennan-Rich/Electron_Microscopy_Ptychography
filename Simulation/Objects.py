# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.size': 40})

#Function that constructs the amplitude of the object
'''
def Make_Amplitude(Size, AmplitudeSize):

    Amplitude = np.zeros((Size, Size))

    Start = (Size -AmplitudeSize)//2
    End = Start +AmplitudeSize

    Amplitude[Start:End, Start:End] = 1

    
    # Add some structure
    Amplitude[Start+13, Start+14] = 10
    Amplitude[Start+14, Start+13] = 10
    Amplitude[Start+15, Start+12] = 10
    Amplitude[Start+15, Start+11] = 10
    Amplitude[Start+15, Start+10] = 10
    Amplitude[Start+15, Start+9] = 8
    Amplitude[Start+15, Start+8] = 8
    Amplitude[Start+15, Start+7] = 8
    Amplitude[Start+15, Start+6] = 8
    Amplitude[Start+14, Start+5] = 8
    Amplitude[Start+13, Start+4] = 8
    Amplitude[Start+12, Start+3] = 6
    Amplitude[Start+11, Start+3] = 6
    Amplitude[Start+10, Start+3] = 6
    Amplitude[Start+9, Start+3] = 6
    Amplitude[Start+8, Start+3] = 4
    Amplitude[Start+7, Start+3] = 4
    Amplitude[Start+6, Start+3] = 4
    Amplitude[Start+5, Start+3] = 4
    Amplitude[Start+4, Start+3] = 4
    Amplitude[Start+3, Start+4] = 2
    Amplitude[Start+2, Start+5] = 2
    Amplitude[Start+1, Start+6] = 2
    Amplitude[Start+1, Start+7] = 5
    Amplitude[Start+1, Start+8] = 5
    Amplitude[Start+1, Start+9] = 5
    Amplitude[Start+1, Start+10] = 5
    Amplitude[Start+1, Start+11] = 15
    Amplitude[Start+1, Start+12] = 15
    Amplitude[Start+2, Start+13] = 15
    Amplitude[Start+3, Start+14] = 15
    
    return Amplitude, Start, End
'''
#Function that constructs the amplitude of the object
def Make_Amplitude(Size, ObjectSize):

    x = np.arange(Size) -Size/2
    y = np.arange(Size) -Size/2

    X, Y = np.meshgrid(x, y)

    R2 = X*X+Y*Y

    Amplitude = np.exp(-R2/(2*ObjectSize*ObjectSize))

    # Add several amplitude features
    Amplitude += 0.5 * np.exp(-((X-10)**2 + (Y+8)**2)/(2*3**2))

    Amplitude += 0.3 * np.exp(-((X+12)**2 + (Y-5)**2)/(2*5**2))
    
    Amplitude += 0.8 * np.exp(-((X+40)**2 + (Y-2)**2)/(2*10**2))
    
    return Amplitude, Size, Size

#Function that constructs the phase of the object
def Make_Phase(Size, ObjectSize):

    Phase = np.zeros((Size, Size))

    Start = (Size -ObjectSize)//2
    End = Start +ObjectSize

    x = np.arange(Size)
    y = np.arange(Size)

    X, Y = np.meshgrid(x, y)

    Centre = (Start +End -1)/2

    R2 = (X -Centre)**2 + (Y -Centre)**2

    Sigma = 5
    PhaseAmplitude = np.pi

    Phase = PhaseAmplitude * np.exp(
        -R2/(2*Sigma**2)
    )

    #Remove phase outside the object
    Phase[:Start, :] = 0
    Phase[End:, :] = 0
    Phase[:, :Start] = 0
    Phase[:, End:] = 0

    return Phase

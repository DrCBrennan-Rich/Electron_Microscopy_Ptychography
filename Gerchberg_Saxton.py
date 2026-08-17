# -*- coding: utf-8 -*-
"""
@author: cbrph
"""

import numpy as np
import matplotlib.pyplot as plt 

#Simulation parameters

#Total image size
N = 64           
#Size of square object at image center      
Object_size = 20       

#Create Objectect
Object = np.zeros((N, N))

start = (N - Object_size) // 2
end = start + Object_size

#Put a simple object in the centre
Object[start:end, start:end] = 1

#Add structure
Object[N//2+4,N//2+4] = 2
Object[N//2+4,N//2+6] = 2
Object[N//2+6,N//2+5] = 10

#Plot
plt.figure(figsize=(5,5))
plt.imshow(Object, cmap="inferno", interpolation="nearest")
plt.colorbar(label="Amplitude")
plt.title("Original Objectect")
plt.show()


Support = np.zeros((N, N), dtype=bool)
Support[start:end, start:end] = True

Psi_true = np.fft.fft2(Object)

Amplitude = np.abs(Psi_true)
Phase = np.angle(Psi_true)
Intensity = Amplitude*Amplitude

#Shift for displaying
AmplitudeDisplay = np.fft.fftshift(Amplitude)
PhaseDisplay = np.fft.fftshift(Phase)
IntensityDisplay = np.fft.fftshift(Intensity)

#Plot
fig, ax = plt.subplots(2, 2, figsize=(10,10))

# Objectect
Image0 = ax[0,0].imshow(Object, cmap="inferno", interpolation="nearest")
ax[0,0].set_title("Objectect")
plt.colorbar(Image0, ax=ax[0,0])

#Fourier amplitude
Image1 = ax[0,1].imshow(AmplitudeDisplay, cmap="inferno")
ax[0,1].set_title("Fourier Amplitude")
plt.colorbar(Image1, ax=ax[0,1])

#Fourier phase
Image2 = ax[1,0].imshow(PhaseDisplay, cmap="twilight")
ax[1,0].set_title("Fourier Phase")
plt.colorbar(Image2, ax=ax[1,0])

#Diffraction intensity
Image3 = ax[1,1].imshow(np.log1p(IntensityDisplay), cmap="inferno")
ax[1,1].set_title("Diffraction Intensity (log scale)")
plt.colorbar(Image3, ax=ax[1,1])

plt.tight_layout()
plt.show()

#Gerchberg-Saxton algorithm

FlatPhase = np.zeros((N,N))
RandomPhase = np.random.uniform(0, 2*np.pi, size=(N, N))

Phase = FlatPhase

Psi = Amplitude*np.exp(1j*Phase)

psi = np.fft.ifft2(Psi)

plt.figure(figsize=(6,6))
plt.imshow(np.real(psi), cmap="inferno")
plt.title("Initial Guess")
plt.colorbar()
plt.show()


for Iteration in range(200):

    psi = np.fft.ifft2(Psi)

    #Apply support constraint
    psi[~Support] = 0
    
    #Always positive constraint
    psi = np.real(psi)
    psi[psi<0] = 0

    Psi = np.fft.fft2(psi)

    #Replace Fourier amplitude with measured amplitude
    Psi = Amplitude*np.exp(1j*np.angle(Psi))
    
    if Iteration % 50 == 0:
        plt.figure(figsize=(6,6))
        plt.imshow(np.real(psi), cmap="inferno", interpolation="nearest")
        plt.title(f"Iteration {Iteration}")
        plt.colorbar()
        plt.show()
    

Reconstruction = np.real(np.fft.ifft2(Psi))

plt.figure(figsize=(5,5))
plt.imshow(Reconstruction, cmap="inferno", interpolation="nearest")
plt.colorbar()
plt.title("Gerchberg-Saxton Reconstruction")
plt.show()

# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.size': 40})


def FraunhoferPropagate(psi):
    Psi = np.fft.fft2(psi)
    return Psi

def BackFraunhoferPropagate(psi):
    Psi = np.fft.ifft2(psi)
    return Psi

def FresnelPropagate(psi, Wavelength, PixelSize, Distance):
    
    Ny, Nx = psi.shape 
    fx = np.fft.fftfreq(Nx, d=PixelSize)
    fy = np.fft.fftfreq(Ny, d=PixelSize)

    FX, FY = np.meshgrid(fx, fy)
    H = np.exp(-1j*np.pi*Wavelength*Distance*(FX**2+FY**2))
    
    Psi = np.fft.fft2(psi)*H
    return Psi

def BackFresnelPropagate(psi, Wavelength, PixelSize, Distance):
    Ny, Nx = psi.shape
    
    fx = np.fft.fftfreq(Nx, d=PixelSize)
    fy = np.fft.fftfreq(Ny, d=PixelSize)

    FX, FY = np.meshgrid(fx, fy)
    H = np.exp(-1j*np.pi*Wavelength*Distance*(FX**2+FY**2))
    
    Psi = np.fft.ifft2(psi*np.conj(H))
    
    return Psi




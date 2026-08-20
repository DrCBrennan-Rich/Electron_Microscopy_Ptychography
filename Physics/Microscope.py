# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
from Physics import Propagation as Prg

class Microscope:

    def __init__(
        self,
        Wavelength,
        PixelSize,
        Distance,
        FocalLength,
        propagator="Fraunhofer",
        fresnel=False,
        lens=False
    ):
        self.Wavelength = Wavelength
        self.PixelSize = PixelSize
        self.Distance = Distance
        self.FocalLength = FocalLength

        self.propagator = propagator
        self.fresnel = fresnel
        self.lens = lens


def MicroscopeForward(ExitWave, microscope):

    psi = ExitWave

    if microscope.propagator.lower() == "fraunhofer":

        psi = Prg.FraunhoferPropagate(psi)

    elif microscope.propagator.lower() == "fresnel":

        psi = Prg.FresnelPropagate(
            psi,
            microscope.Wavelength,
            microscope.PixelSize,
            microscope.Distance
        )

    elif microscope.propagator.lower() == "angular_spectrum":

        psi = Prg.AngularSpectrumPropagate(
            psi,
            microscope.Wavelength,
            microscope.PixelSize,
            microscope.Distance
        )

    else:
        raise ValueError(
            f"Unknown propagator: {microscope.propagator}"
        )

    return psi


def MicroscopeBackward(DetectorWave, microscope):

    psi = DetectorWave

    if microscope.propagator.lower() == "fraunhofer":

        psi = Prg.BackFraunhoferPropagate(psi)

    elif microscope.propagator.lower() == "fresnel":

        psi = Prg.BackFresnelPropagate(
            psi,
            microscope.Wavelength,
            microscope.PixelSize,
            microscope.Distance
        )

    elif microscope.propagator.lower() == "angular_spectrum":

        psi = Prg.BackAngularSpectrumPropagate(
            psi,
            microscope.Wavelength,
            microscope.PixelSize,
            microscope.Distance
        )

    else:
        raise ValueError(
            f"Unknown propagator: {microscope.propagator}"
        )

    return psi

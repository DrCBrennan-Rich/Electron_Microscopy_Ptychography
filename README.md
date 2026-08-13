# Electron-Microscopy-Ptychography
Here you will find a set of scripts to introduce many of the most important concepts in Ptychography and phase retrieval in general.

The central file in which all parameters will be set is InitialTesting.py
Here, the microcopy paramters
Wavelength, PixelSize, Distance to detector, FocalLength, and the desired propagator (currently either Fresnel or Fraunhofer) can be created in the micoscope object.

After this, a step and probe size has to be selected for the simulated probe that will be rastering over the object.

Then, the update parameters for the retrieval algorithm (currently either ePIE or rPIE) Beta for the object nad BetaProbe for the probe are assigned.

Finally, the number of iterations (typically ~ 500) can be selected.

Object and probe amplitude and phase creation is handled by Simulation\Object.py and Simulation\Probes.py respectively.

The scanning positions (including subpixel shifts) are produced by Simulation\Scanning.py and then are used to simulate a complete set of diffraction patterns to use in the ptychography by Simulation\Datasets.py

The microscope physics and the modelling of the electron wave propagation from lens to detector can be found in Physics\Microscope.py

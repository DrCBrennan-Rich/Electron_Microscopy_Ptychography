# Electron-Microscopy-Ptychography
Here you will find a set of scripts to introduce many of the most important concepts in Ptychography and phase retrieval in general.

The central file in which all parameters will be set is InitialTesting.py
Here, the microcopy paramters
Wavelength, PixelSize, Distance to detector, FocalLength, and the desired propagator (currently either Fresnel or Fraunhofer) can be created in the micoscope object.

After this, a step and probe size has to be selected for the simulated probe that will be rastering over the object.

Then, the update parameters for the retrieval algorithm (currently either ePIE or rPIE) Beta for the object nad BetaProbe for the probe are assigned.

Finally, the number of iterations (typically ~ 500) can be selected.

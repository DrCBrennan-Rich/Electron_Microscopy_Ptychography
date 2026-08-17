# -*- coding: utf-8 -*-
"""
@author: cbrph
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 40})

from Physics.Microscope import Microscope, MicroscopeForward
from Physics.PhysicalConversions import Voltage_To_Wavelength
from Reconstruction.ePIE import ePIE
from Reconstruction.rPIE import rPIE
from Simulation.Objects import Make_Amplitude, Make_Phase
from Simulation.Probes import Make_Probe
from Simulation.Scanning import Make_Scan_Positions
from Analysis.Metrics import Reconstruction_Error, Align_Global_Phase, Consistency_Error
from Simulation.Datasets import Simulate_Ptychography


########   Simulation parameters   ########
np.random.seed(420)

#Total image size and internal object size
N = 75               
ObjectSize = 45       

MicroscopeInstance = Microscope(
    Wavelength=Voltage_To_Wavelength(100E3),
    PixelSize=1E-8,
    Distance=10,
    FocalLength=0.1,
    propagator="Fresnel")

#Probe construction sizes
Step = 5
ProbeSize = 15

#Update parameters
BetaObject = 0.5
BetaProbe = 0.05

#Number of iterations performed
Iterations = 600


########   Create and plot object   ########


Amplitude, Start, End = Make_Amplitude(N, ObjectSize)
Phase = Make_Phase(N, ObjectSize)

Object = Amplitude*np.exp(1j*Phase)

plt.figure(figsize=(9,9))
plt.imshow(np.abs(Object), cmap="inferno", interpolation="nearest")
plt.colorbar(label="Amplitude")
plt.title("Object Amplitude")
plt.show()

PhaseDisplay = np.angle(Object)%(2*np.pi)

PhaseDisplay[np.abs(Object) == 0] = np.nan

plt.figure(figsize=(9,9))
plt.imshow(PhaseDisplay, cmap="twilight",
           vmin=0,
           vmax=2*np.pi,
           interpolation="nearest")

plt.colorbar(label="Phase (rad)")
plt.title("Object Phase")
plt.show()


########   Create the probe   ########


ScanPositions = Make_Scan_Positions(Object.shape[0], ProbeSize, Step)

Probe = Make_Probe(ProbeSize, 4)


#Plot the probe after creation

# plt.figure(figsize=(9,9))
# plt.imshow(np.abs(Probe),cmap="inferno")
# plt.title("Probe")
# plt.colorbar()
# plt.title("Probe Beam")
# plt.show()

# plt.figure(figsize=(9,9))
# plt.imshow(np.angle(Probe)%(2*np.pi), cmap="twilight", vmin=0, vmax=2*np.pi)
#            
# plt.colorbar()
# plt.title("Probe phase")
# plt.show()


########   Simulate the diffraction patterns   ########



Patterns = Simulate_Ptychography(Object, Probe, ScanPositions, MicroscopeInstance, Dose =10000)

ObjectFourier = np.fft.fft2(Object)

FourierAmplitude = np.abs(ObjectFourier)
FourierPhase = np.angle(ObjectFourier) % (2*np.pi)
FourierIntensity = FourierAmplitude*FourierAmplitude

#Shift for display
amplitude_display = np.fft.fftshift(FourierAmplitude)
phase_display = np.fft.fftshift(FourierPhase)
intensity_display = np.fft.fftshift(FourierIntensity)


#Plot a single diffraction pattern
# PatternNumber = 11

# plt.figure(figsize=(9,9))
# plt.imshow(np.log1p(Patterns[pattern_number]), cmap="inferno")
# plt.colorbar(label="log(Intensity)")
# plt.title(f"Diffraction pattern {pattern_number}")
# plt.show()

# Position = PatternNumber

# x,y = ScanPositions[Position]

# plt.figure(figsize=(9,9))

# plt.imshow(np.abs(Object), cmap="inferno", interpolation="nearest")
#     
# plt.gca().add_patch(
#     plt.Rectangle(
#         (y, x),
#         Probe.shape[1],
#         Probe.shape[0],
#         fill=False,
#         edgecolor="red",
#         linewidth=2))

# plt.colorbar(label="Amplitude")
# plt.title(f"Probe position {Position}")
# plt.show()


########   Reconstruction routine   ########


ObjectGuess = np.ones_like(Object, dtype=complex)
#ObjectGuess = (np.random.rand(*obj.shape)+1j*np.random.rand(*obj.shape))

ProbeSize = Probe.shape[0]

ProbeGuess = Make_Probe(ProbeSize, 1)

#ProbeGuess = Probe.copy()

#Call solver and perform the main reconstruction loop
ObjectReconstructed, ProbeReconstructed, ReconstructionErrors, ConsistencyErrors= ePIE(
    ObjectGuess=ObjectGuess,
    ProbeGuess=ProbeGuess,
    Patterns=Patterns,
    ScanPositions=ScanPositions,
    Microscope=MicroscopeInstance,
    Beta=BetaObject,
    BetaProbe=BetaProbe,
    Iterations=Iterations,
    #alpha = 0.8,
    ObjectTrue=Object)

Error = Reconstruction_Error(Object, ObjectReconstructed)
print(f"Reconstruction error = {Error:.6e}")

ConsistencyError = Consistency_Error(
    ObjectReconstructed,
    ProbeReconstructed,
    Patterns,
    ScanPositions,
    MicroscopeInstance,
    MicroscopeForward)

print(f"Data consistency error = {ConsistencyError:.6e}")

ObjectAligned = Align_Global_Phase(Object, ObjectReconstructed)

#Mask regions where the amplitude is essentially zero
Threshold = 0.01

TruePhase = np.ma.masked_where(
    np.abs(Object) < Threshold,
    np.angle(Object) %(2*np.pi))

ReconstructedPhase = np.ma.masked_where(
    np.abs(ObjectAligned) < Threshold,
    np.angle(ObjectAligned) %(2*np.pi))


fig, axes = plt.subplots(3, 2, figsize=(14, 18))

PhaseCmap = plt.cm.twilight.copy()
PhaseCmap.set_bad(color="lightgrey")   # Colour for masked pixels



########   True object   ########



axes[0, 0].imshow(
    np.abs(Object),
    cmap="inferno",
    interpolation="nearest")

axes[0, 0].set_title("True amplitude")
axes[0, 0].set_axis_off()

# True phase
axes[0, 1].imshow(
    TruePhase,
    cmap=PhaseCmap,
    vmin=0,
    vmax=2*np.pi,
    interpolation="nearest")

axes[0, 1].set_title("True phase")
axes[0, 1].set_axis_off()



########   Reconstruction   ########


axes[1, 0].imshow(
    np.abs(ObjectAligned),
    cmap="inferno",
    interpolation="nearest")

axes[1, 0].set_title("Reconstructed amplitude")
axes[1, 0].set_axis_off()

# Reconstructed phase
axes[1, 1].imshow(
    ReconstructedPhase,
    cmap=PhaseCmap,
    vmin=0,
    vmax=2*np.pi,
    interpolation="nearest")

axes[1, 1].set_title("Reconstructed phase")
axes[1, 1].set_axis_off()



########   Difference   ########


AmplitudeDifference = (np.abs(ObjectAligned) - np.abs(Object))

PhaseDifference = np.angle(
    ObjectAligned * np.conj(Object))


axes[2, 0].imshow(
    AmplitudeDifference,
    cmap="RdBu_r",
    interpolation="nearest")

axes[2, 0].set_title("Amplitude difference")
axes[2, 0].set_axis_off()

axes[2, 1].imshow(
    PhaseDifference,
    cmap="twilight",
    vmin=-np.pi,
    vmax=np.pi,
    interpolation="nearest")

axes[2, 1].set_title("Phase difference")
axes[2, 1].set_axis_off()


plt.tight_layout()
plt.show()

#Plot Errors against iterations 
plt.figure(figsize=(15, 12)) 
plt.plot( np.arange(1, Iterations + 1), ReconstructionErrors, linewidth=3, color = "red") 
plt.xlabel("Iteration") 
plt.ylabel("Normalized reconstruction error") 
plt.yscale("log") 
plt.grid(True) 
plt.show() 

plt.figure(figsize=(15, 12)) 
plt.plot( np.arange(1, Iterations + 1), ConsistencyErrors, linewidth=3, color = "orange") 
plt.xlabel("Iteration") 
plt.ylabel("Data consistency error") 
plt.yscale("log") 
plt.grid(True) 
plt.show()


########   Probe comparison   ########


TrueProbePhase = np.angle(Probe) % (2*np.pi)

ReconstructedProbePhase = (np.angle(ProbeReconstructed) % (2*np.pi))

ProbeAmplitudeDifference = (np.abs(ProbeReconstructed) - np.abs(Probe))

ProbePhaseDifference = np.angle(ProbeReconstructed * np.conj(Probe))

fig, axes = plt.subplots(3, 2, figsize=(14, 18))


########   True probe   ########


axes[0, 0].imshow(
    np.abs(Probe),
    cmap="inferno",
    interpolation="nearest")

axes[0, 0].set_title("True probe amplitude")
axes[0, 0].set_axis_off()

axes[0, 1].imshow(
    TrueProbePhase,
    cmap=PhaseCmap,
    vmin=0,
    vmax=2*np.pi,
    interpolation="nearest")

axes[0, 1].set_title("True probe phase")
axes[0, 1].set_axis_off()



########   Reconstructed probe   ########


axes[1, 0].imshow(
    np.abs(ProbeReconstructed),
    cmap="inferno",
    interpolation="nearest"
)
axes[1, 0].set_title("Reconstructed probe amplitude")
axes[1, 0].set_axis_off()

axes[1, 1].imshow(
    ReconstructedProbePhase,
    cmap=PhaseCmap,
    vmin=0,
    vmax=2*np.pi,
    interpolation="nearest")

axes[1, 1].set_title("Reconstructed probe phase")
axes[1, 1].set_axis_off()



########   Difference   ########


axes[2, 0].imshow(
    ProbeAmplitudeDifference,
    cmap="RdBu_r",
    interpolation="nearest")

axes[2, 0].set_title("Probe amplitude difference")
axes[2, 0].set_axis_off()

axes[2, 1].imshow(
    ProbePhaseDifference,
    cmap="twilight",
    vmin=-np.pi,
    vmax=np.pi,
    interpolation="nearest")

axes[2, 1].set_title("Probe phase difference")
axes[2, 1].set_axis_off()


plt.tight_layout()
plt.show()

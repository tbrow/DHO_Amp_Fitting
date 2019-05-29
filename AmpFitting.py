# -*- coding: utf-8 -*-
"""
Created on Wed May 29 09:33:23 2019

@author: teb3

This code is for fitting the Amplitude response to sinusoidal forcing of a damped harmonic oscillator
Designed for .csv files containing multiple tunes over the same frequency range
Application: Atomic force microscopy
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import glob

#Lorentzian fit to the driven damped harmonic oscillator, from Gannepalli et al., Nanotech. (2011)
def SHO(f, fo, Adrive, Q):
    return fo**2*Adrive/np.sqrt((fo**2-f**2)**2+(fo*f/Q)**2)

files=glob.glob('*.csv')

for filename in files:
    alldata = pd.read_csv(filename)
    minFreq = 40000
    maxFreq = 80000
    alldata = alldata[alldata.iloc[:, 0] >= minFreq]
    alldata = alldata[alldata.iloc[:, 0] <= maxFreq]
    FreqData = alldata.iloc[:, 0]
    AmpData = alldata.filter(like='Amp', axis = 1)
    plt.semilogy(FreqData, AmpData)
    
    z = 0
    for col in AmpData.columns:
        ydata = AmpData.values[:, z]
        z += 1
        popt, pcov = curve_fit(SHO, FreqData, ydata, p0=[60000, .01, 10])
        
        plt.semilogy(FreqData, SHO(FreqData, *popt),':')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.title(filename)
    plt.show()
    

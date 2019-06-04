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
AllCoeffs=[1]*len(files)
for filename in range(len(files)):
    alldata = pd.read_csv(files[filename])
    minFreq = 40000
    maxFreq = 80000
    alldata = alldata[alldata.iloc[:, 0] >= minFreq]
    alldata = alldata[alldata.iloc[:, 0] <= maxFreq]
    FreqData = alldata.iloc[:, 0]
    AmpData = alldata.filter(like='Amp', axis = 1)
    plt.semilogy(FreqData, AmpData)
    
    coeffs=pd.DataFrame() 
    
    for col in range(len(AmpData.columns)):
        ydata = AmpData.values[:, col]
        popt, pcov = curve_fit(SHO, FreqData, ydata, p0=[60000, .005, 10])
        coeffs=pd.concat([coeffs, pd.DataFrame(popt)], axis=1)
        plt.semilogy(FreqData, SHO(FreqData, *popt),':')
        
        
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.title(files[filename])
    plt.show()
    
    coeffs.index=['fo','Adrive','Q']
    coeffs.columns = list(AmpData.columns)
#    print(coeffs)
    AllCoeffs[filename] = coeffs

for x in range(len(files)):
    a=AllCoeffs[x].T
    Qs=a.Q[a.Q<100].sort_values(ascending=False)
    
    d = [0]*len(Qs)
    for depth in range(len(Qs)):
        d[depth] = (depth+1)*100
        
    plt.plot(d,1/Qs)
    plt.xlabel('Insertion Length [nm]')
    plt.ylabel('1/Q')
    


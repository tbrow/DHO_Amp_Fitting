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

files=glob.glob('./AggregatedViscData/190710/NN_N100_2.csv')
AllCoeffs=[1]*len(files)
for filenumber in range(len(files)):
    alldata = pd.read_csv(files[filenumber])
    minFreq = 50000
    maxFreq = 70000
    alldata = alldata[alldata.iloc[:, 0] >= minFreq]
    alldata = alldata[alldata.iloc[:, 0] <= maxFreq]
    FreqData = alldata.iloc[:, 0]
    AmpData = alldata.filter(like='AmpV', axis = 1)
    AmpData=AmpData[AmpData.columns[:-1]] #drop last column (air)
    plt.semilogy(FreqData, AmpData)
    
    coeffs=pd.DataFrame() 
    pnext = [60000, 0.005, 2]
    for col in reversed(range(len(AmpData.columns))): #fit the higher Q peaks first

        ydata = AmpData.values[:, col]
        popt, pcov = curve_fit(SHO, FreqData, ydata, p0=pnext, method='trf')
        coeffs=pd.concat([coeffs, pd.DataFrame(popt)], axis=1)
        plt.semilogy(FreqData, SHO(FreqData, *popt),':')
        pnext = popt #reuse the fitted parms as the initial guess for the next curve
        
        
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [V - arb.]')
    plt.title(files[filenumber])
    plt.savefig('./figures/NN_N100_Amp.png',dpi=300)
    plt.show()
    
    
    coeffs.index=['fo','Adrive','Q']
    coeffs.columns = list(AmpData.columns)
    AllCoeffs[filenumber] = coeffs
  
allQ = pd.DataFrame()    
    
for filenumber in range(len(files)):
    Qs=AllCoeffs[filenumber].iloc[2]
    allQ = pd.concat([allQ,Qs], axis = 1)        
    d = list(range(100,100*len(Qs)+100, 100)) # for 100 nm steps and starting point
        
#    k = 2.34 # N/m, spring constant
#    Amp = 5 # nm, this amplitude can be changed to calculate the drag force at any amplitude in the linear range
#    print(files[filenumber], '; peak force at 600 nm =', k/Qs[5]*Amp, 'nN')    
#    print(files[filenumber], '; peak force at 1000 nm =', k/Qs[11]*Amp, 'nN')  
    plt.plot(d,np.abs(1/Qs),'o')
    plt.xlabel('Insertion Length [nm]')
    plt.ylabel('1/Q')
#    plt.legend(list(files))
#plt.savefig('./figures/CFM_N100.png',dpi=300)


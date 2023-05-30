#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 13:23:41 2021

@author: danielchapman
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 14:53:25 2021

@author: danielchapman
"""

##############################################################################      
############################################################################## 
##############################################################################      
##############################################################################  

## THIS SCRIPT GET'S FEATURES FROM STEPH'S DATA TO IMPORT INTO EVALUATE     ##
## FUNCTION                                                                 ##
## code modified from bluebrain EFEL github                                 ##

##############################################################################      
############################################################################## 
##############################################################################      
##############################################################################

#%%
##############################################################################      
##############################################################################   
     
        ### Import Modules
        
##############################################################################      
############################################################################## 

import efel
# import csv
import numpy as np
import matplotlib.pyplot as plt 
import os 
import pyabf
import sys
sys.settrace

import faulthandler
faulthandler.enable()


#%%
#%%
##############################################################################      
##############################################################################   
     
        ### Define the function
        
##############################################################################      
############################################################################## 

def get_data(PathToFolder):
    '''
    Function get_Data
    Input: path to folder containing abf files for current clamp experiment
    Output: returns 22 features (tuple) from depolarizing current steps and their STDs
    
    Change stim start and stim end time indices to match the depolarizing 
    current step
    '''
    features = list()
    for file in os.listdir(PathToFolder):
        
        filename = os.fsdecode(file)


        if filename.endswith(".abf"): 
            # print(os.path.join(PathToFolder, filename))
            abf = pyabf.ABF(os.path.join(PathToFolder,filename))
            SweepCount = abf.sweepCount
            # convert to ms
            Time = abf.sweepX*1000
            
            # Throws segfualt if i don't do this plot 
            # abf.setSweep(0)
            # plt.plot(abf.sweepX,abf.sweepY)
            for i in range (0,SweepCount):   
                # setup trace for efel input 
                # setup stim parameters
                stim_start = 246.7
                stim_end = 646.7
                abf.setSweep(i)
                trace = {}
                trace['T'] = Time
                trace['V'] = abf.sweepY
                trace['stim_start'] = [stim_start]
                trace['stim_end'] = [stim_end]
                if i == 0:
                    traces = [trace]
                else:
                    traces.append(trace)
            features.append(efel.getMeanFeatureValues(traces,['steady_state_voltage_stimend',
                                     'steady_state_voltage','voltage_base',
                                     'decay_time_constant_after_stim','minimum_voltage',
                                     'sag_amplitude','sag_ratio1','sag_ratio2',
                                     'ohmic_input_resistance',
                                     'ohmic_input_resistance_vb_ssse']))
        else:
            continue
    steady_state_voltage_stimend = np.zeros([len(features),len(features[1])])
    steady_state_voltage = np.zeros([len(features),len(features[1])])
    decay_time_constant_after_stim = np.zeros([len(features),len(features[1])])
    minimum_voltage = np.zeros([len(features),len(features[1])])
    minimum_voltage = np.zeros([len(features),len(features[1])])
    sag_amplitude = np.zeros([len(features),len(features[1])])
    sag_ratio1 = np.zeros([len(features),len(features[1])])
    for g in range (0,len(features)):
        for c in range(0,len(features[g])):
            sag_ratio1[g,c] = features[g][c]['sag_ratio1']
            sag_amplitude[g,c] = features[g][c]['sag_amplitude']
            steady_state_voltage_stimend[g,c] = features[g][c]['steady_state_voltage_stimend']
            steady_state_voltage[g,c] = features[g][c]['steady_state_voltage']
            decay_time_constant_after_stim[g,c] = features[g][c]['decay_time_constant_after_stim']
            minimum_voltage[g,c] = features[g][c]['minimum_voltage']
        
    SSVSE = np.zeros([2,10])
    SSVSE[0,:] = np.mean(steady_state_voltage_stimend,axis=0)
    SSVSE[1,:] = np.std(steady_state_voltage_stimend,axis=0)
    
    SSV = np.zeros([2,10])
    SSV[0,:] = np.mean(steady_state_voltage,axis=0)
    SSV[1,:] = np.std(steady_state_voltage,axis=0)
    
    DTC = np.zeros([2,10])
    DTC[0,:] = np.mean(decay_time_constant_after_stim,axis=0)
    DTC[1,:] = np.std(decay_time_constant_after_stim,axis=0)
    
    MV = np.zeros([2,10])
    MV[0,:] = np.mean(minimum_voltage,axis=0)
    MV[1,:] = np.std(minimum_voltage,axis=0)
    
    SA = np.zeros([2,10])
    SA[0,:] = np.mean(sag_amplitude,axis=0)
    SA[1,:] = np.std(sag_amplitude,axis=0)
    
    return SSVSE,SSV,DTC,MV,SA
    # return minimum_voltage,sag_amplitude, sag_ratio1
        # voltage_deflection_vb_ssse
    
PathToFolder ='/Users/danielchapman/Desktop/StephCCDat/11.28.Run/ShamCC/' 
Sham = get_data(PathToFolder)
PathToFolder ='/Users/danielchapman/Desktop/StephCCDat/NoBMR/ShamNoBMR/' 
Hfhi = get_data(PathToFolder)

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
    Name = []
    for file in os.listdir(PathToFolder):
        
        filename = os.fsdecode(file)
        

        if filename.endswith(".abf"): 
            # print(os.path.join(PathToFolder, filename))
            Name.append(filename)
            abf = pyabf.ABF(os.path.join(PathToFolder,filename))
            SweepCount = abf.sweepCount
            # convert to ms
            Time = abf.sweepX*1000
            
            # Throws segfualt if i don't do this plot 
            abf.setSweep(9)
            # plt.plot(abf.sweepX,abf.sweepY)
            for i in range (0,SweepCount):   
                # setup trace for efel input 
                # setup stim parameters
                stim_start = 1640
                stim_end = 2040
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
            features.append(efel.getMeanFeatureValues(traces, ["Spikecount_stimint",
                                      "AP_amplitude_from_voltagebase",
                                      "voltage_base","AHP_depth_abs",
                                      "AHP_depth_abs_slow",
                                      "AHP_slow_time","AHP_depth",
                                      "AHP_time_from_peak",
                                      "AP_duration_half_width",
                                      "steady_state_voltage_stimend",
                                      "steady_state_voltage",
                                      "decay_time_constant_after_stim",
                                      "inv_time_to_first_spike",
                                      "inv_last_ISI","Spikecount",
                                      "inv_first_ISI","inv_second_ISI",
                                      "inv_third_ISI","inv_fourth_ISI",
                                      "AP_rise_rate",
                                      "AP_peak_downstroke",'AP_width','AP_peak_upstroke',
                                      'AP2_AP1_diff','AP_begin_voltage',
                                      'AP_phaseslope'
                                      ]))
        else:
            continue
    


    Spikecount = np.zeros([len(features),len(features[1])])
    Spikecount_stimint = np.zeros([len(features),len(features[1])])
    AP_amplitude = np.zeros([len(features),len(features[1])])
    voltage_base = np.zeros([len(features),len(features[1])])
    AHP_depth_abs = np.zeros([len(features),len(features[1])])
    AHP_depth_abs_slow = np.zeros([len(features),len(features[1])])
    AHP_slow_time = np.zeros([len(features),len(features[1])])
    AHP_depth = np.zeros([len(features),len(features[1])])
    AHP_time_from_peak = np.zeros([len(features),len(features[1])])
    AP_duration_half_width = np.zeros([len(features),len(features[1])])
    AP_width = np.zeros([len(features),len(features[1])])
    steady_state_voltage_stimend = np.zeros([len(features),len(features[1])])
    steady_state_voltage = np.zeros([len(features),len(features[1])])
    decay_time_constant_after_stim = np.zeros([len(features),len(features[1])])
    inv_time_to_first_spike = np.zeros([len(features),len(features[1])])
    inv_last_ISI = np.zeros([len(features),len(features[1])])
    inv_first_ISI = np.zeros([len(features),len(features[1])])
    inv_second_ISI = np.zeros([len(features),len(features[1])])
    inv_third_ISI = np.zeros([len(features),len(features[1])])
    inv_fourth_ISI = np.zeros([len(features),len(features[1])])
    AP_peak_upstroke = np.zeros([len(features),len(features[1])])
    AP_peak_downstroke = np.zeros([len(features),len(features[1])])
    AP_rise_time = np.zeros([len(features),len(features[1])])
    
    AP1_AP2_diff = np.zeros([len(features),len(features[1])])
    AP_begin_voltage = np.zeros([len(features),len(features[1])])
    
    AP_phaseslope = np.zeros([len(features),len(features[1])])
    
    for g in range (0,len(features)):
        for c in range(0,len(features[g])):
            # inv_time_to_first_spike[g,c] = features[g][c]['inv_time_to_first_spike']
            # inv_last_ISI[g,c] = features[g][c]['inv_last_ISI']
            Spikecount[g,c] = features[g][c]['Spikecount']
            Spikecount_stimint[g,c] = features[g][c]['Spikecount_stimint']
            
            if features[g][c]['AP_amplitude_from_voltagebase'] is None:
                AmpAv = 0
            else:
                AmpAv = np.mean(features[g][c]['AP_amplitude_from_voltagebase'])
            AP_amplitude[g,c] = AmpAv
            
            voltage_base[g,c] = features[g][c]['voltage_base']
            
            if features[g][c]['AHP_depth_abs'] is None:
                AHP_Av = 0
            else:
                AHP_Av = np.mean(features[g][c]['AHP_depth_abs'])
            AHP_depth_abs[g,c] = AHP_Av
            
            if features[g][c]['AHP_depth_abs_slow'] is None:
                AHP_Slow_Av = 0
            else:
                AHP_Slow_Av = np.mean(features[g][c]['AHP_depth_abs_slow'])
            AHP_depth_abs_slow[g,c] = AHP_Slow_Av
            
            if features[g][c]['AHP_slow_time'] is None:
                AHP_Slow_Time_Av = 0
            else:
                 AHP_Slow_Time_Av = np.mean(features[g][c]['AHP_slow_time'])
            AHP_slow_time[g,c] =  AHP_Slow_Time_Av
            
            if features[g][c]['AHP_depth'] is None:
                AHP_Depth_Av = 0
            else:
                AHP_Depth_Av = np.mean(features[g][c]['AHP_depth'])
            AHP_depth[g,c] = AHP_Depth_Av
            
            if features[g][c]['AHP_time_from_peak'] is None:
                AHP_TFP_Av = 0
            else:
                AHP_TFP_Av = np.mean(features[g][c]['AHP_time_from_peak'])
            AHP_time_from_peak[g,c] = AHP_TFP_Av
            
            if features[g][c]['AP_duration_half_width'] is None:
                AP_HW_Av = 0
            else:
                AP_HW_Av = np.mean(features[g][c]['AP_duration_half_width'])
            AP_duration_half_width[g,c] = AP_HW_Av
            
            
            try:
                AP_W_Av = np.mean(features[g][c]['AP_width'])
            except:
                AP_W_Av = 0
            
            if features[g][c]['AP2_AP1_diff'] is None:
                APDIFF = 0
                
            else:
                APDIFF = np.mean(features[g][c]['AP2_AP1_diff'])
            AP1_AP2_diff[g,c] = APDIFF
            
            
            
            if features[g][c]['AP_begin_voltage'] is None:
                APBEG = 0
                
            else:
                APBEG = np.mean(features[g][c]['AP_begin_voltage'])
            AP_begin_voltage[g,c] = APBEG
            
                
                
            # if features[g][c]['AP_width'] is None:
            #     AP_W_Av = 0
            # else:
            #     AP_W_Av = np.mean(features[g][c]['AP_width'])
            AP_width[g,c] = AP_W_Av
            
            if features[g][c]['inv_time_to_first_spike'] is None:
                IFS = 0
            else:
                IFS = np.mean(features[g][c]['inv_time_to_first_spike'])
            inv_time_to_first_spike[g,c] = IFS
            
            if features[g][c]['inv_last_ISI'] is None:
                ILS = 0
            else:
                ILS = np.mean(features[g][c]['inv_last_ISI'])
            inv_last_ISI[g,c] = ILS
            
            if features[g][c]['inv_first_ISI'] is None:
                IFIS = 0
            else:
                IFIS = np.mean(features[g][c]['inv_first_ISI'])
            inv_first_ISI[g,c] = IFIS
            
            if features[g][c]['inv_second_ISI'] is None:
                ISIS = 0
            else:
                ISIS = np.mean(features[g][c]['inv_second_ISI'])
            inv_second_ISI[g,c] = ISIS
            
            if features[g][c]['inv_third_ISI'] is None:
                ITIS = 0
            else:
                ITIS = np.mean(features[g][c]['inv_third_ISI'])
            inv_third_ISI[g,c] = ITIS

            if features[g][c]['inv_fourth_ISI'] is None:
                IFoIS = 0
            else:
                IFoIS = np.mean(features[g][c]['inv_fourth_ISI'])
            inv_fourth_ISI[g,c] = IFoIS
            
            if features[g][c]['AP_peak_upstroke'] is None:
                APUS = 0
            else:
                APUS = np.mean(features[g][c]['AP_peak_upstroke'])
            AP_peak_upstroke[g,c] = APUS
            
            if features[g][c]['AP_peak_downstroke'] is None:
                ADUS = 0
            else:
                ADUS = np.mean(features[g][c]['AP_peak_downstroke'])
            AP_peak_downstroke[g,c] = ADUS            
            
            if features[g][c]['AP_rise_rate'] is None:
                APRT = 0
            else:
                APRT = np.mean(features[g][c]['AP_rise_rate'])
            AP_rise_time[g,c] = APRT    
            
            
            if features[g][c]['AP_phaseslope'] is None:
                APPSlo = 0
            else:
                APPSlo = np.mean(features[g][c]['AP_phaseslope'])
            AP_phaseslope[g,c] = (features[g][c]['AP_phaseslope'])
            
            
            steady_state_voltage_stimend[g,c] = features[g][c]['steady_state_voltage_stimend']
            steady_state_voltage[g,c] = features[g][c]['steady_state_voltage']
            decay_time_constant_after_stim[g,c] = features[g][c]['decay_time_constant_after_stim']
    
    # now average everything across slice for each stim intensity and return that array
    SC = np.zeros([2,10])
    SC[0,:] = np.mean(Spikecount,axis=0)
    SC[1,:] = np.std(Spikecount,axis=0)
    
    SCSI = np.zeros([2,10])
    SCSI[0,:] = np.mean(Spikecount_stimint,axis=0)
    SCSI[1,:] = np.std(Spikecount_stimint,axis=0)
    
    AP_amp = np.zeros([2,10])
    AP_amp[0,:] = np.mean(AP_amplitude,axis=0)
    AP_amp[1,:] = np.std(AP_amplitude,axis=0)
    
    
    VB = np.zeros([2,10])
    VB[0,:] = np.mean(voltage_base,axis=0)
    VB[1,:] = np.std(voltage_base,axis=0)
    
    AHPDAbs = np.zeros([2,10])
    AHPDAbs[0,:] = np.mean(AHP_depth_abs,axis=0)
    AHPDAbs[1,:] = np.std(AHP_depth_abs,axis=0)
    
    AHPDAbslow = np.zeros([2,10])
    AHPDAbslow[0,:] = np.mean(AHP_depth_abs_slow,axis=0)
    AHPDAbslow[1,:] = np.std(AHP_depth_abs_slow,axis=0)
    
    AHPSlowT = np.zeros([2,10])
    AHPSlowT[0,:] = np.mean(AHP_slow_time,axis=0)
    AHPSlowT[1,:] = np.std(AHP_slow_time,axis=0)
    
    AHPD = np.zeros([2,10])
    AHPD[0,:] = np.mean(AHP_depth,axis=0)
    AHPD[1,:] = np.std(AHP_depth,axis=0)
    
    AHPTFP = np.zeros([2,10])
    AHPTFP[0,:] = np.mean(AHP_time_from_peak,axis=0)
    AHPTFP[1,:] = np.std(AHP_time_from_peak,axis=0)
    
    APHW = np.zeros([2,10])
    APHW[0,:] = np.mean(AP_duration_half_width,axis=0)
    APHW[1,:] = np.std(AP_duration_half_width,axis=0)
    
    print(type(APHW))
    
    APW = np.zeros([2,10])
    APW[0,:] = np.mean(AP_width,axis=0)
    APW[1,:] = np.std(AP_width,axis=0)
    
    print(type(APW))
    # print(APW)
    
    SSVSE = np.zeros([2,10])
    SSVSE[0,:] = np.mean(steady_state_voltage_stimend,axis=0)
    SSVSE[1,:] = np.std(steady_state_voltage_stimend,axis=0)
    
    SSV = np.zeros([2,10])
    SSV[0,:] = np.mean(steady_state_voltage,axis=0)
    SSV[1,:] = np.std(steady_state_voltage,axis=0)
    
    DTC = np.zeros([2,10])
    DTC[0,:] = np.mean(decay_time_constant_after_stim,axis=0)
    DTC[1,:] = np.std(decay_time_constant_after_stim,axis=0)
    
    # Interval to first spike
    ITFS = np.zeros([2,10])
    ITFS[0,:] = np.mean(inv_time_to_first_spike,axis=0)
    ITFS[1,:] = np.std(inv_time_to_first_spike,axis=0)
    
    # Interval to last spike
    ITLS = np.zeros([2,10])
    ITLS[0,:] = np.mean(inv_last_ISI,axis=0)
    ITLS[1,:] = np.std(inv_last_ISI,axis=0)
    
    # " " First spike
    IFIS = np.zeros([2,10])
    IFIS[0,:] = np.mean(inv_first_ISI,axis=0)
    IFIS[1,:] = np.std(inv_first_ISI,axis=0)
    
    # " " second spike
    ISIS = np.zeros([2,10])
    ISIS[0,:] = np.mean(inv_second_ISI,axis=0)
    ISIS[1,:] = np.std(inv_second_ISI,axis=0)  
    
    # " " Third spike
    ITIS = np.zeros([2,10])
    ITIS[0,:] = np.mean(inv_third_ISI,axis=0)
    ITIS[1,:] = np.std(inv_third_ISI,axis=0)  
    
    # " " fourth spike 
    IFoIS = np.zeros([2,10])
    IFoIS[0,:] = np.mean(inv_fourth_ISI,axis=0)
    IFoIS[1,:] = np.std(inv_fourth_ISI,axis=0)  
    
    # AP upstroke
    APUS = np.zeros([2,10])
    APUS[0,:] = np.mean(AP_peak_upstroke,axis=0)
    APUS[1,:] = np.std(AP_peak_upstroke,axis=0)        
    
    # # AP downstroke
    ADUS = np.zeros([2,10])
    ADUS[0,:] = np.mean(AP_peak_downstroke,axis=0)
    ADUS[1,:] = np.std(AP_peak_downstroke,axis=0)               
        
    # AP rise time 
    APRT = np.zeros([2,10])
    APRT[0,:] = np.mean(AP_rise_time,axis=0)
    APRT[1,:] = np.std(AP_rise_time,axis=0)
    print(APRT)
    
    # print('blahhhhhHHHHHHHHH')
    print(AP1_AP2_diff)
    AP_diff = np.zeros([2,10])
    AP_diff[0,:] = np.mean(AP1_AP2_diff,axis=0)
    AP_diff[1,:] = np.std(AP1_AP2_diff,axis=0)
    
    AP_beg = np.zeros([2,10])
    AP_beg[0,:] = np.mean(AP_begin_voltage,axis=0)
    AP_beg[1,:] = np.std(AP_begin_voltage,axis=0)
    
    APPS = np.zeros([2,10])
    APPS[0,:] = np.mean(AP_phaseslope,axis=0)
    APPS[1,:] = np.std(AP_phaseslope,axis=0)


    print('GET DATA DONE %%%%%%%%%%%%%%%%')
    return SC,SCSI, AP_amp, VB, AHPDAbs, AHPDAbslow, AHPSlowT, AHPD, AHPTFP,\
    APHW, APW, SSVSE, SSV, DTC,APUS,APRT,ADUS, AP_diff,AP_beg,APPS
# 
    # return features
    
    # return Spikecount,Spikecount_stimint,\
    # AP_amplitude, voltage_base,AHP_depth_abs,\
    # AHP_depth_abs_slow,AHP_slow_time,AHP_depth,AHP_time_from_peak,\
    # AP_duration_half_width, AP_width,steady_state_voltage_stimend,\
    # steady_state_voltage, decay_time_constant_after_stim, Name


#AHPDAbs

PathToFolder ='/Users/danielchapman/Desktop/StephCCDat/11.28.Run/ShamCC/' 

PathToFolderN = '/Users/danielchapman/Desktop/StephCCDat/11.28.Run/HFHICC/'

Sham = get_data(PathToFolder)
HFHI = get_data(PathToFolderN)

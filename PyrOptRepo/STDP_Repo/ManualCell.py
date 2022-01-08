#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 18:41:13 2022

@author: danielchapman
"""
%matplotlib inline
import matplotlib.pyplot as plt
%reload_ext autoreload
%autoreload

import matplotlib.pyplot as plt


import os

import bluepyopt as bpopt
import bluepyopt.ephys as ephys

# NEURON simulator
nrn_sim = ephys.simulators.NrnSimulator()

# Single compartment
morph = ephys.morphologies.NrnFileMorphology('morphology/fx_CA1_8.CNG.swc',
                                                  do_replace_axon=True)

# Object that points to sectionlist somatic
somatic_loc = ephys.locations.NrnSeclistLocation('somatic',seclist_name='somatic')
all_loc = ephys.locations.NrnSeclistLocation('all',seclist_name='all')

# Object that points to the center of the soma
somacenter_loc = ephys.locations.NrnSeclistCompLocation(
    name='somacenter',
    seclist_name='somatic',
    sec_index=0,
    comp_x=0.5)

pas_mech = ephys.mechanisms.NrnMODMechanism(                                    
    name='pas',                                                                 
    suffix='pas',                                                               
    locations=[all_loc])  

cm_param = ephys.parameters.NrnSectionParameter(
        name='cm',
        param_name='cm',
        value=1.2,
        locations=[all_loc],
        frozen=True)
Parameters = []
Parameters.append(cm_param)

g_pas_param = ephys.parameters.NrnSectionParameter(
        name='g_pas',
        param_name='g_pas',
        value=3e-05,
        locations=[all_loc],
        frozen=True)

Parameters.append(g_pas_param)

e_pas_param = ephys.parameters.NrnSectionParameter(
        name='e_pas',
        param_name='e_pas',
        value=-70,
        locations=[all_loc],
        frozen=True)

Parameters.append(e_pas_param)

Ra_param = ephys.parameters.NrnSectionParameter(
        name='Ra',
        param_name='Ra',
        value=100,
        locations=[all_loc],
        frozen=True)

Parameters.append(Ra_param)

Temp_param = ephys.parameters.NrnGlobalParameter(
    name='celsius',
    param_name='celsius',
    frozen=True,
    value=20)

Parameters.append(Temp_param)

init_param = ephys.parameters.NrnGlobalParameter(
    name='v_init',
    param_name='v_init',
    frozen=True,
    value=-70)

Parameters.append(init_param)











expsyn_mech = ephys.mechanisms.NrnMODPointProcessMechanism(                     
    name='expsyn',                                                              
    suffix='ExpSyn',                                                            
    locations=[somacenter_loc])

expsyn_loc = ephys.locations.NrnPointProcessLocation(                           
    'expsyn_loc',                                                               
    pprocess_mech=expsyn_mech) 

expsyn_tau_param = ephys.parameters.NrnPointProcessParameter(                   
    name='expsyn_tau',                                                          
    param_name='tau',                                                           
    value=2,                                                                    
    bounds=[0, 50],                                                             
    locations=[expsyn_loc])

Parameters.append(expsyn_tau_param)









cell = ephys.models.CellModel(                                               
    name='simple_cell',                                                      
    morph=morph,                                                             
    mechs=[pas_mech,expsyn_mech],                                           
    params=Parameters) 
print(cell)

               

#%%

stim_start = 20
number = 5
interval = 5

netstim = ephys.stimuli.NrnNetStimStimulus(                                  
    total_duration=200,                                                      
    number=5,                                                                
    interval=5,                                                              
    start=stim_start,                                                        
    weight=5e-4,                                                             
    locations=[expsyn_loc])

stim_end = stim_start + interval * number

rec = ephys.recordings.CompRecording(
    name='soma.v', 
    location=somacenter_loc,
    variable='v')

protocol = ephys.protocols.SweepProtocol('netstim_protocol', [netstim], [rec])




max_volt_feature = ephys.efeatures.eFELFeature(                              
    'maximum_voltage',                                                       
    efel_feature_name='maximum_voltage',                                     
    recording_names={'': 'soma.v'},                                          
    stim_start=stim_start,                                                   
    stim_end=stim_end,                                                       
    exp_mean=-50,                                                            
    exp_std=.1)

max_volt_objective = ephys.objectives.SingletonObjective(                    
    max_volt_feature.name,                                                   
    max_volt_feature)                       

score_calc = ephys.objectivescalculators.ObjectivesCalculator(               
    [max_volt_objective])                                                    

cell_evaluator = ephys.evaluators.CellEvaluator(                             
    cell_model=cell,                                                         
    param_names=['expsyn_tau'],                                              
    fitness_protocols={protocol.name: protocol},                             
    fitness_calculator=score_calc,                                           
    sim=nrn_sim)      

#%%
release_params = {
    'expsyn_tau':2

}

responses = protocol.run(                                                    
    cell_model=cell,                                                         
    param_values=release_params,                                              
    sim=nrn_sim)                                                             

time = responses['soma.v']['time']                                           
voltage = responses['soma.v']['voltage']                                     

import matplotlib.pyplot as plt                                              
plt.style.use('ggplot')                                                      
plt.plot(time, voltage)                                                      
plt.xlabel('Time (ms)')                                                      
plt.ylabel('Voltage (mV)')                                                   
plt.show()      



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 16:22:46 2021

@author: danielchapman
"""
##############################################################################
##############################################################################
##############################################################################

# load necessary modules

##############################################################################
##############################################################################
##############################################################################

import numpy as np
import argparse
import os
import sys
import textwrap
from datetime import datetime
import bluepyopt as bpopt
import bluepyopt.ephys as ephys
import Ball_evaluator
import matplotlib.pyplot as plt
import pprint
pp = pprint.PrettyPrinter(indent=2)
import logging                                                                      
logging.basicConfig()                                                               
logger = logging.getLogger()                                                        
logger.setLevel(logging.DEBUG)

# !nrnivmodl mechanisms


#%%
##############################################################################
##############################################################################
##############################################################################

# Let's import the morphology, can uncommment neurom lines for visualization

##############################################################################
##############################################################################
##############################################################################

# import neurom.viewer
# neurom.viewer.draw(neurom.load_neuron('morphology/fx_CA1_8.CNG.swc'));

morphology = ephys.morphologies.NrnFileMorphology('morphology/fx_CA1_8.CNG.swc',
                                                  do_replace_axon=True)

# Morph taken from 
# http://neuromorpho.org/MorphometryBrowseView.jsp?MS11=measurements&MS12=neuro
# n_id&MS13=Operator:=&MS14=60522&MS21=measurements&MS22=&MS23=Operator:=&MS24
# =&MS31=measurements&MS32=&MS33=Operator:=&MS34=&MS41=measurements&MS42=&MS43
# =Operator:=&MS44=&MS51=measurements&MS52=&MS53=Operator:=&MS54=&MS61
# =measurements&MS62=&MS63=Operator:like&MS64=&browseBy=1

#%%
##############################################################################
##############################################################################
##############################################################################

# Load the parameters and mechanisms as done before from L5pc example but let's
# appnd on the expsyn mechanism and parameter and then create the cell

##############################################################################
##############################################################################
##############################################################################

# NOW LETS MAKE THE PARAMETERS AND CHANGE THE MECHANISM    
import json
param_configs = json.load(open('config/parameters.json'))
# param_configs = json.load(open('config/parameters.json'))
# print([param_config['param_name'] for param_config in param_configs])

# The directory that contains this notebook has a module that will load all 
# the parameters in BluePyOpt Parameter objects

import Ball_model
parameters = Ball_model.define_parameters()
# print('\n'.join('%s' % param for param in parameters))

##%%
# We also need to add all the necessary mechanisms, like ion channels to the 
# model. The configuration of the mechanisms is also stored in a json file, 
# and can be loaded in a similar way

mechanisms = Ball_model.define_mechanisms()

somatic_loc = ephys.locations.NrnSeclistLocation('somatic',
    seclist_name='somatic')

somacenter_loc = ephys.locations.NrnSeclistCompLocation(
    name='somacenter',
    seclist_name='somatic',
    sec_index=0,
    comp_x=0.5)  

# Add ExpSyn synapse pointprocess at the center of the soma
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
mechanisms.append(expsyn_mech)
parameters.append(expsyn_tau_param)
# print('\n'.join('%s' % mech for mech in mechanisms))

# With the morphology, mechanisms and parameters we can build the cell model
Ball_cell = ephys.models.CellModel('Ball', morph=morphology,
    mechs=mechanisms, params=parameters)
# print(Ball_cell)


# For use in the cell evaluator later, we need to make a list of the name of 
# the parameters we are going to optimise. These are the parameters that are
# not frozen.
param_names = [param.name for param in Ball_cell.params.values()
    if not param.frozen]

#%%
##############################################################################
##############################################################################
##############################################################################

# Make the protocol for the netstim

##############################################################################
##############################################################################
##############################################################################

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


sim = ephys.simulators.NrnSimulator()

evaluator = ephys.evaluators.CellEvaluator(                                          
        cell_model=Ball_cell,                                                       
        param_names=param_names,                                                    
        fitness_protocols=protocol,                                        
        fitness_calculator=score_calc,                                      
        sim=sim)

#%%
##############################################################################
##############################################################################
##############################################################################

# Load good parameter values from the optimization and run the sweep

##############################################################################
##############################################################################
##############################################################################

import csv
with open('/Users/danielchapman/Desktop/PyrOptResults/12.21_Run/HFHI/1000MSGenTestHofParams.csv', newline='') as csvfile:
  Good_params = np.loadtxt(csvfile, delimiter=",")

# This evaluator can be used to run the protocols. 
Model_Num = 8
# Sham : 3, 7, 13,16,17, 18
# HFHI: 6, 8*, 11,13, 15 (low spike), 17, 18 (high spike),19
release_params = {
    'gkdrbar_kdr.somatic': Good_params[0,Model_Num],
    'gbar_nax.somatic': Good_params[1,Model_Num],
    'gkabar_kap.somatic':Good_params[2,Model_Num],
    'gcalbar_cal.somatic':Good_params[3,Model_Num],
    'gcanbar_can.somatic':Good_params[4,Model_Num],
    'gcatbar_cat.somatic':Good_params[5,Model_Num],
    'ghdbar_hd.somatic':Good_params[6,Model_Num],
    'gbar_kca.somatic':Good_params[7,Model_Num],
    'gbar_kmb.somatic': Good_params[8,Model_Num],
    'gbar_cagk.somatic':Good_params[9,Model_Num],
    'expsyn_tau': 2
}


release_responses = protocol.run(                                                    
    cell_model=Ball_cell,                                                         
    param_values=release_params,                                              
    sim=sim) 

#%%
##############################################################################
##############################################################################
##############################################################################

# Plot responses 

##############################################################################
##############################################################################
##############################################################################

# We can now plot all the responses
# def plot_responses(responses):
#     fig, axes = plt.subplots(len(responses), figsize=(10,10))
#     for index, (resp_name, response) in enumerate(sorted(responses.items())):
#         axes[index].plot(response['time'], response['voltage'], label=resp_name)
#         axes[index].set_title(resp_name)
#     fig.tight_layout()
#     fig.show()
#     # fig.savefig('Blah')
# plot_responses(release_responses)

fig = plt.plot(release_responses['soma.v']['time'],
                release_responses['soma.v']['voltage'],
                linewidth = 0.5)
# plt.ylim(top = 40)
# plt.ylim(bottom = -80)
plt.xlabel('Time (ms)',fontsize=20)
plt.ylabel('Voltage (mV)',fontsize=20)
plt.show()

# # plt.savefig('Blah')
# print('Finished')
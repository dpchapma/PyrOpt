#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 16:22:46 2021

@author: danielchapman
"""
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

#%%
# Let's import just the simple cell morphology and create one section for the soma 

# import neurom.viewer
# neurom.viewer.draw(neurom.load_neuron('morphology/fx_CA1_8.CNG.swc'));


morphology = ephys.morphologies.NrnFileMorphology('morphology/fx_CA1_8.CNG.swc',
                                                  do_replace_axon=True)
# morphology = ephys.morphologies.NrnFileMorphology('morphology/Mouse-CA1-Pyramidal-Cell.CNG.swc',
#                                                       do_replace_axon=True)
# morphology = ephys.morphologies.NrnFileMorphology('morphology/fx_CA1_8.CNG.swc',
                                                  # do_replace_axon=True)
# Morph taken from 
# http://neuromorpho.org/MorphometryBrowseView.jsp?MS11=measurements&MS12=neuron
# _id&MS13=Operator:=&MS14=60522&MS21=measurements&MS22=&MS23=Operator:=&MS24
# =&MS31=measurements&MS32=&MS33=Operator:=&MS34=&MS41=measurements&MS42=&MS43
# =Operator:=&MS44=&MS51=measurements&MS52=&MS53=Operator:=&MS54=&MS61
# =measurements&MS62=&MS63=Operator:like&MS64=&browseBy=1

#%%
# # Since we have many parameters in this model, they are stored in a json file:

# NOW LETS MAKE THE PARAMETERS AND CHANGE THE MECHANISM    
import json
param_configs = json.load(open('config/parameters.json'))
# param_configs = json.load(open('config/parameters.json'))
# print([param_config['param_name'] for param_config in param_configs])

# #%%
# # The directory that contains this notebook has a module that will load all 
# # the parameters in BluePyOpt Parameter objects

import Ball_model
parameters = Ball_model.define_parameters()
# print('\n'.join('%s' % param for param in parameters))

# #%%
# # We also need to add all the necessary mechanisms, like ion channels to the 
# # model. The configuration of the mechanisms is also stored in a json file, 
# # and can be loaded in a similar way

mechanisms = Ball_model.define_mechanisms()
# print('\n'.join('%s' % mech for mech in mechanisms))

# #%%
# # With the morphology, mechanisms and parameters we can build the cell model

Ball_cell = ephys.models.CellModel('Ball', morph=morphology, mechs=mechanisms, params=parameters)
# print(Ball_cell)

# #%% 
# # For use in the cell evaluator later, we need to make a list of the name of 
# # the parameters we are going to optimise. These are the parameters that are not frozen.

param_names = [param.name for param in Ball_cell.params.values() if not param.frozen]

# #%%
# Now that we have a cell model, we can apply protocols to it. The protocols 
# are also stored in a json file.

proto_configs = json.load(open('config/protocols.json'))
# proto_configs = json.load(open('config/protocols.json'))
# print(proto_configs)

# #%%
# And they can be automatically loaded

fitness_protocols = Ball_evaluator.define_protocols()
# print('\n'.join('%s' % protocol for protocol in fitness_protocols.values()))

# #%%
# For every protocol we need to define which eFeatures will be used as 
# objectives of the optimisation algorithm.

feature_configs = json.load(open('config/features.json'))
# feature_configs = json.load(open('config/features.json'))
# print(feature_configs)

# #%%
# Fitness
fitness_calculator = Ball_evaluator.define_fitness_calculator(fitness_protocols)
# print(fitness_calculator)

# #%%
# We need to define which simulator we will use. In this case it will be 
# Neuron, i.e. the NrnSimulator class

sim = ephys.simulators.NrnSimulator()

## %%
## With all the components defined above we can build a cell evaluator

evaluator = ephys.evaluators.CellEvaluator(                                          
        cell_model=Ball_cell,                                                       
        param_names=param_names,                                                    
        fitness_protocols=fitness_protocols,                                        
        fitness_calculator=fitness_calculator,                                      
        sim=sim)

#%%

import csv
with open('/Users/danielchapman/Desktop/PyrOptResults/NoBMR_Run/HFHI/1000MSGenTestHofParams.csv', newline='') as csvfile:
  Good_params = np.loadtxt(csvfile, delimiter=",")

#%%
# This evaluator can be used to run the protocols. 
Model_Num = 75
# Sham : 3, 52
# HFHI: 3, 17
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
    'gbar_cagk.somatic':Good_params[9,Model_Num]
}

## %%
# Running the responses is as easy as passing the protocols and parameters to 
# the evaluator. (The line below will take some time to execute)
release_responses = evaluator.run_protocols(protocols=fitness_protocols.values(),
                                            param_values=release_params)

##%%
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


fig = plt.plot(release_responses['Step9.soma.v']['time'],
               release_responses['Step9.soma.v']['voltage'],
               linewidth = 3)
plt.ylim(top = 40)
plt.ylim(bottom = -80)
plt.xlim(0,1000)
plt.xlabel('Time (ms)',fontsize=20)
plt.ylabel('Voltage (mV)',fontsize=20)
# plt.axis('off')
plt.show()
plt.savefig('HFHI_75.png',dpi=300)

# plt.savefig('Blah')
print('Finished')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
Copyright (c) 2016-2020, EPFL/Blue Brain Project

 This file is part of BluePyOpt <https://github.com/BlueBrain/BluePyOpt>

 This library is free software; you can redistribute it and/or modify it under
 the terms of the GNU Lesser General Public License version 3.0 as published
 by the Free Software Foundation.

 This library is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 details.

 You should have received a copy of the GNU Lesser General Public License
 along with this library; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
"""
Created on Tue Jul 13 20:05:21 2021

@author: danielchapman
"""

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
# Let's import just the simple cell morphology and create one section for the soma uncomment if you want to look at morphology

# import neurom.viewer
# neurom.viewer.draw(neurom.load_neuron('morphology/fx_CA1_8.CNG.swc'));
# neurom.viewer.draw(neurom.load_neuron('/Users/danielchapman/Desktop/PyrOpt/morphology/Mouse-CA1-Pyramidal-Cell.CNG.swc'));

#%%
def main():

    # Morph taken from
    # http://neuromorpho.org/MorphometryBrowseView.jsp?MS11=measurements&MS12=neuron
    # _id&MS13=Operator:=&MS14=60522&MS21=measurements&MS22=&MS23=Operator:=&MS24
    # =&MS31=measurements&MS32=&MS33=Operator:=&MS34=&MS41=measurements&MS42=&MS43
    # =Operator:=&MS44=&MS51=measurements&MS52=&MS53=Operator:=&MS54=&MS61
    # =measurements&MS62=&MS63=Operator:like&MS64=&browseBy=1

    morphology = ephys.morphologies.NrnFileMorphology('PyrOpt/morphology/fx_CA1_8.CNG.swc',
                                                       do_replace_axon=True)

    
    #%%
    # # Since we have many parameters in this model, they are stored in a json file:
    
    # NOW LETS MAKE THE PARAMETERS AND CHANGE THE MECHANISM    
    import json
    param_configs = json.load(open('PyrOpt/config/parameters.json'))
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
    proto_configs = json.load(open('PyrOpt/config/protocols.json'))
    # proto_configs = json.load(open('config/protocols.json'))
    # print(proto_configs)
    
    # #%%
    # And they can be automatically loaded
    fitness_protocols = Ball_evaluator.define_protocols()
    # print('\n'.join('%s' % protocol for protocol in fitness_protocols.values()))
    
    # #%%
    # For every protocol we need to define which eFeatures will be used as 
    # objectives of the optimisation algorithm.
    feature_configs = json.load(open('PyrOpt/config/features.json'))
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
    
    # %%
    # This evaluator can be used to run the protocols. 
    # release_params = {
    #     'gkdrbar_kdr.somatic': 0.0609,
    #     'gbar_nax.somatic': 0.1,
    #     'gkabar_kap.somatic':0.1,
    #     'gcalbar_cal.somatic':0.000001,
    #     'gcalbar_can.somatic':0.000001,
    #     'gcatbar_cat.somatic':0.000001,
    #     'gbar_h.somatic':0.0001,
    #     'gbar_kdBG.somatic':0.0001,
    #     'gbar_km.somatic':0.00001,
    #     'gbar_kca.somatic':0.00001,
    #     'gkbar_mykca.somatic':0.00001
    # }
    
    # #%%
    # # Running the responses is as easy as passing the protocols and parameters to 
    # # the evaluator. (The line below will take some time to execute)
    # release_responses = evaluator.run_protocols(protocols=fitness_protocols.values(),
    #                                             param_values=release_params)
    
    # #%%
    # # We can now plot all the responses
    # def plot_responses(responses):
    #     fig, axes = plt.subplots(len(responses), figsize=(10,10))
    #     for index, (resp_name, response) in enumerate(sorted(responses.items())):
    #         axes[index].plot(response['time'], response['voltage'], label=resp_name)
    #         axes[index].set_title(resp_name)
    #     fig.tight_layout()
    #     fig.show()
    # plot_responses(release_responses)
    
    #%%
    # Run the optimiazation
    import random
    Rand = random.randint(1,50)
    random.seed(Rand)
    
    map_function = None
    
    opt = bpopt.deapext.optimisations.NSDEwFeatCrowdOptimisation(use_scoop=(True),
                  evaluator=evaluator,
                  map_function=map_function,
                  seed=random.seed(Rand),
                  cxpb=1.0,
                  jitter=0.1,
                  numSDs=2,offspring_size=96
              )
    
    final_pop, halloffame, log, hist = opt.run(max_ngen=1000, 
                                                cp_filename='PyrOpt/checkpoints/checkpoint.pkl')
    # final_pop, halloffame, log, hist = opt.run(max_ngen=5, 
    #                                             cp_filename='checkpoints/checkpoint.pkl')
    
    #%%
    Num_Features = 30
    Num_Params = 10
    import numpy as np
    hofparams = np.empty([Num_Params,len(halloffame)])
    hofFeatures = np.empty([Num_Features,len(halloffame)])
    hofError = np.empty([Num_Features,len(halloffame)])
    for i in range(0,len(halloffame)):
        hofparams[0:Num_Params,i] = halloffame[i]
        hofError[0:Num_Features,i] = halloffame.keys[i].values
        values = halloffame.keys[i].feature_values.values()
        values_list = list(values)
        ValueOrder = list(halloffame.keys[i].feature_values)
        for c in range(0,len(values_list)):
            NameTemp = list(values_list[c])    
            feature_value = list(values_list[c].values())
            hofFeatures[c,i] = feature_value[0]
    
    
    #%%
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'Results')
    import csv
    
    with open('FeatureValueOrder.csv', 'w') as filehandle:
        for listitem in ValueOrder:
            filehandle.write('%s\n' % listitem)
        
    #%%
    np.savetxt("1000MSGenTestHofParams.csv",hofparams,delimiter=",")
    np.savetxt("1000MSGenTestHofError.csv",hofError,delimiter=",")
    np.savetxt("1000MSGenTestHofFeatures.csv",hofFeatures,delimiter=",")


#%% 
if __name__ == '__main__':
    main()


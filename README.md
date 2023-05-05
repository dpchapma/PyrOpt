# PyrOpt
Pyramidal cell modeling optimization and current clamp frequency analysis for paper "Single neuron modeling identifies potassium 
channel modulation as potential target for repetitive head impacts" under review at Neuroinformatics

PyrOptRepo contains directory for running optimization on current clamp data. Data is taken from "High-frequency head impact causes 
chronic synaptic adaptation and long-term cognitive impairment in mice" published in Nature Communications in 2021. 8 cells from 
HFHI and Sham animals were used for data and extracted mean & SD are in the "Features" Json file. 

Code is optimized for running on cloud based HPC. The file Long_Slurm_Run will run the optimization in parallel.

Matlab code in the top level is for analysis. Run_Script.mlx runs code and prompts user to a folder for both Sham and then HFHI .csv output
from optimization code. 


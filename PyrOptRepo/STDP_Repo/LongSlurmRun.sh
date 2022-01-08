#!/bin/bash -l
#SBATCH --job-name="PyrOpt"
#SBATCH --output="%x.o%j"
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --cpus-per-task=1
#SBATCH --time=120:00:00
#SBATCH --mem=5G
#SBATCH --mail-user=dpc53@georgetown.edu
#SBATCH --mail-type=END,FAILqk


# Following code taken from https://ulhpc-tutorials.readthedocs.io/en/latest/python/
# advanced/scoop-deap/
# Ensure process affinity is disabled
export SLURM_CPU_BIND=none

# Prepare in the current folder a worker launcher for Scoop 
# The scipt below will 'decorate' the python interpreter command
# Before python is called, modules are loaded
HOSTFILE=$(pwd)/hostfile
SCOOP_WRAPPER=$(pwd)/scoop-python.sh

cat << EOF > $SCOOP_WRAPPER
#!/bin/bash -l
module load anaconda3
export SLURM_NTASKS=${SLURM_NTASKS}
source $(pwd)/test_env/bin/activate
EOF
echo 'python $@' >> $SCOOP_WRAPPER

chmod +x $SCOOP_WRAPPER

# Classical "module load" in the main script
module load anaconda3
source $(pwd)/test_env/bin/activate

# Save the hostname of the allocated nodes
scontrol show hostnames > $HOSTFILE

# Start scoop with python input script
INPUTFILE=$(pwd)/PyrOpt/BallAndStick_opt.py
python -m scoop --hostfile $HOSTFILE -n ${SLURM_NTASKS} --python-interpreter=$SCOOP_WRAPPER $INPUTFILE $@

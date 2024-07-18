#!/bin/bash

# Base script generated by NERSC Batch Script Generator on https://iris.nersc.gov/jobscript.html

#SBATCH -N 4
#SBATCH -C cpu
#SBATCH -q regular
#SBATCH -J ilamb
#SBATCH --mail-user=nathaniel.collier@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -A m2467
#SBATCH -t 4:00:0

# OpenMP settings:
export OMP_NUM_THREADS=1
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

# ILAMB setup:
export ILAMB_ROOT=/global/homes/n/nate/m2467/nate
module load python/3.11
conda activate ilamb

#run the application:
srun -n 16 -c 64 --cpu_bind=cores  ilamb-run \
     --config ilamb.cfg \
     --model_setup models_e3sm.yaml \
     --define_regions ${ILAMB_ROOT}/DATA/regions/GlobalLand.nc ${ILAMB_ROOT}/DATA/regions/LandRegions.nc regions.txt \
     --regions global southamericaamazon eqas eqaf hilat \
     --rmse_score_basis cycle \
     --title "esm-hist and E3SM" \
     --build_dir _build_esmhist
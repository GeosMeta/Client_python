#!/bin/bash
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --partition serial
#SBATCH --qos serial
#SBATCH --mem=4G
#SBATCH --tasks-per-node=1
#SBATCH --account=n02-optclim
. ~/setup_optclim2.sh
GMTOP=/work/n02/shared/mjmn02/geosmeta/GeosMetaClient_python/clientpy3

export PYTHONPATH=$PYTHONPATH:$GMTOP:$GMTOP/geosmeta
export PATH=$PATH:$GMTOP/bin


cd /work/n02/shared/mjmn02/geosmeta/GeosMetaClient_python/gm_tests

python testApp1.py A2_sb_$$

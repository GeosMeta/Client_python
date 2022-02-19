#!/bin/bash

# interim way to set environemnt for geosmeta tests using dataastore
# to hold the  client software
# This might be used from desktop, Burn or Eddie3 (but not Eddie2)

if [[ $HOSTNAME == *'geos'* ]]
 then
 echo $HOSTNAME
   #MINI
#   source activate gm_py36_1 # clim_py36_1
   PATH=/scratch/mjm/miniconda/gm_py36_1/bin/:$PATH
   GMTOP=/exports/csce/datastore/geos/groups/cesd/GeosMeta/clientpy3
   # default python is ok on Burn
elif [[ $HOSTNAME == "login"*"ecdf"* ]]
then
   echo eddie3 login node
   module load anaconda
   source activate cesd_clim_1   # is this needed? Or just if its used then needs to coexist happily
   GMTOP=/exports/csce/eddie/geos/groups/cesd/MOfficer/geosmetaclient
elif [[ $HOSTNAME == *"ecdf"* ]]
then
   echo eddie3 worker node
   module load anaconda
   source activate cesd_clim_1   # is this needed? Or just if its used then needs to coexist happily
   GMTOP=/exports/csce/eddie/geos/groups/cesd/MOfficer/geosmetaclient
elif [[ $HOSTNAME == *"ceda"* ]]
then
   echo jasmin
   GMTOP=/home/users/mmineter/geosmetaclient
elif [[ $HOSTNAME == "ln"* ]]
then
   echo archer2 login node
   GMTOP=/work/n02/shared/mjmn02/geosmeta/GeosMetaClient_python/clientpy3
elif [[ $HOSTNAME == "dn"* ]]
then
   echo archer2 serial node
   GMTOP=/work/n02/shared/mjmn02/geosmeta/GeosMetaClient_python/clientpy3
fi

export PYTHONPATH=$PYTHONPATH:$GMTOP:$GMTOP/geosmeta
export PATH=$PATH:$GMTOP/bin


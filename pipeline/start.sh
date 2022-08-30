#!/bin/bash

BASEDIR=$(dirname "BASH_SOURCE")
cd $BASEDIR
echo "Start ..."

# The raw data originally is stored as .zip files,
# 
echo "Step 1: Extract flight trajectories from raw data..."
python 1_extract.py

echo "Step 2: Clean up extracted trajectory data..."
python 2_filter.py

echo "Step 3: Compute statistics from fixed entry ring..."
python 3_stat_fixed_distance.py

echo "Step 4: Compute distances..."
python 4_distance_time_curves.py


echo "All done!!"

#!/bin/bash

tar xvfz nsides_scripts.tgz

# Run the scripts
python prepare_data_osg.py --model-number $1 | tee prepare_data.log
tar cvfz data_$1.tgz model*.mtx model*.npy *.log *.py

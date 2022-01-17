#!/bin/bash
for f in ./CombinedTempFiles/*2e2mu*.root
do
    python DataCardmaker.py $f
done
    
    

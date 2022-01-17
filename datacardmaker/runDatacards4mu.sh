#!/bin/bash
for f in ./CombinedTempFiles/*4mu*.root
do
    python DataCardmaker.py $f
done
    
    

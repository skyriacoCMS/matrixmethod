#!/bin/bash
for f in ./CombinedTempFiles/*4e*.root
do
    python DataCardmaker.py $f
done
    
    

#!/bin/sh

for i in {21..25}; do
    mkdir $i
    cp template.py $i/main.py
    touch $i/test.txt
    touch $i/input.txt
done

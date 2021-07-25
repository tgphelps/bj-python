#!/bin/bash

rm stats.txt
./bj.py -v -r  -n 50 -s 2    data/house.cfg $1
./summary_stats.py

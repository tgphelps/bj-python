#!/bin/bash

# Use this to compare trace.txt to good-trace.txt
# WARNING: Use 25% cut card
rm stats.txt
./bj.py  -l -r  -n 500000 -s 2    data/house.cfg $1
./summary_stats.py

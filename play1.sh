#!/bin/bash

rm stats.txt
./bj.py -v  -n 2 -s 2    data/house.cfg $1
./summary_stats.py

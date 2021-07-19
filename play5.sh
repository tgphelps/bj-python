#!/bin/bash

rm stats.txt
./bj.py -v -t  -n 1 -s 5    data/house.cfg $1
./summary_stats.py

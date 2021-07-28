#!/bin/bash

rm stats.txt
./bj.py  -l    -n 2000 -s 5    data/house.cfg $1
./summary_stats.py

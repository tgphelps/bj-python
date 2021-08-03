#!/bin/bash

rm stats.txt
./bj.py  -l --ins 3  -n 10000 -s 1    data/house.cfg $1
./summary_stats.py

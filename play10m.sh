#!/bin/bash

rm stats.txt
for x in {1..10} ; do
  ./bj.py        -n 200000 -s 5    data/house.cfg $1
  echo $x million
done
./summary_stats.py

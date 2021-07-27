#!/bin/bash

echo This deals RANDOM cards

if [ $1 = "-s" ] ; then
    shift
    rm stats.txt
    echo NEW stats file
fi
for x in 2 4 6 8 10 ; do
  ./bj.py        -n 400000 -s 5    data/house.cfg $1
  echo $x million
  echo
  ./summary_stats.py
done

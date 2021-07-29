#!/bin/bash

echo This deals RANDOM cards

if [ $1 = "-s" ] ; then
    shift
    rm stats.txt
    echo NEW stats file
fi

BET=1
if [ $1 = "-b" ] ; then
    shift
    BET=$1
    shift
fi

for x in 2 4 6 8 10 ; do
  ./bj.py  -b $BET   -n 400000 -s 5    data/house.cfg $1
  echo $x million
  echo
  ./summary_stats.py
done

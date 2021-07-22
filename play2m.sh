#!/bin/sh

echo This deals RANDOM cards

if [ $1 = "-s" ] ; then
    shift
    rm stats.txt
    echo NEW stats file
fi

./bj.py      -n 400000 -s 5    data/house.cfg $1
./summary_stats.py

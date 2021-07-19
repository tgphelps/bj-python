#!/bin/sh

rm stats.txt
make quicktest

echo Test differences:
diff stats.txt data/std_quicktest.txt

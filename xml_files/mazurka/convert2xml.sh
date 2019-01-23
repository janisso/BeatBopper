#!/bin/bash
FILES=$PWD
M="M"
e=".xml"
for f in *.krn
do
	echo "Converting $f"
	n=$(echo $f | head -c 11 | tail -c 4)
	./hum2xml $f > $M$n$e
done
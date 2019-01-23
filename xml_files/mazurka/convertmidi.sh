#!/bin/bash
FILES=$PWD
M="M"
e=".mid"
for f in *.xml
do
	echo "Converting $f"
	mscore $f -o ${f%%.*}$e
done
#!/bin/bash

LINKS=("8.8.8.8" "unimelb.edu.au" "caltech.edu")
UNI_LIST=(unsw unisa mcgill)
INDEX=1

for link in "${LINKS[@]}"
do
	: 
	START=$(date +%s)
	echo $START
	echo $INDEX
	echo "$link"
	traceroute $link
	echo "`date`, google, toupin" >> log.csv
	((INDEX++))

	END=$(date +%s)
	DIFF=$(($END-$START))
	echo $START
	echo $END
	echo "It took $DIFF seconds"
done


